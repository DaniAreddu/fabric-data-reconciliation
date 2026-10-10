# Licenses

This repository mixes code, writing, data and third-party assets, so one license does not cover everything. The table below says which terms apply to each path. Where a third-party license applies, it takes precedence over the repository licenses for that item.

Nothing here licenses source code, data or documents from the Municipality of Messina project described in the talk. None of that material is included.

## Original work by Daniele Mario Areddu

| Terms | Paths |
|---|---|
| MIT ([LICENSE](LICENSE)) | `reference.py`; the **code cells** of `fabric_reconciliation.ipynb`; `tests/`; `scripts/`; `.github/`; code blocks quoted in the documentation; the synthetic fixtures `datasets/crm.csv`, `erp.csv`, `erp_B002.csv`, `portal.json`, `review_decisions.csv`, `labelled_pairs.csv`, `group_check_example.csv`, `messina_example_records.csv`, `messina_review_decisions.csv` and `teaching_evidence.json`; the generated results in `expected/` |
| CC BY 4.0 ([LICENSE-DOCS](LICENSE-DOCS)) | `README.md`, `CONTRIBUTING.md`, `LICENSES.md`, `asset_sources.md`; `docs/`, including the diagram sources in `docs/diagrams/`; the **Markdown cells** of `fabric_reconciliation.ipynb`; `talks/`; `presentations/reconciliation_checklist.pdf`; the `english_display_name` column of `datasets/messina_display_labels.csv`; the original text, tables and native diagrams of the decks in `presentations/` |

The synthetic fixtures are under MIT so that they can travel with the code they test. They describe invented companies and illustrative street-link records, not exports from a real system.

If you reuse the CC BY 4.0 material, a credit such as this is enough: *"When Enterprise Data Disagrees: Reconciliation Patterns in Microsoft Fabric" by Daniele Mario Areddu, CC BY 4.0*, with a link to this repository and a note of any changes.

## Third-party material

| Item | Owner | Terms | Notes |
|---|---|---|---|
| `datasets/messina_public_sample.csv`; the `id`, `official_street_name` and `civic` columns of `datasets/messina_display_labels.csv` | Comune di Messina, *Indirizzario del Comune di Messina* | CC BY 4.0, with the municipality's published addendum for reuse by OpenStreetMap | Four rows copied without changes. See [asset_sources.md](asset_sources.md#public-data) |
| `assets/messina.jpg` (and its crop on deck slide 5) | Jeroen P, Wikimedia Commons | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | Original file; the deck uses a crop |
| `assets/microsoft-learn/*.png` (and their crops on deck slides 19–20) | Microsoft, MicrosoftDocs/fabric-docs | CC BY 4.0 for the documentation content | The license grants no rights to Microsoft names, logos or trademarks |
| `assets/fabric-icons/*.svg` (used on deck slides 18 and 34) | Microsoft | MIT, see [assets/fabric-icons/LICENSE.txt](assets/fabric-icons/LICENSE.txt) | Unmodified icon files from the official package |
| `fonts/*.ttf` (embedded in the PDF decks) | Adobe, Source Sans Pro | SIL Open Font License 1.1, see [fonts/LICENSE.md](fonts/LICENSE.md) | Unmodified; "Source" is a reserved font name |

## Not licensed by this repository

The decks also contain elements that are neither MIT nor CC BY 4.0. They are distributed inside the decks only so the presentation stays complete, and remain under their owners' rights:

- the speaker portrait and the LinkedIn QR code on slides 2 and 40;
- the GitHub, LinkedIn, Instagram and other contact icons, which are trademarks of their owners;
- the Data Saturdays Sofia logo and the event's visual identity from its speaker template;
- Microsoft, Fabric, Power BI and other product names and logos.

These files are deliberately not extracted into `assets/`. If you adapt the decks, replace or remove them unless you have the owners' permission.
