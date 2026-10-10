"""Repository hygiene checks that need only the Python standard library.

    python scripts/check_repo.py              # local checks; exit 1 on any problem
    python scripts/check_repo.py --external   # also report the status of external links

Problems are reported as path and problem type. Matched values are never printed.
"""
import argparse
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {'.md', '.py', '.json', '.csv', '.ipynb', '.mmd', '.yml', '.yaml', '.txt', '.svg', ''}
MAX_FILE_BYTES = 25 * 1024 * 1024

SECRET_PATTERNS = {
    'GitHub token': r'\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{30,}',
    'AWS access key': r'\bAKIA[0-9A-Z]{16}\b',
    'private key block': r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----',
    'Slack token': r'\bxox[abprs]-[A-Za-z0-9-]{10,}',
    'storage account key': r'AccountKey=[A-Za-z0-9+/=]{20,}',
    'API key assignment': r'(?i)\b(?:api[_-]?key|secret|password|passwd|token)\b\s*[:=]\s*["\'][^"\'\s]{8,}["\']',
}
LOCAL_PATH_PATTERNS = {
    'Windows user path': r'(?i)\b[A-Z]:[\\/]+Users[\\/]',
    'Git Bash user path': r'(?i)(?<![\w.])/c/Users/',
    'home directory path': r'(?<![\w.])/(?:home|Users)/[A-Za-z0-9._-]+/',
    'temporary folder path': r'(?i)AppData[\\/]+Local[\\/]+Temp',
}
FORBIDDEN_NAMES = [
    (r'(^|/)\.env(\..*)?$', 'environment file'),
    (r'\.(pem|key|pfx|p12)$', 'key or certificate file'),
    (r'(^|/)~\$', 'Office lock file'),
    (r'(^|/)(__pycache__|\.ipynb_checkpoints|\.venv|venv)/', 'cache or environment folder'),
    (r'\.(log|tmp|bak)$', 'log or temporary file'),
    (r'(^|/)(output|dist)/', 'generated output'),
]
LINK = re.compile(r'(!?)\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')


def tracked_files():
    try:
        out = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True).stdout
        return [ROOT / p for p in out.decode('utf-8').split('\0') if p]
    except (OSError, subprocess.CalledProcessError):
        # Outside Git (for example an extracted source archive), skip what .gitignore would skip.
        skipped = {'.git', '__pycache__', '.ipynb_checkpoints', '.venv', 'venv', 'output', 'dist'}
        return [p for p in ROOT.rglob('*') if p.is_file() and not skipped & set(p.relative_to(ROOT).parts)]


def rel(path):
    return path.relative_to(ROOT).as_posix()


def is_text(path):
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {'LICENSE', 'LICENSE-DOCS', '.gitignore', '.gitattributes'}


def github_anchor(heading):
    text = re.sub(r'[`*_]|\[([^\]]*)\]\([^)]*\)', r'\1', heading.strip().lower())
    text = ''.join(c for c in text if c.isalnum() or c in ' -' or unicodedata.category(c) == 'Pc')
    return text.replace(' ', '-')


def anchors(markdown_path):
    found, in_code = set(), False
    for line in markdown_path.read_text(encoding='utf-8').splitlines():
        if line.startswith('```'):
            in_code = not in_code
        elif not in_code and line.startswith('#'):
            found.add(github_anchor(line.lstrip('#')))
    return found


def check_links(files, problems):
    external = set()
    for md in (f for f in files if f.suffix == '.md'):
        in_code = False
        for line in md.read_text(encoding='utf-8').splitlines():
            if line.startswith('```'):
                in_code = not in_code
            if in_code:
                continue
            for bang, target in LINK.findall(line):
                if re.match(r'https?://', target):
                    external.add(target)
                    continue
                if target.startswith('mailto:'):
                    continue
                path_part, _, fragment = target.partition('#')
                resolved = (md.parent / path_part).resolve() if path_part else md
                kind = 'image' if bang else 'link'
                if not resolved.exists():
                    problems.append((rel(md), 'broken local %s: %s' % (kind, target)))
                elif fragment and resolved.suffix == '.md' and fragment not in anchors(resolved):
                    problems.append((rel(md), 'missing anchor: %s' % target))
    return external


def scan_text(name, text, problems):
    for kind, pattern in {**SECRET_PATTERNS, **LOCAL_PATH_PATTERNS}.items():
        if re.search(pattern, text):
            problems.append((name, kind))


def check_contents(files, problems):
    for path in files:
        name = rel(path)
        for pattern, kind in FORBIDDEN_NAMES:
            if re.search(pattern, name):
                problems.append((name, kind))
        if path.stat().st_size > MAX_FILE_BYTES:
            problems.append((name, 'file larger than %d MB' % (MAX_FILE_BYTES // 2 ** 20)))
        if path.resolve() == Path(__file__).resolve():
            continue  # this file contains the patterns themselves
        if is_text(path):
            scan_text(name, path.read_text(encoding='utf-8', errors='replace'), problems)
        elif path.suffix.lower() == '.pdf':
            scan_text(name, path.read_bytes().decode('latin-1'), problems)


def check_mermaid(files, problems):
    sources = {p.read_text(encoding='utf-8').strip() for p in (ROOT / 'docs' / 'diagrams').glob('*.mmd')}
    for md in (f for f in files if f.suffix == '.md'):
        blocks = re.findall(r'```mermaid\n(.*?)```', md.read_text(encoding='utf-8'), re.S)
        for block in blocks:
            if block.strip() not in sources:
                problems.append((rel(md), 'Mermaid block differs from every file in docs/diagrams/'))


def check_external(urls):
    print('\nExternal links (%d):' % len(urls))
    failures = 0
    for url in sorted(urls):
        request = urllib.request.Request(url, headers={'User-Agent': 'fabric-data-reconciliation link check'})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                status = response.status
        except urllib.error.HTTPError as error:
            status = error.code
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            status = type(error).__name__
        ok = isinstance(status, int) and status < 400
        failures += not ok
        print('  %s  %s' % (status, url))
    print('%d external link(s) did not answer with a success status.' % failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--external', action='store_true', help='also request every external link and report its status')
    args = parser.parse_args()
    files = tracked_files()
    problems = []
    external = check_links(files, problems)
    check_contents(files, problems)
    check_mermaid(files, problems)
    for path, kind in sorted(set(problems)):
        print('%s: %s' % (path, kind))
    print('Checked %d files: %d problem(s).' % (len(files), len(set(problems))))
    if args.external:
        check_external(external)
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
