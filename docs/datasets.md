# Datasets

Everything in [`datasets/`](../datasets) is small enough to read in a minute. Most of it is invented for the exercise; one file holds four unmodified rows of public municipal data. Full provenance and licenses are in [asset_sources.md](../asset_sources.md) and [LICENSES.md](../LICENSES.md).

| File | Origin | Read by |
|---|---|---|
| `crm.csv`, `erp.csv`, `portal.json` | Invented company fixture | reference, notebook |
| `erp_B002.csv` | Invented update for batch B002 | reference tests, notebook |
| `review_decisions.csv` | Invented review decision | reference, notebook |
| `labelled_pairs.csv` | Invented pair labels | tests, notebook |
| `teaching_evidence.json` | Description of the two illustrative evidence references | people (no code reads it) |
| `group_check_example.csv` | Separate A–B–C example | tests |
| `messina_public_sample.csv` | Comune di Messina open data, unmodified | tests |
| `messina_display_labels.csv` | English display names for the public rows | tests |
| `messina_example_records.csv`, `messina_review_decisions.csv` | Invented street-link example | tests |

The Messina files and the A–B–C example are separate illustrations. They are not extra rows of the customer data and the notebook does not ingest them.

## Company extracts

`crm.csv`, `erp.csv` and `portal.json` share one set of fields:

| Field | Meaning |
|---|---|
| `record_id` | Local key inside its source (C101, E501, P901). Combined with the source name it becomes the source key `CRM:C101` |
| `company_name` | Name as the source holds it |
| `business_id` | Company identifier claimed by the source. Empty when missing. `DEMO-` plus three digits is treated as a reliable company ID in this exercise |
| `address`, `postcode`, `city` | As held by the source; `address` is a billing address in the ERP |
| `source_updated_at` | When the source changed the row (UTC) |

The loader adds `source`, `batch_id` and `ingested_at`. The source name does not come from the file contents: it is assigned by which file the row came from.

`portal.json` stands for the response of a portal API saved to a file. Nothing in this repository connects to a live portal, CRM or ERP.

| Source key | `company_name` | `business_id` | `address` | `postcode` |
|---|---|---|---|---|
| `CRM:C101` | Alfa Ltd | DEMO-001 | Roma Street 12 | 98100 |
| `CRM:C102` | Aurora Consulting | DEMO-002 | Verdi Street 8 | 98121 |
| `CRM:C103` | Delta Services | | Port Street 5 | 98122 |
| `CRM:C104` | Nova Travel | | Milan Street 4 | 00100 |
| `ERP:E501` | ALFA LTD | DEMO-001 | Roma St., 12 | 98100 |
| `ERP:E502` | Aurora Consulting | DEMO-009 | Verdi Street 8 | 98121 |
| `ERP:E503` | Delta Services | DEMO-003 | Port Street 5 | 98122 |
| `PORTAL:P901` | Alfa | DEMO-001 | Roma Street 10 | 98100 |
| `PORTAL:P902` | Delta Service | | Port Street 5 | 98122 |

Cities are Messina except Nova (Rome). The rows form batch B001.

## Batch B002

`erp_B002.csv` has the same fields and one row: `ERP:E501` with address `Roma Street 14` and `source_updated_at` `2026-10-09T08:00:00Z`. Every other field matches the B001 row. The notebook ingests it as batch B002; the reference tests load the same file and check that it matches the update the reference uses.

After B002 there are ten stored snapshots and nine current rows. The latest snapshot per source key is chosen by `source_updated_at`, then batch. Load time alone does not decide which value is newer.

## Review decisions

`review_decisions.csv` holds one decision per pair: `pair_key`, `decision` (`APPROVE` or `REJECT`), `reviewer`, `reviewed_at`, `evidence_reference`, `rule_version` and `evidence_fingerprint`. The only row approves `CRM:C103|ERP:E503` with `ONB-DELTA-42` under `recon-demo-v2-en`. Pair keys put the two source keys in sorted order.

The fingerprint must match the current records. If you edit any compared field of C103 or E503 (name, ID, address, postcode, city), the approval becomes stale and the pair returns to review, which is what should happen. See [How the decisions are made](reconciliation.md#a-review-that-can-be-reused).

## Pair labels

`labelled_pairs.csv` labels seven pairs: four `MATCH` (three Alfa pairs and Delta CRM–ERP), one `DIFFERENT` (Aurora) and two `UNKNOWN` (both pairs with `PORTAL:P902`). `UNKNOWN` is a label of its own, not a missing value and not a negative. It stays out of precision and recall.

## Teaching evidence

`teaching_evidence.json` explains the two evidence references used in the examples, what each one asserts and what it is *not* evidence for. `ONB-DELTA-42` covers only the Delta CRM–ERP pair. `REF-CELI-01` covers only a street link between `MAG:ODN:000184` and `TOP:STR:000531`, not a merge of civic addresses. Neither is a document from a real project.

## A–B–C group example

`group_check_example.csv` lists three nodes (`CRM:A` with DEMO-002, `ERP:B` with no ID, `PORTAL:C` with DEMO-009) and the proposed links A→B→C. The tests use it to show that a missing middle ID cannot join two contradictory IDs.

## Messina files

`messina_public_sample.csv` contains four rows from the municipality's [address register](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194) with their original Italian header and values: `id`, `odonimo` (street name), `civico` (civic number), `esponente` (number suffix), `lat`, `long` (WGS84 degrees) and `data_rilevazione` (survey time). An odonym is the name of a street or other circulation area. The file is kept byte for byte as published (CC BY 4.0, Comune di Messina).

`messina_display_labels.csv` maps each public `id` to its `official_street_name` and an `english_display_name` (`VIALE BOCCETTA` → Boccetta Avenue, `VIA ADOLFO CELI` → Adolfo Celi Street). Slides and documents use the English labels; the source file stays as published.

`messina_example_records.csv` and `messina_review_decisions.csv` describe the street-link example from the talk with invented keys: `MAG:ODN:000184` (A. Celi Street, the operational row), `TOP:STR:000531` (Adolfo Celi Street, the street register row) and `OFF:ROW:000009` (Adolfo Celi Square, a type conflict). The review approves only the street link, with status `VALIDATED_LOCAL_TARGET_PENDING`: validated locally, not yet confirmed by the receiving system. See [The Messina project](messina.md).

## Changing the data

Any change to the company extracts can change candidates, scores, fingerprints and the expected outputs together. [CONTRIBUTING.md](../CONTRIBUTING.md) describes how to make such a change deliberately and verify it.
