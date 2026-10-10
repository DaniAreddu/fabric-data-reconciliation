"""Structural checks for the Fabric notebook. These do not run PySpark or Fabric."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / 'fabric_reconciliation.ipynb'
TABLE_ROLES = {'bronze_snapshots', 'silver_records', 'exceptions', 'review_decisions', 'match_pairs',
               'review_queue', 'gold_customers', 'gold_source_links', 'held_records', 'run_metrics'}


class NotebookTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        cls.code = [''.join(c['source']) for c in cls.nb['cells'] if c['cell_type'] == 'code']
        cls.markdown = [''.join(c['source']) for c in cls.nb['cells'] if c['cell_type'] == 'markdown']

    def test_nbformat_structure(self):
        self.assertEqual((self.nb['nbformat'], self.nb['nbformat_minor']), (4, 5))
        self.assertEqual(self.nb['metadata']['kernelspec']['name'], 'synapse_pyspark')
        ids = [c.get('id') for c in self.nb['cells']]
        self.assertTrue(all(isinstance(i, str) and re.fullmatch(r'[A-Za-z0-9_-]{1,64}', i) for i in ids), ids)
        self.assertEqual(len(ids), len(set(ids)))
        for cell in self.nb['cells']:
            self.assertIn(cell['cell_type'], ('code', 'markdown'))
            self.assertIsInstance(cell['metadata'], dict)
            self.assertIsInstance(cell['source'], list)

    def test_no_outputs_are_committed(self):
        for cell in self.nb['cells']:
            if cell['cell_type'] == 'code':
                self.assertEqual(cell['outputs'], [])
                self.assertIsNone(cell['execution_count'])

    def test_code_cells_compile(self):
        self.assertEqual(len(self.code), 9)
        for i, source in enumerate(self.code):
            compile(source, 'notebook code cell %d' % i, 'exec')

    def test_embedded_rules_match_reference(self):
        shared = (ROOT / 'reference.py').read_text(encoding='utf-8').split('\ndef main():')[0]
        self.assertEqual(self.code[1].rstrip(), shared.rstrip())

    def test_configuration(self):
        config = self.code[0]
        self.assertIn("BASE = Path('/lakehouse/default/Files/reconciliation_demo')", config)
        self.assertIn("PREFIX = 'recon_demo_'", config)
        self.assertIn("SCHEMA = ''", config)

    @staticmethod
    def call_arguments(source, function):
        """Return the argument text of each call, following nested parentheses."""
        calls = []
        for match in re.finditer(re.escape(function) + r'\(', source):
            depth, i = 1, match.end()
            while depth:
                depth += {'(': 1, ')': -1}.get(source[i], 0)
                i += 1
            calls.append(source[match.end():i - 1])
        return calls

    def test_every_table_goes_through_the_prefix(self):
        source = '\n'.join(self.code)
        self.assertNotRegex(source, r"saveAsTable\(\s*['\"]")
        written = [args for args in self.call_arguments(source, 'write_demo') if args != 'df, role']
        roles = {re.search(r"'([a-z_]+)'\s*$", args).group(1) for args in written}
        roles |= set(re.findall(r"table_name\('([a-z_]+)'\)", source))
        self.assertEqual(roles, TABLE_ROLES)

    def test_b001_assertions_match_expected_metrics(self):
        metrics = json.loads((ROOT / 'expected/B001_results.json').read_text(encoding='utf-8'))['metrics']
        compact = re.sub(r'\s+', '', self.code[6])
        for name, value in metrics.items():
            self.assertIn("'%s':%d" % (name, value), compact)

    def test_markdown_mentions_only_existing_repository_files(self):
        text = '\n'.join(self.markdown)
        for name in set(re.findall(r'[\w./-]+\.(?:csv|json|md|py)\b', text)):
            matches = list(ROOT.glob(name)) or list(ROOT.glob('**/' + Path(name).name))
            self.assertTrue(matches, name)


if __name__ == '__main__':
    unittest.main()
