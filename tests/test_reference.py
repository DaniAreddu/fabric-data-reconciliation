"""Decision checks for reference.py, using the published datasets."""
import csv
import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import reference as ref  # noqa: E402

DATASETS = ROOT / 'datasets'
ALFA_CUSTOMER_ID = 'CUS-a60635aa3160'


def load_reviews():
    with (DATASETS / 'review_decisions.csv').open(newline='') as f:
        return list(csv.DictReader(f))


def load_b002():
    with (DATASETS / 'erp_B002.csv').open(newline='') as f:
        return [dict(r, source='ERP', batch_id='B002', ingested_at='2026-10-09T09:00:00Z')
                for r in csv.DictReader(f)]


def by_pair(result):
    return {p['pair_key']: p for p in result['pairs']}


def replace(rows, source_key, **changes):
    return [dict(r, **changes) if r['source'] + ':' + r['record_id'] == source_key else r for r in rows]


class Fixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = ref.load_inputs(DATASETS)
        cls.reviews = load_reviews()
        cls.b001 = ref.evaluate(cls.rows, cls.reviews)


class NormalisationTest(Fixture):
    def test_english_address_forms_compare_equal(self):
        self.assertEqual(ref.norm_address('Roma St., 12'), 'roma street 12')
        self.assertEqual(ref.norm_address('Roma Street 12'), 'roma street 12')

    def test_house_number_survives_normalisation(self):
        self.assertNotEqual(ref.norm_address('Roma Street 10'), ref.norm_address('Roma St., 12'))

    def test_names_ignore_case_and_punctuation(self):
        self.assertEqual(ref.norm_name('ALFA LTD'), 'alfa ltd')
        self.assertEqual(ref.norm_name('Alfa Ltd.'), 'alfa ltd')

    def test_silver_keeps_original_values_beside_comparison_fields(self):
        silver = {r['source_key']: r for r in self.b001['silver_records']}
        erp = silver['ERP:E501']
        self.assertEqual((erp['company_name'], erp['address']), ('ALFA LTD', 'Roma St., 12'))
        self.assertEqual((erp['name_norm'], erp['address_norm']), ('alfa ltd', 'roma street 12'))
        self.assertEqual(silver['PORTAL:P901']['address_norm'], 'roma street 10')


class IdentifierTest(Fixture):
    def record(self, business_id, source='CRM', record_id='X1'):
        return ref.normalise(dict(self.rows[0], source=source, record_id=record_id, business_id=business_id))

    def test_format_validation(self):
        self.assertEqual(ref.usable_id(''), '')
        self.assertEqual(ref.usable_id(None), '')
        self.assertEqual(ref.usable_id('BAD-ID'), '')
        self.assertEqual(ref.usable_id('DEMO-1'), '')
        self.assertEqual(ref.usable_id(' demo-001 '), 'DEMO-001')

    def test_two_missing_ids_are_not_evidence(self):
        pair = ref.score_pair(self.record(''), self.record('', 'ERP', 'X2'))
        self.assertFalse(pair['exact_id'])
        self.assertFalse(pair['id_conflict'])

    def test_malformed_id_is_neither_match_nor_conflict(self):
        pair = ref.score_pair(self.record('BAD-ID'), self.record('DEMO-001', 'ERP', 'X2'))
        self.assertFalse(pair['exact_id'])
        self.assertFalse(pair['id_conflict'])

    def test_two_usable_ids_that_disagree_conflict(self):
        pair = ref.score_pair(self.record('DEMO-002'), self.record('DEMO-009', 'ERP', 'X2'))
        self.assertTrue(pair['id_conflict'])
        self.assertEqual(pair['route'], 'REJECT')


class CandidateTest(Fixture):
    def test_source_counts(self):
        counts = {}
        for r in self.rows:
            counts[r['source']] = counts.get(r['source'], 0) + 1
        self.assertEqual(counts, {'CRM': 4, 'ERP': 3, 'PORTAL': 2})

    def test_26_cross_source_pairs_become_7_candidates(self):
        silver = [ref.normalise(r) for r in self.rows]
        possible = [(a, b) for a, b in itertools.combinations(silver, 2) if a['source'] != b['source']]
        self.assertEqual(len(possible), 26)
        self.assertEqual(sorted(by_pair(self.b001)), [
            'CRM:C101|ERP:E501', 'CRM:C101|PORTAL:P901', 'CRM:C102|ERP:E502', 'CRM:C103|ERP:E503',
            'CRM:C103|PORTAL:P902', 'ERP:E501|PORTAL:P901', 'ERP:E503|PORTAL:P902'])

    def test_included_pair_without_shared_id(self):
        silver = {r['source_key']: r for r in map(ref.normalise, self.rows)}
        crm, portal = silver['CRM:C103'], silver['PORTAL:P902']
        self.assertEqual((crm['usable_id'], portal['usable_id']), ('', ''))
        self.assertEqual(crm['postcode_norm'], portal['postcode_norm'])
        self.assertEqual(crm['name_norm'][:3], portal['name_norm'][:3])
        self.assertTrue(ref.candidate(crm, portal))

    def test_excluded_pair_nova_and_alfa(self):
        silver = {r['source_key']: r for r in map(ref.normalise, self.rows)}
        self.assertFalse(ref.candidate(silver['CRM:C104'], silver['PORTAL:P901']))
        self.assertFalse(any('CRM:C104' in key for key in by_pair(self.b001)))


