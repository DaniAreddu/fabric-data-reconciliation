# Asset and data sources

This file records where each dataset, piece of evidence and image comes from, what may be reused, and how it was changed. License terms per path are summarised in [LICENSES.md](LICENSES.md).

## What comes from the real project

The examples start from a real project for the Municipality of Messina. Daniele Mario Areddu worked on it; the facts below are his account of the project:

- street-name (odonym) reconciliation and territorial data management;
- end-to-end architecture and full-stack development;
- five to six sources;
- reading references from Maggioli and returning validated links to Maggioli;
- Python/FastAPI, React/TypeScript, PostgreSQL/PostGIS and trigram search;
- normalisation, matching, reconciliation and deduplication;
- ETL, APIs, Docker, deployment and production stabilisation.

SIMEL is the municipal information system in the Maggioli context. The supplier and its product are one operational node, not two sources. The materials do not establish which SIMEL release Messina uses. An official procurement record of the Autorità di Sistema Portuale del Mare di Sicilia Orientale names SIMEL2 and Maggioli services; it concerns another authority and says nothing about the Messina version, contract or topology.

Everything else about Messina in this repository is a teaching reconstruction:

- **Reference feed topology.** The diagram's other feeds (street register and toponymy, municipal public addresses, SITR/Geoportale Sicilia, cadastral extracts, office CSV/Excel exports) make the architecture concrete. They are not a statement that each one was integrated in the original project.
- **Proposed patterns.** Confirmation that the destination applied an update, safe retry, idempotency and richer decision/audit states are integration patterns proposed in the slides and in [docs/messina.md](docs/messina.md). They are not described as part of the original implementation.
- **Example records.** `MAG:ODN:000184`, `TOP:STR:000531`, `OFF:ROW:000009`, `CIV:ADR:012784` and their fields are invented namespaces and schemas. They are not SIMEL API contracts or project exports. Via Adolfo Celi exists in the municipal register; the abbreviated "A. Celi Street" and the "Adolfo Celi Square" variant illustrate disagreement. The materials do not claim that a Piazza Adolfo Celi exists, and the register checked on 10 October 2026 contains none.
- **Impact scenarios.** Misdirected letters or fine notices, delayed services, unusable address links, wrong territorial context, altered counts and manual rework are possible consequences of bad links. They are not documented incidents, and the materials do not claim the platform operated those services.

## Evidence references

`ONB-DELTA-42` and `REF-CELI-01` are illustrative evidence references written for the examples. Neither is a production document. `datasets/teaching_evidence.json` states what each one asserts and what it does not support:

- `ONB-DELTA-42` associates `CRM:C103` with company `DEMO-003`, which `ERP:E503` already carries. It supports that pair only. It says nothing about `PORTAL:P902`.
- `REF-CELI-01` associates `MAG:ODN:000184` with `TOP:STR:000531` as the same registered street. Its scope is `STREET_LINK_ONLY`: it is not evidence for merging civic addresses and not a SIMEL integration contract.

## Customer fixture

The nine CRM, ERP and portal rows, the B002 update, the review decision and the pair labels describe invented companies (Alfa, Aurora, Delta, Nova) with English names and addresses. `DEMO-` identifiers are stipulated reliable company IDs for the exercise, not real registration numbers. The saved review fingerprint and the expected results correspond to these records under rule version `recon-demo-v2-en`.

## Public data

