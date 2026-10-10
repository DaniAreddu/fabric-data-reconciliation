# Licenses

Different parts of the repository have different terms. Where a third-party license applies, it takes precedence over the repository licenses for that item.

Nothing here licenses source code, data or documents from the Municipality of Messina project. None of that material is included.

## Original work by Daniele Mario Areddu

| Terms | Paths |
|---|---|
| MIT ([LICENSE](LICENSE)) | `reference.py`; the code cells of `fabric_reconciliation.ipynb`; `tests/`; `scripts/`; `.github/`; code blocks in the documentation; the synthetic fixtures `datasets/crm.csv`, `erp.csv`, `erp_B002.csv`, `portal.json`, `review_decisions.csv`, `labelled_pairs.csv`, `group_check_example.csv`, `messina_example_records.csv`, `messina_review_decisions.csv` and `teaching_evidence.json`; the generated results in `expected/` |
| CC BY 4.0 ([LICENSE-DOCS](LICENSE-DOCS)) | `README.md`, `CONTRIBUTING.md`, `LICENSES.md`, `asset_sources.md`; `docs/`, including `docs/diagrams/` and `docs/reconciliation_checklist.pdf`; the Markdown cells of `fabric_reconciliation.ipynb`; the `english_display_name` column of `datasets/messina_display_labels.csv`; the original text, tables and diagrams of `slides/When_Enterprise_Data_Disagrees_Sofia_2026.pdf` |

The synthetic fixtures are MIT so they can be reused with the code that reads them. They describe invented companies and illustrative street-link records.

Credit for CC BY 4.0 material: *"When Enterprise Data Disagrees: Reconciliation Patterns in Microsoft Fabric" by Daniele Mario Areddu, CC BY 4.0*, with a link to this repository and a note of any changes.

## Third-party material

| Item | Owner | Terms | Notes |
|---|---|---|---|
| `datasets/messina_public_sample.csv`; the `id`, `official_street_name` and `civic` columns of `datasets/messina_display_labels.csv` | Comune di Messina, *Indirizzario del Comune di Messina* | CC BY 4.0, with the municipality's published addendum for reuse by OpenStreetMap | Four rows copied without changes. See [asset_sources.md](asset_sources.md#public-data) |
| `assets/messina.jpg` (cropped on slide 5) | Jeroen P, Wikimedia Commons | [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/) | |
| `assets/microsoft-learn/*.png` (cropped on slides 19 and 20) | Microsoft, MicrosoftDocs/fabric-docs | CC BY 4.0 for the documentation content | No rights to Microsoft names, logos or trademarks |
| `assets/fabric-icons/*.svg` (on slides 18 and 34) | Microsoft | MIT, see [assets/fabric-icons/LICENSE.txt](assets/fabric-icons/LICENSE.txt) | Unmodified files from the official icon package |
| Noto Sans, embedded as subsets in the slides PDF | Google | SIL Open Font License 1.1 | The OFL does not restrict documents that embed the font |

## Not licensed by this repository

The slides PDF also contains elements that are neither MIT nor CC BY 4.0 and remain under their owners' rights:

- the portrait and the LinkedIn QR code on slides 2 and 40;
- the GitHub, LinkedIn, Instagram and Sessionize icons on slide 40, which are trademarks of their owners;
- the Data Saturdays logo and the event's visual identity from the Data Saturdays Sofia 2026 template;
- Microsoft, Fabric, Power BI and other product names and logos.

If you adapt the slides, replace or remove these elements unless you have the owners' permission.