class RoutingTest(Fixture):
    def test_aurora_conflict_beats_a_perfect_score(self):
        aurora = by_pair(self.b001)['CRM:C102|ERP:E502']
        self.assertEqual(aurora['score'], 100)
        self.assertEqual((aurora['route'], aurora['reason']), ('REJECT', 'ID_CONFLICT'))
        published = {g['business_id']: g for g in self.b001['gold_customers']}
        self.assertEqual(published['DEMO-002']['name_source_key'], 'CRM:C102')
        self.assertEqual(published['DEMO-009']['name_source_key'], 'ERP:E502')

    def test_a_review_approval_cannot_override_an_id_conflict(self):
        approval = dict(self.reviews[0], pair_key='CRM:C102|ERP:E502',
                        evidence_fingerprint=by_pair(self.b001)['CRM:C102|ERP:E502']['evidence_fingerprint'])
        result = ref.evaluate(self.rows, self.reviews + [approval])
        self.assertEqual(by_pair(result)['CRM:C102|ERP:E502']['route'], 'REJECT')

    def test_shared_reliable_id_links_despite_a_low_score(self):
        portal = by_pair(self.b001)['CRM:C101|PORTAL:P901']
        self.assertEqual(portal['score'], 45)
        self.assertEqual((portal['route'], portal['reason']), ('AUTO', 'EXACT_DEMO_ID'))

    def test_score_formula_on_delta_portal(self):
        pair = by_pair(self.b001)['ERP:E503|PORTAL:P902']
        similarity = 1 - 1 / len('delta services')
        self.assertAlmostEqual(pair['name_similarity'], similarity)
        self.assertEqual(pair['score'], round(60 * similarity + 25 + 15, 6))
        self.assertEqual(pair['score'], 95.714286)
        self.assertEqual(pair['initial_route'], 'REVIEW')

    def test_non_exact_pair_below_70_stays_separate(self):
        a = ref.normalise(dict(self.rows[0], business_id='', address='North Street 1'))
        b = ref.normalise(dict(self.rows[0], source='ERP', record_id='E9', business_id='',
                               company_name='Alfa Holdings', address='South Street 2'))
        pair = ref.score_pair(a, b)
        self.assertLess(pair['score'], 70)
        self.assertEqual(pair['route'], 'KEEP_SEPARATE')


class DeltaReviewTest(Fixture):
    def test_approval_covers_only_the_reviewed_pair(self):
        pairs = by_pair(self.b001)
        approved = pairs['CRM:C103|ERP:E503']
        self.assertEqual(approved['route'], 'APPROVED')
        self.assertEqual(approved['evidence_reference'], 'ONB-DELTA-42')
        for key in ('CRM:C103|PORTAL:P902', 'ERP:E503|PORTAL:P902'):
            self.assertEqual(pairs[key]['route'], 'REVIEW')
            self.assertNotIn('evidence_reference', pairs[key])
        self.assertEqual(self.b001['held_source_keys'], ['PORTAL:P902'])
        linked = {link['source_key'] for link in self.b001['gold_source_links']}
        self.assertIn('CRM:C103', linked)
        self.assertNotIn('PORTAL:P902', linked)

    def test_saved_fingerprint_matches_the_current_english_records(self):
        self.assertEqual(self.reviews[0]['rule_version'], ref.RULE_VERSION)
        self.assertEqual(ref.RULE_VERSION, 'recon-demo-v2-en')
        self.assertEqual(self.reviews[0]['evidence_fingerprint'],
                         by_pair(self.b001)['CRM:C103|ERP:E503']['evidence_fingerprint'])

    def assert_review_not_applied(self, rows, reviews):
        result = ref.evaluate(rows, reviews)
        delta = by_pair(result)['CRM:C103|ERP:E503']
        self.assertEqual(delta['route'], 'REVIEW')
        self.assertEqual(delta['reason'], 'STALE_OR_INCOMPLETE_REVIEW')
        self.assertEqual(result['metrics']['approved_review_pairs'], 0)

    def test_changed_compared_field_makes_the_approval_stale(self):
        self.assert_review_not_applied(replace(self.rows, 'ERP:E503', address='Port Street 7'), self.reviews)

    def test_changed_rule_version_makes_the_approval_stale(self):
        self.assert_review_not_applied(self.rows, [dict(self.reviews[0], rule_version='recon-demo-v1')])

    def test_missing_evidence_reference_makes_the_approval_incomplete(self):
        self.assert_review_not_applied(self.rows, [dict(self.reviews[0], evidence_reference='')])

    def test_load_metadata_does_not_change_the_fingerprint(self):
        reloaded = replace(self.rows, 'ERP:E503', batch_id='B009', ingested_at='2026-10-10T09:00:00Z')
        result = ref.evaluate(reloaded, self.reviews)
        self.assertEqual(by_pair(result)['CRM:C103|ERP:E503']['route'], 'APPROVED')


