"""Checks for the slides PDF, the checklist and the Messina display labels."""
import csv
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / 'slides' / 'When_Enterprise_Data_Disagrees_Sofia_2026.pdf'


def pdf_pages(data):
    # Counts page objects; valid while the file is saved without object streams.
    assert b'/ObjStm' not in data, 'page count needs a PDF without object streams'
    return len(re.findall(rb'/Type\s*/Page(?![a-zA-Z])', data))


class SlidesTest(unittest.TestCase):
    def test_slides_pdf_has_40_pages(self):
        self.assertEqual(pdf_pages(SLIDES.read_bytes()), 40)

    def test_slides_pdf_has_no_attachments_or_xmp_packet(self):
        data = SLIDES.read_bytes()
        self.assertNotIn(b'/EmbeddedFile', data)
        self.assertNotIn(b'/Metadata', data)

    def test_slides_pdf_title_and_author(self):
        data = SLIDES.read_bytes()
        self.assertIn(b'/Title (When Enterprise Data Disagrees: Reconciliation Patterns in Microsoft Fabric)', data)
        self.assertIn(b'/Author (Daniele Mario Areddu)', data)

    def test_only_one_slides_file(self):
        self.assertEqual([p.name for p in ROOT.rglob('*.pdf') if 'slides' in p.parts], [SLIDES.name])
        self.assertEqual(list(ROOT.rglob('*.pptx')), [])

    def test_checklist_is_one_page(self):
        self.assertEqual(pdf_pages((ROOT / 'docs' / 'reconciliation_checklist.pdf').read_bytes()), 1)


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
