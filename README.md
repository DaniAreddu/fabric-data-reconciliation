# fabric-data-reconciliation

Materials for Daniele Mario Areddu's session at Data Saturday Sofia 2026, *When Enterprise Data Disagrees: Reconciliation Patterns in Microsoft Fabric*. The example reconciles customer records from CRM, ERP and a portal extract. It keeps source keys, records review decisions and publishes linked records with field provenance.

## Contents

```text
reference.py                  matching rules and checks, Python standard library only
fabric_reconciliation.ipynb   the same rules in PySpark for a Fabric Lakehouse
datasets/                     CRM, ERP and portal extracts, B002 update, review decision,
                              pair labels, Messina street-link examples
expected/                     B001 and B002 results produced by reference.py
tests/                        unit tests for the rules, the notebook and the data files
scripts/check_repo.py         link, file and diagram checks
docs/                         rules, datasets, Fabric setup, production limits, Messina project
slides/                       slides PDF
```

`datasets/portal.json` is a saved API response. Nothing in the repository connects to a live system.

## Run

Python 3.10 or later, no dependencies:

```bash
git clone https://github.com/DaniAreddu/fabric-data-reconciliation.git
cd fabric-data-reconciliation
python reference.py
python -m unittest discover -s tests
python scripts/check_repo.py
```

`reference.py` runs the rule checks, writes the B001 and B002 results to `output/` and exits with an error if they differ from `expected/`. The last lines of a good run:

```text
Checks passed: routing, null IDs, conflict override, stale review, group guard, rerun and update.
Generated B001 and B002 results match expected/ (written to output).
```

## Results

Batch B001 has nine source rows: four CRM, three ERP, two portal.

| Outcome | Count |
|---|---:|
| Cross-source pairs | 26 |
| Candidate pairs after blocking | 7 |
| Linked by a shared company ID | 3 |
| Sent to review | 3 |
| Rejected by an ID conflict | 1 |
| Approved in review | 1 |
| Published companies | 5 |
| Published source links | 8 |
| Held source rows | 1 |

- Aurora: `CRM:C102` and `ERP:E502` have the same name, address and postcode and score 100, but carry DEMO-002 and DEMO-009. They stay two companies.
- Alfa: `CRM:C101`, `ERP:E501` and `PORTAL:P901` share DEMO-001. The portal pairs score 45 and are still linked.
- Delta: `CRM:C103` has no company ID. Its pair with `ERP:E503` is approved in review with evidence `ONB-DELTA-42`. `PORTAL:P902` has no evidence of its own and is held.

Batch B002 changes the billing address of `ERP:E501` to Roma Street 14. Alfa keeps its customer ID (`CUS-a60635aa3160`) after the address update; Bronze holds ten snapshots and five companies are published.

These counts show that the rules behave as written on this fixture. They are not an accuracy measurement. The rule order, scoring, review reuse and grouping are explained in [docs/reconciliation.md](docs/reconciliation.md); the input files in [docs/datasets.md](docs/datasets.md).

## Fabric

Create a Lakehouse used only for this example, upload `datasets/` to `Files/reconciliation_demo/datasets`, import the notebook, attach the Lakehouse as default and run the sections in order. The notebook writes `recon_demo_*` tables and asserts the same B001 and B002 counts as `reference.py`. Step-by-step instructions, the tables each section writes and troubleshooting: [docs/fabric-setup.md](docs/fabric-setup.md).

The tests check that the notebook is valid, that every code cell compiles and that its rules are identical to `reference.py`. The notebook has not been run in a Fabric workspace for this repository; the expected results come from `reference.py`.

What changes for real data volumes is listed in [docs/production.md](docs/production.md).

## Messina

The rules come from a street-name reconciliation project for the Municipality of Messina. [docs/messina.md](docs/messina.md) separates the project facts from the illustrative records used in the examples. No project code or data is included.

## Slides

[When_Enterprise_Data_Disagrees_Sofia_2026.pdf](slides/When_Enterprise_Data_Disagrees_Sofia_2026.pdf)

## License

Code and synthetic data: MIT, see [LICENSE](LICENSE). Documentation and slide text: CC BY 4.0, see [LICENSE-DOCS](LICENSE-DOCS). The Messina public data, photographs, Microsoft documentation images, icons and the parts of the slides that are not covered by these licenses are listed in [LICENSES.md](LICENSES.md). Data and image sources: [asset_sources.md](asset_sources.md).

Daniele Mario Areddu — Global Technologies Italia
