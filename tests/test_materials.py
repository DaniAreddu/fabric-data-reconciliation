"""Checks for the talk scripts, timing budgets, decks and Messina display labels."""
import csv
import posixpath
import re
import unittest
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORDS_PER_MINUTE = 110
# Budget items besides the speech, in seconds, as listed in both timing files.
OTHER_SECONDS = {'visual observation': 171, 'slide changes': 39, 'six exchanges': 150, 'Q&A': 480, 'margin': 120}
EDITIONS = {
    '50min': {'speech': 'talks/50min/Sofia_2026_English_50min_Speech.md',
              'timing': 'talks/50min/Sofia_2026_English_50min_Timing.md',
              'deck': 'presentations/Sofia_2026_English_50min_Final', 'words': 3780, 'before_qa': 3678,
              'speech_time': '33:26', 'total': '49:52'},
    'extended': {'speech': 'talks/extended/Sofia_2026_English_Extended_Speech.md',
                 'timing': 'talks/extended/Sofia_2026_English_Extended_Timing.md',
                 'deck': 'presentations/Sofia_2026_English_Extended_Final', 'words': 4586, 'before_qa': 4484,
                 'speech_time': '40:46', 'total': '57:12'},
}
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}


def speech_paragraphs(path):
    body = (ROOT / path).read_text(encoding='utf-8').split('\n## Sources')[0]
    return [p.strip() for p in body.split('\n\n') if p.strip()]


def minutes(seconds):
    seconds = round(seconds)
    return '%d:%02d' % divmod(seconds, 60)


def pptx_notes(path):
    """Speaker-notes body text per slide, in presentation order."""
    with zipfile.ZipFile(path) as z:
        def rels(part):
            """Map relationship ids to (type, part name), resolving relative and absolute targets."""
            folder, name = part.rsplit('/', 1)
            tree = ET.fromstring(z.read('%s/_rels/%s.rels' % (folder, name)))
            out = {}
            for r in tree.findall('rel:Relationship', NS):
                target = r.get('Target')
                target = target[1:] if target.startswith('/') else posixpath.normpath(posixpath.join(folder, target))
                out[r.get('Id')] = (r.get('Type').rsplit('/', 1)[1], target)
            return out
        presentation = ET.fromstring(z.read('ppt/presentation.xml'))
        targets = rels('ppt/presentation.xml')
        notes = []
        for slide in presentation.find('p:sldIdLst', NS):
            slide_part = targets[slide.get('{%s}id' % NS['r'])][1]
            note_target = [t for kind, t in rels(slide_part).values() if kind == 'notesSlide']
            text = ''
            if note_target:
                note = ET.fromstring(z.read(note_target[0]))
                for shape in note.iter('{%s}sp' % NS['p']):
                    placeholder = shape.find('.//p:nvPr/p:ph', NS)
                    if placeholder is not None and placeholder.get('type') == 'body':
                        text = '\n'.join(''.join(t.text or '' for t in para.iter('{%s}t' % NS['a']))
                                         for para in shape.iter('{%s}p' % NS['a']))
            notes.append(text)
        return notes


def pdf_pages(path):
    data = path.read_bytes()
    return len(re.findall(rb'/Type\s*/Page(?![a-zA-Z])', data))


def normalise_text(text):
    return ' '.join(text.replace('’', "'").split())


class TalkTest(unittest.TestCase):
    def test_word_counts_and_timing(self):
        for name, edition in EDITIONS.items():
            with self.subTest(edition=name):
                paragraphs = speech_paragraphs(edition['speech'])
                words = [len(p.split()) for p in paragraphs]
                # The last two paragraphs are the Q&A invitation and the closing contacts.
                self.assertEqual(words[-2:], [54, 48])
                self.assertEqual(sum(words), edition['words'])
                self.assertEqual(sum(words[:-2]), edition['before_qa'])
                speech = edition['before_qa'] * 60 / WORDS_PER_MINUTE
                contacts = 48 * 60 / WORDS_PER_MINUTE
                total = speech + contacts + sum(OTHER_SECONDS.values())
                self.assertEqual(minutes(speech), edition['speech_time'])
                self.assertEqual(minutes(total), edition['total'])
                timing = (ROOT / edition['timing']).read_text(encoding='utf-8')
                self.assertIn('**%s**' % edition['total'], timing)
                self.assertIn('| %s |' % edition['speech_time'], timing)
                self.assertIn('{:,}'.format(edition['before_qa']), timing)

    def test_sources_appear_only_in_the_final_bibliography(self):
        for name, edition in EDITIONS.items():
            with self.subTest(edition=name):
                text = (ROOT / edition['speech']).read_text(encoding='utf-8')
                self.assertEqual(text.count('## Sources'), 1)
                body = text.split('\n## Sources')[0]
                self.assertNotRegex(body, r'https?://')
                self.assertFalse(any(line.startswith('#') for line in body.splitlines()))

    def test_extended_is_not_presented_as_a_50_minute_talk(self):
        timing = (ROOT / EDITIONS['extended']['timing']).read_text(encoding='utf-8')
        self.assertIn('exceeds 50 minutes', timing)


class DeckTest(unittest.TestCase):
    def test_published_decks_have_40_slides_and_the_matching_notes(self):
        checked = 0
        for name, edition in EDITIONS.items():
            pptx = ROOT / (edition['deck'] + '.pptx')
            pdf = ROOT / (edition['deck'] + '.pdf')
            if not pptx.exists():
                continue
            with self.subTest(edition=name):
                notes = pptx_notes(pptx)
                self.assertEqual(len(notes), 40)
                self.assertEqual(normalise_text(' '.join(notes)),
                                 normalise_text(' '.join(speech_paragraphs(edition['speech']))))
                self.assertFalse([i for i, n in enumerate(notes, 1) if re.search(r'https?://', n)])
                self.assertEqual(pdf_pages(pdf), 40)
                checked += 1
        self.assertGreaterEqual(checked, 1)

    def test_checklist_is_one_page(self):
        self.assertEqual(pdf_pages(ROOT / 'presentations/reconciliation_checklist.pdf'), 1)


class MessinaDataTest(unittest.TestCase):
    def read(self, name):
        with (ROOT / 'datasets' / name).open(newline='', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    def test_display_labels_are_a_separate_mapping_of_the_public_rows(self):
        public = {r['id']: r for r in self.read('messina_public_sample.csv')}
        labels = self.read('messina_display_labels.csv')
        self.assertEqual(sorted(public), sorted(r['id'] for r in labels))
        for label in labels:
            row = public[label['id']]
            self.assertEqual(label['official_street_name'], row['odonimo'])
            self.assertEqual(label['civic'], row['civico'])
        self.assertEqual(list(public.values())[0].keys(),
                         {'id', 'odonimo', 'civico', 'esponente', 'lat', 'long', 'data_rilevazione'})

    def test_street_review_is_scoped_to_the_street_link(self):
        (decision,) = self.read('messina_review_decisions.csv')
        self.assertEqual((decision['evidence_reference'], decision['decision_scope']), ('REF-CELI-01', 'STREET_LINK'))
        self.assertEqual(decision['status'], 'VALIDATED_LOCAL_TARGET_PENDING')


if __name__ == '__main__':
    unittest.main()
