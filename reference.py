"""Small, auditable reference implementation. Standard library only; not a scale design."""
import csv
import hashlib
import itertools
import json
import re
from pathlib import Path

RULE_VERSION = 'recon-demo-v2-en'
COMPARE_FIELDS = ('source_key', 'company_name', 'business_id', 'address', 'postcode', 'city')


def norm_name(value):
    return ' '.join(re.sub(r'[^a-z0-9 ]', '', (value or '').lower()).split())


def norm_address(value):
    value = re.sub(r'\bst\.(?=\s|,|$)', 'street', (value or '').lower().strip())
    return ' '.join(re.sub(r'[^a-z0-9 ]', '', value).split())


def usable_id(value):
    value = (value or '').strip().upper()
    return value if re.fullmatch(r'DEMO-[0-9]{3}', value) else ''


def normalise(record):
    r = dict(record)
    r['source_key'] = r['source'] + ':' + r['record_id']
    r.update(name_norm=norm_name(r['company_name']), address_norm=norm_address(r['address']),
             postcode_norm=(r.get('postcode') or '').strip().upper(),
             usable_id=usable_id(r.get('business_id')))
    return r


def edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def name_similarity(a, b):
    return 1 - edit_distance(a, b) / max(len(a), len(b)) if a and b else 0.0


def candidate(a, b):
    if a['source'] == b['source']:
        return False
    exact = bool(a['usable_id'] and a['usable_id'] == b['usable_id'])
    block = bool(a['postcode_norm'] and a['postcode_norm'] == b['postcode_norm']
                 and a['name_norm'] and b['name_norm'] and a['name_norm'][:3] == b['name_norm'][:3])
    return exact or block