class GroupGuardTest(Fixture):
    def bridge(self):
        with (DATASETS / 'group_check_example.csv').open(newline='') as f:
            nodes = list(csv.DictReader(f))
        records = []
        for node in nodes:
            source, record_id = node['source_key'].split(':')
            records.append(ref.normalise(dict(self.rows[0], source=source, record_id=record_id,
                                              business_id=node['business_id'])))
        return nodes, records

    def test_missing_middle_id_cannot_join_a_contradictory_group(self):
        nodes, (a, b, c) = self.bridge()
        self.assertEqual([n['business_id'] for n in nodes], ['DEMO-002', '', 'DEMO-009'])
        edges = [dict(ref.score_pair(a, b), route='APPROVED'), dict(ref.score_pair(b, c), route='APPROVED')]
        result = ref.consolidate([a, b, c], edges)
        self.assertEqual([p['route'] for p in result['pairs']].count('GROUP_CONFLICT'), 1)
        customer = {link['source_key']: link['customer_id'] for link in result['gold_source_links']}
        self.assertNotEqual(customer.get('CRM:A'), customer.get('PORTAL:C'))

    def test_recorded_rejection_blocks_the_whole_group(self):
        _, records = self.bridge()
        a, b, c = [dict(r, usable_id='') for r in records]
        edges = [dict(ref.score_pair(a, b), route='APPROVED'), dict(ref.score_pair(b, c), route='APPROVED'),
                 dict(ref.score_pair(a, c), route='REJECT')]
        result = ref.consolidate([a, b, c], edges)
        self.assertIn('GROUP_CONFLICT', [p['route'] for p in result['pairs']])


class GoldTest(Fixture):
    def gold(self, result, business_id):
        return next(g for g in result['gold_customers'] if g['business_id'] == business_id)

    def test_alfa_value_provenance(self):
        alfa = self.gold(self.b001, 'DEMO-001')
        self.assertEqual(alfa['customer_id'], ALFA_CUSTOMER_ID)
        self.assertEqual((alfa['display_name'], alfa['name_source_key']), ('Alfa Ltd', 'CRM:C101'))
        self.assertEqual((alfa['billing_address'], alfa['billing_address_source_key']), ('Roma St., 12', 'ERP:E501'))

    def test_membership_is_separate_from_value_provenance(self):
        members = sorted(l['source_key'] for l in self.b001['gold_source_links'] if l['customer_id'] == ALFA_CUSTOMER_ID)
        self.assertEqual(members, ['CRM:C101', 'ERP:E501', 'PORTAL:P901'])
        alfa = self.gold(self.b001, 'DEMO-001')
        self.assertEqual({alfa['name_source_key'], alfa['billing_address_source_key']}, {'CRM:C101', 'ERP:E501'})

    def test_delta_publishes_from_crm_and_erp(self):
        delta = self.gold(self.b001, 'DEMO-003')
        self.assertEqual((delta['name_source_key'], delta['billing_address_source_key']), ('CRM:C103', 'ERP:E503'))

    def test_billing_falls_back_to_crm_when_erp_is_empty(self):
        result = ref.evaluate(replace(self.rows, 'ERP:E501', address=''), self.reviews)
        alfa = self.gold(result, 'DEMO-001')
        self.assertEqual((alfa['billing_address'], alfa['billing_address_source_key']), ('Roma Street 12', 'CRM:C101'))

    def test_customer_id_is_derived_from_the_reliable_company_id(self):
        expected = 'CUS-' + hashlib.sha256(b'business:DEMO-001').hexdigest()[:12]
        self.assertEqual(expected, ALFA_CUSTOMER_ID)


