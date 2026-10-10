"""Build or verify the files attached to a GitHub release.

    python scripts/build_release.py v1.0.0          # writes dist/v1.0.0/ from the committed HEAD
    python scripts/build_release.py --verify DIR    # checks DIR against its SHA256SUMS.txt

The materials ZIP is made with `git archive`, so it contains exactly the committed
files of HEAD. The decks are attached separately and left out of the ZIP.
"""
import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATTACHMENTS = [
    'presentations/Sofia_2026_English_Extended_Final.pptx',
    'presentations/Sofia_2026_English_Extended_Final.pdf',
    'presentations/reconciliation_checklist.pdf',
    'talks/50min/Sofia_2026_English_50min_Speech.md',
    'talks/50min/Sofia_2026_English_50min_Timing.md',
    'talks/extended/Sofia_2026_English_Extended_Speech.md',
    'talks/extended/Sofia_2026_English_Extended_Timing.md',
]
LEFT_OUT_OF_ZIP = ['presentations/*.pptx', 'presentations/Sofia_*.pdf']


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, check=True, capture_output=True).stdout


def build(version):
    if git('status', '--porcelain', '--untracked-files=no').strip():
        sys.exit('Commit or stash changes first: the release must match a commit.')
    out = ROOT / 'dist' / version
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for name in ATTACHMENTS:
        # Take each attachment from HEAD, not from the working tree.
        (out / Path(name).name).write_bytes(git('show', 'HEAD:' + name))
    archive = out / ('fabric-data-reconciliation-%s-materials.zip' % version)
    git('archive', '--format=zip', '--prefix=fabric-data-reconciliation-%s/' % version, '-o', str(archive),
        'HEAD', '--', '.', *(':(exclude,glob)' + p for p in LEFT_OUT_OF_ZIP))
    files = sorted(p for p in out.iterdir() if p.name != 'SHA256SUMS.txt')
    (out / 'SHA256SUMS.txt').write_text(''.join('%s  %s\n' % (sha256(p), p.name) for p in files),
                                        encoding='utf-8', newline='\n')
    print('Built %s from commit %s:' % (out.relative_to(ROOT).as_posix(), git('rev-parse', '--short', 'HEAD').decode().strip()))
    for p in files + [out / 'SHA256SUMS.txt']:
        print('  %10d  %s' % (p.stat().st_size, p.name))


def verify(folder):
    folder = Path(folder)
    failures = 0
    for line in (folder / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        expected, name = line.split('  ', 1)
        path = folder / name
        status = 'missing' if not path.exists() else 'OK' if sha256(path) == expected else 'MISMATCH'
        failures += status != 'OK'
        print('%-8s %s' % (status, name))
    sys.exit(1 if failures else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('version', nargs='?', help='release tag, for example v1.0.0')
    parser.add_argument('--verify', metavar='DIR', help='verify the files in DIR against DIR/SHA256SUMS.txt')
    args = parser.parse_args()
    if args.verify:
        verify(args.verify)
    elif args.version:
        build(args.version)
    else:
        parser.error('give a version to build or --verify DIR')


if __name__ == '__main__':
    main()