def evidence_fingerprint(a, b):
    items = sorted((a, b), key=lambda r: r['source_key'])
    payload = {'rule_version': RULE_VERSION, 'records': [
        {key: (r.get(key) or '') for key in COMPARE_FIELDS} for r in items]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def score_pair(a, b):
    a, b = sorted((a, b), key=lambda r: r['source_key'])
    sim = name_similarity(a['name_norm'], b['name_norm'])
    address = bool(a['address_norm'] and a['address_norm'] == b['address_norm'])
    postcode = bool(a['postcode_norm'] and a['postcode_norm'] == b['postcode_norm'])
    exact = bool(a['usable_id'] and a['usable_id'] == b['usable_id'])
    conflict = bool(a['usable_id'] and b['usable_id'] and a['usable_id'] != b['usable_id'])
    score = 60 * sim + 25 * address + 15 * postcode
    route = 'REJECT' if conflict else 'AUTO' if exact else 'REVIEW' if score >= 70 else 'KEEP_SEPARATE'
    return {'pair_key': a['source_key'] + '|' + b['source_key'], 'a_key': a['source_key'],
            'b_key': b['source_key'], 'name_similarity': sim, 'same_address': address,
            'same_postcode': postcode, 'exact_id': exact, 'id_conflict': conflict,
            'score': round(score, 6), 'initial_route': route, 'route': route,
            'reason': 'ID_CONFLICT' if conflict else 'EXACT_DEMO_ID' if exact else 'REVIEW_SCORE' if route == 'REVIEW' else 'WEAK_EVIDENCE',
            'evidence_fingerprint': evidence_fingerprint(a, b), 'rule_version': RULE_VERSION}


def apply_reviews(pairs, reviews):
    by_key = {r['pair_key']: r for r in reviews}
    out = []
    for p in pairs:
        p = dict(p)
        review = by_key.get(p['pair_key'])
        if review and p['initial_route'] == 'REVIEW':
            valid = (review['rule_version'] == RULE_VERSION and
                     review['evidence_fingerprint'] == p['evidence_fingerprint'] and
                     bool(review.get('reviewer') and review.get('evidence_reference')))
            if not valid:
                p['reason'] = 'STALE_OR_INCOMPLETE_REVIEW'
            elif review['decision'] == 'APPROVE':
                p.update(route='APPROVED', reason='MANUAL_EVIDENCE', evidence_reference=review['evidence_reference'])
            elif review['decision'] == 'REJECT':
                p.update(route='REJECT', reason='MANUAL_REJECTION')
        out.append(p)
    return out


def consolidate(records, pairs):
    """Driver grouping for nine rows only. Check whole groups before each union."""
    records = {r['source_key']: r for r in records}
    parent = {k: k for k in records}
    def root(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k
    def members(k):
        return {x for x in records if root(x) == root(k)}
    denied = {frozenset((p['a_key'], p['b_key'])) for p in pairs if p['route'] == 'REJECT'}
    pairs = [dict(p) for p in pairs]
    for p in sorted(pairs, key=lambda p: (p['route'] != 'AUTO', p['pair_key'])):
        if p['route'] not in ('AUTO', 'APPROVED'):
            continue
        left, right = members(p['a_key']), members(p['b_key'])
        union = left | right
        ids = {records[k]['usable_id'] for k in union if records[k]['usable_id']}
        blocked = len(ids) > 1 or any(d <= union for d in denied)
        if blocked:
            p.update(route='GROUP_CONFLICT', reason='GROUP_CONTRADICTION')
        else:
            parent[root(p['b_key'])] = root(p['a_key'])
    held = set()
    for p in pairs:
        if p['route'] not in ('REVIEW', 'GROUP_CONFLICT'):
            continue
        left, right = members(p['a_key']), members(p['b_key'])
        if left == right:
            continue
        # Preserve a supported existing group; hold the new unresolved singleton.
        if len(left) > 1 and len(right) == 1:
            held |= right
        elif len(right) > 1 and len(left) == 1:
            held |= left
        else:
            held |= left | right
    groups = {}
    for key in records:
        if key not in held:
            groups.setdefault(root(key), []).append(records[key])
    gold, links = [], []
    for rows in groups.values():
        rows.sort(key=lambda r: r['source_key'])
        ids = {r['usable_id'] for r in rows if r['usable_id']}
        identity_anchor = 'business:' + next(iter(ids)) if ids else 'source:' + rows[0]['source_key']
        customer_id = 'CUS-' + hashlib.sha256(identity_anchor.encode()).hexdigest()[:12]
        def choose(field, priority):
            ordered = sorted(rows, key=lambda r: (priority.index(r['source']), r['source_key']))
            return next((r for r in ordered if r.get(field)), ordered[0])
        name = choose('company_name', ['CRM', 'ERP', 'PORTAL'])
        address = choose('address', ['ERP', 'CRM', 'PORTAL'])
        gold.append({'customer_id': customer_id, 'business_id': next(iter(ids)) if ids else '',
                     'display_name': name['company_name'], 'billing_address': address['address'],
                     'name_source_key': name['source_key'], 'billing_address_source_key': address['source_key'],
                     'rule_version': RULE_VERSION})
        links.extend({'source_key': r['source_key'], 'customer_id': customer_id,
                      'source_updated_at': r['source_updated_at'], 'batch_id': r['batch_id']} for r in rows)
    return {'pairs': pairs, 'gold_customers': sorted(gold, key=lambda r: r['customer_id']),
            'gold_source_links': sorted(links, key=lambda r: r['source_key']), 'held_source_keys': sorted(held)}


def evaluate(records, reviews=()):
    records = [normalise(r) for r in records]
    pairs = [score_pair(a, b) for a, b in itertools.combinations(records, 2) if candidate(a, b)]
    result = consolidate(records, apply_reviews(pairs, reviews))
    result['silver_records'] = records
    result['metrics'] = {'input_records': len(records), 'candidate_pairs': len(pairs),
                         'automatic_pairs': sum(p['initial_route'] == 'AUTO' for p in pairs),
                         'initial_review_pairs': sum(p['initial_route'] == 'REVIEW' for p in pairs),
                         'conflicting_pairs': sum(p['id_conflict'] for p in pairs),
                         'approved_review_pairs': sum(p['route'] == 'APPROVED' for p in result['pairs']),
                         'published_entities': len(result['gold_customers']),
                         'published_source_links': len(result['gold_source_links']),
                         'held_records': len(result['held_source_keys'])}
    return result


def load_inputs(folder):
    folder = Path(folder)
    rows = []
    for source, name in [('CRM', 'crm.csv'), ('ERP', 'erp.csv')]:
        with (folder / name).open(newline='') as f:
            rows.extend(dict(r, source=source, batch_id='B001', ingested_at='2026-10-08T09:00:00Z') for r in csv.DictReader(f))
    rows.extend(dict(r, source='PORTAL', batch_id='B001', ingested_at='2026-10-08T09:00:00Z') for r in json.loads((folder / 'portal.json').read_text()))
    return rows


def upsert_snapshot(history, incoming):
    snapshots = {(r['source'], r['record_id'], r['batch_id']): dict(r) for r in history}
    for r in incoming:
        key = (r['source'], r['record_id'], r['batch_id'])
        if key in snapshots and snapshots[key] != r:
            raise ValueError('A batch/source key cannot be reused for different evidence')
        snapshots[key] = dict(r)
    return list(snapshots.values())


def latest_snapshot(history):
    out = {}
    for r in sorted(history, key=lambda r: (r['source_updated_at'], r['batch_id'])):
        out[(r['source'], r['record_id'])] = r
    return list(out.values())


def checks(rows, reviews):
    result = evaluate(rows, reviews)
    assert result['metrics'] == dict(input_records=9, candidate_pairs=7, automatic_pairs=3,
        initial_review_pairs=3, conflicting_pairs=1, approved_review_pairs=1,
        published_entities=5, published_source_links=8, held_records=1)
    assert result['held_source_keys'] == ['PORTAL:P902']
    aurora = next(p for p in result['pairs'] if p['pair_key'] == 'CRM:C102|ERP:E502')
    assert aurora['score'] == 100 and aurora['route'] == 'REJECT'
    a = normalise(dict(rows[0], business_id=''))
    b = normalise(dict(rows[0], source='ERP', record_id='TEST', business_id=''))
    assert not score_pair(a, b)['exact_id']  # two missing identifiers are not evidence
    assert usable_id('BAD-ID') == '' and usable_id('DEMO-001') == 'DEMO-001'
    stale = [dict(r, evidence_fingerprint='stale') for r in reviews]
    assert evaluate(rows, stale)['metrics']['approved_review_pairs'] == 0
    # A-B and B-C cannot bypass an A-C identifier contradiction.
    bridge = [normalise(dict(rows[0], source='CRM', record_id='A', business_id='DEMO-001')),
              normalise(dict(rows[0], source='ERP', record_id='B', business_id='')),
              normalise(dict(rows[0], source='PORTAL', record_id='C', business_id='DEMO-009'))]
    edges = [dict(score_pair(bridge[0], bridge[1]), route='APPROVED'),
             dict(score_pair(bridge[1], bridge[2]), route='APPROVED')]
    guarded = consolidate(bridge, edges)
    assert any(p['route'] == 'GROUP_CONFLICT' for p in guarded['pairs'])
    history = upsert_snapshot([], rows)
    assert len(upsert_snapshot(history, rows)) == 9
    changed = dict(next(r for r in rows if r['source'] == 'ERP' and r['record_id'] == 'E501'),
                   address='Roma Street 14', source_updated_at='2026-10-09T08:00:00Z',
                   batch_id='B002', ingested_at='2026-10-09T09:00:00Z')
    history = upsert_snapshot(history, [changed])
    after = evaluate(latest_snapshot(history), reviews)
    before_id = next(r['customer_id'] for r in result['gold_customers'] if r['business_id'] == 'DEMO-001')
    after_alfa = next(r for r in after['gold_customers'] if r['business_id'] == 'DEMO-001')
    assert after_alfa['customer_id'] == before_id and after_alfa['billing_address'] == 'Roma Street 14'
    assert len(upsert_snapshot(history, [changed])) == 10
    return result, after


def main():
    base = Path(__file__).parent
    rows = load_inputs(base / 'datasets')
    reviews = list(csv.DictReader((base / 'datasets/review_decisions.csv').open(newline='')))
    before, after = checks(rows, reviews)
    out = base / 'expected'
    out.mkdir(exist_ok=True)
    for name, data in [('B001', before), ('B002', after)]:
        (out / (name + '_results.json')).write_text(json.dumps(data, indent=2))
    print(json.dumps(before['metrics'], indent=2))
    print('Checks passed: routing, null IDs, conflict override, stale review, group guard, rerun and update.')

if __name__ == '__main__':
    main()