class SnapshotTest(Fixture):
    def test_rerunning_a_batch_adds_no_snapshot(self):
        history = ref.upsert_snapshot([], self.rows)
        self.assertEqual(len(ref.upsert_snapshot(history, self.rows)), 9)

    def test_reusing_a_batch_key_for_different_values_fails(self):
        history = ref.upsert_snapshot([], self.rows)
        with self.assertRaises(ValueError):
            ref.upsert_snapshot(history, replace(self.rows, 'ERP:E501', address='Roma Street 99'))

    def test_b002_file_matches_the_update_used_by_reference_checks(self):
        (update,) = load_b002()
        self.assertEqual(update['record_id'], 'E501')
        self.assertEqual(update['address'], 'Roma Street 14')
        self.assertEqual(update['source_updated_at'], '2026-10-09T08:00:00Z')
        original = next(r for r in self.rows if r['source'] == 'ERP' and r['record_id'] == 'E501')
        for field in ('company_name', 'business_id', 'postcode', 'city'):
            self.assertEqual(update[field], original[field])

    def test_b002_keeps_alfa_identity_and_publishes_the_new_address(self):
        history = ref.upsert_snapshot(ref.upsert_snapshot([], self.rows), load_b002())
        self.assertEqual(len(history), 10)
        self.assertEqual(len(ref.upsert_snapshot(history, load_b002())), 10)
        current = ref.latest_snapshot(history)
        self.assertEqual(len(current), 9)
        result = ref.evaluate(current, self.reviews)
        self.assertEqual(result['metrics']['published_entities'], 5)
        self.assertEqual(result['metrics']['approved_review_pairs'], 1)
        alfa = next(g for g in result['gold_customers'] if g['business_id'] == 'DEMO-001')
        self.assertEqual(alfa['customer_id'], ALFA_CUSTOMER_ID)
        self.assertEqual((alfa['billing_address'], alfa['billing_address_source_key']), ('Roma Street 14', 'ERP:E501'))
        link = next(l for l in result['gold_source_links'] if l['source_key'] == 'ERP:E501')
        self.assertEqual(link['batch_id'], 'B002')


class LabelTest(Fixture):
    def test_unknown_labels_stay_out_of_the_measurement(self):
        with (DATASETS / 'labelled_pairs.csv').open(newline='') as f:
            labels = {r['pair_key']: r['label'] for r in csv.DictReader(f)}
        self.assertEqual(sorted(k for k, v in labels.items() if v == 'UNKNOWN'),
                         ['CRM:C103|PORTAL:P902', 'ERP:E503|PORTAL:P902'])
        routes = {k: p['route'] for k, p in by_pair(self.b001).items()}
        known = {k: v for k, v in labels.items() if v in ('MATCH', 'DIFFERENT')}
        accepted = {k for k in known if routes.get(k) in ('AUTO', 'APPROVED')}
        true_positive = sum(known[k] == 'MATCH' for k in accepted)
        false_positive = sum(known[k] == 'DIFFERENT' for k in accepted)
        false_negative = sum(v == 'MATCH' and k not in accepted for k, v in known.items())
        self.assertEqual((true_positive, false_positive, false_negative), (4, 0, 0))


class ExpectedOutputTest(unittest.TestCase):
    def run_reference(self, folder, *args):
        return subprocess.run([sys.executable, str(folder / 'reference.py'), *args],
                              capture_output=True, text=True, cwd=folder)

    def test_fresh_run_matches_versioned_outputs_byte_for_byte(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = self.run_reference(ROOT, '--output-dir', tmp)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            for name in ('B001_results.json', 'B002_results.json'):
                self.assertEqual((Path(tmp) / name).read_bytes(), (ROOT / 'expected' / name).read_bytes(), name)

    def test_in_process_results_match_versioned_json(self):
        rows, reviews = ref.load_inputs(DATASETS), load_reviews()
        before, after = ref.checks(rows, reviews)
        self.assertEqual(json.loads((ROOT / 'expected/B001_results.json').read_text(encoding='utf-8')),
                         json.loads(json.dumps(before)))
        self.assertEqual(json.loads((ROOT / 'expected/B002_results.json').read_text(encoding='utf-8')),
                         json.loads(json.dumps(after)))

    def test_divergence_fails_and_leaves_expected_files_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            shutil.copy(ROOT / 'reference.py', work)
            shutil.copytree(DATASETS, work / 'datasets')
            shutil.copytree(ROOT / 'expected', work / 'expected')
            golden = work / 'expected' / 'B001_results.json'
            altered = golden.read_text(encoding='utf-8').replace('Roma St., 12', 'Roma St., 13')
            golden.write_text(altered, encoding='utf-8')
            run = self.run_reference(work)
            self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
            self.assertIn('B001_results.json', run.stdout)
            self.assertEqual(golden.read_text(encoding='utf-8'), altered)


if __name__ == '__main__':
    unittest.main()