| Field | Value |
|---|---|
| Files | `datasets/messina_public_sample.csv`; the `id`, `official_street_name` and `civic` columns of `datasets/messina_display_labels.csv` |
| Publisher | Comune di Messina |
| Dataset | [Indirizzario del Comune di Messina](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194) ([CSV](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194/resource/fce8cc08-6654-4c00-bf94-e3157d5da534/download/indirizzario.csv), [national catalogue entry](https://www.dati.gov.it/node/view-dataset/dataset?id=68adbea8-8e6d-486d-8804-d8782c2bbe3c)) |
| License | CC BY 4.0. The dataset page adds an addendum for OpenStreetMap: attribution through the OSM contributors page satisfies the attribution requirement, and the municipality waives clause 2(a)(5)(B) for reuse by OpenStreetMap and its users |
| Use | Slides 7 and 9 and the Messina examples in [docs/messina.md](docs/messina.md) |
| Changes | None. Four rows (Viale Boccetta 63 and 65, Via Adolfo Celi 251 and 253) copied with original header, values and CRLF line endings. On 10 October 2026 all four rows matched the published CSV exactly |

The slides show English display names (Boccetta Avenue, Adolfo Celi Street) and shortened UUIDs. Those translations live only in `messina_display_labels.csv`, next to the official names; the public sample is never edited to look English. Coordinates stay in the CSV and are not presented as surveyed entrance positions.

On slide 9, address IDs `019e5e6c-85d2-7c04-9a36-83f3168ca0a0` (Viale Boccetta, civic 63) and `019e5e66-65b4-783a-9192-2f37fbc19e9f` (same street, civic 65) keep their own identities. Sharing a street does not establish a street link or an address merge.

Other public sources used for context, not data:

- [Municipality of Messina, territorial and urban services department](https://www.comune.messina.it/it/unita_organizzative/dipartimento-servizi-territoriali-ed-urbanistici): street register, toponymy and SITR responsibilities. Supports the feed labels in the reference architecture.
- [SITR, Regione Siciliana](https://www.sitr.regione.sicilia.it/): the regional territorial information system, named on slide 6 as a reference source. No screenshot or connection is claimed.
- [Procurement record naming SIMEL2 and Maggioli services](https://trasparenza.adspmaresiciliaorientale.it/appalti-190/detail.aspx?app=799&tp1=40): supports the product name and its English expansion ("Multichannel Information System for Local Authorities") only.

## Images

| File | Author or owner | Source | License | Use | Changes |
|---|---|---|---|---|---|
| `assets/messina.jpg` | Jeroen P | [Wikimedia Commons: Messina_Strait.jpg](https://commons.wikimedia.org/wiki/File:Messina_Strait.jpg) | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | Slide 5; [docs/messina.md](docs/messina.md) | File unchanged; cropped on the slide, with attribution |
| `assets/microsoft-learn/lakehouse-official.png` | Microsoft | [Load data into your lakehouse with a notebook](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data); [original image](https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-engineering/media/lakehouse-notebook-explore/load-data-menu.png) | CC BY 4.0 (MicrosoftDocs/fabric-docs); no trademark rights | Slide 19; [docs/fabric-setup.md](docs/fabric-setup.md) | File unchanged; the slide crops it to the explorer with Files and Tables. Its sample table names are Microsoft's, not ours |
| `assets/microsoft-learn/pipeline-settings-official.png` | Microsoft | [Notebook activity](https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity); [original image](https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-factory/media/notebook-activity/notebook-connection-workspace-parameters.png) | CC BY 4.0 (MicrosoftDocs/fabric-docs); no trademark rights | Slide 20; [docs/fabric-setup.md](docs/fabric-setup.md) | File unchanged; the slide crops it around the Notebook activity settings. It does not show a pipeline built for this repository |
| `assets/fabric-icons/*.svg` (Lakehouse, Notebook, OneLake, Pipeline, Semantic model) | Microsoft | [Fabric icons](https://learn.microsoft.com/en-us/fabric/fundamentals/icons), [Icons.zip](https://github.com/microsoft/fabric-samples/blob/main/docs-samples/Icons.zip) | MIT, `assets/fabric-icons/LICENSE.txt` | Slides 18 and 34, with names beside each icon | Unchanged colours and proportions |

The Microsoft images are authentic documentation screenshots. They explain where things are in the Fabric interface; none of them shows this notebook running.

The slides PDF embeds subsets of Noto Sans (Google, SIL Open Font License 1.1).

## Original visuals in the slides

Drawn by Daniele Mario Areddu and covered by CC BY 4.0:

- the operator comparison on slide 11, a reconstructed view with invented keys and states, not a screenshot of a production application;
- the Bronze, review and Gold tables on slides 19, 31 and 34, built from the local reference results (table names omit the `recon_demo_` prefix for readability);
- the outcome table on slide 36, from `expected/B001_results.json`;
- the production comparison on slide 37 and the takeaways on slide 38;
- the four chapter dividers and all diagrams and arrows.

## Elements not licensed here

These appear in the slides PDF and are not extracted into `assets/`:

| Element | Origin | Status |
|---|---|---|
| Portrait, contact icons and LinkedIn QR code (slides 2 and 40) | Daniele Mario Areddu's slides for Day of Data Toronto 2026 | The QR code opens Daniele Mario Areddu's LinkedIn profile, not this repository |
| Data Saturdays logo, dark background and green accents | Data Saturdays Sofia 2026 template | Event identity, used as provided by the organisers |

## Status of the materials

The local reference (`reference.py`) and its tests pass and produce the versioned files in `expected/`. Every notebook code cell compiles. The notebook has not been run in a Fabric workspace for this repository; no slide or image is presented as output of such a run. No live CRM, ERP or portal connection, provisioned pipeline, review application or production identity registry is included.
