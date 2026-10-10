# Validation report

What was checked before publishing v1.0.0, with the commands used and their results. Checks that were not possible are listed as such.

## Starting materials

The repository was assembled from the final English session pack, `Sofia_2026_English_Materials.zip` (SHA-256 `acd39494423cc070b73d8c23ac6711fd6f46c0c11d1b3ad9284f5e62e0e04ae4`), and the Extended deck files. The ZIP was listed before extraction, extracted into an empty folder with a check that rejects absolute paths, `..` components and links, and every extracted file was hashed.

| File | SHA-256 | Notes |
|---|---|---|
| `Sofia_2026_English_Extended_Final.pptx` | `a14a8d8be9ca9a2149b7233d3ec8ebbf3bf6f4daf692c0d13659469910ccea88` | Matches the hash in the pack's own verification record |
| `Sofia_2026_English_Extended_Final.pdf` | `60021e669da7a23eb654999461c3f6314ac0a0f4c1d58ad3f759762871eb7e9b` | See below |
| `Sofia_2026_English_50min_Speech.md` | `d7a1e46d9ef32bf47a5170c2c3b99c2c0a17dc029ad8eb85fc2a744af63093cb` | From the ZIP, unchanged |
| `Sofia_2026_English_50min_Timing.md` | `497eac37b02dbf7ebe8f9ecdb8f98ffec1816e4c89b79a606d699128702b15e0` | From the ZIP, unchanged |
| `Sofia_2026_English_Extended_Speech.md` | `503fdeee788e9c5df3f2ee10234bf17b3becca0d29775d8b44d375bd92ebcd50` | From the ZIP, unchanged |
| `Sofia_2026_English_Extended_Timing.md` | `e2c45c72abe05cb8ce3affd0149e2de9d3fed9ecd94b1fe3804578e8640b85d9` | From the ZIP, unchanged |

All dataset files, the expected results, the checklist, the Messina photograph, the Microsoft images, the icons and the fonts are byte-identical to the ZIP. Text files are stored with LF line endings except the dataset CSVs, which keep their original CRLF bytes.

**Not available:** `Sofia_2026_English_50min_Final.pptx` and `Sofia_2026_English_50min_Final.pdf` were not among the files provided for publication, and no file matching the hashes recorded for them in the pack's verification record was found. They are not included, and no substitute was generated. `Sofia_2026_English_Revision.md` was also not provided; the pack's `revision_summary.md` was read in its place.

**Extended PDF:** its hash differs from the one in the pack's verification record (`8454ff99…`). The file provided is a LibreOffice export created on 10 October 2026 with 40 pages. It carries a C2PA Content Credentials manifest as an embedded file, signed at 08:21 UTC that day, after the verification record was written; the manifest records that the file was produced with ChatGPT. The manifest was inspected and contains no personal data or local paths, and it was left in place. The text of every slide's text boxes in the PPTX was found on the corresponding PDF page. The pixel comparison described in the pack's record was not repeated, because no renderer was available.

**Not published from the pack:** `speaker_notes.md`, `speaker_notes_50min.md`, `speaker_notes_extended.md`, `timing_50min.md` and `timing_extended.md` are byte-identical duplicates of the speech and timing files kept in `talks/`. `slide_results.json` duplicates `expected/B001_results.json`. `GITHUB_READY.md`, `revision_summary.md`, `run_sheet.md`, `slide_audit.csv` and `verification_*.json` are preparation records. The pack's `README.md` was replaced by the documentation in this repository. The portrait, contact icons, QR code and event logo images are not licensed for redistribution here (they remain inside the decks). The OpenStreetMap tile is no longer used in the deck.

## Corrections made while preparing the repository

- `reference.py` wrote its JSON with the platform's line endings, so on Windows the regenerated files differed byte for byte from the versioned ones while their content was identical. It now writes LF, writes to `output/` by default, compares with `expected/` and exits with an error on any difference. Rewriting `expected/` requires `--output-dir expected`. The functions shared with the notebook did not change, and neither did any result.
- Two Markdown cells of the notebook had no cell `id`, which nbformat 4.5 requires. Ids were added, and the Markdown cells were updated to point to `expected/` instead of the unpublished `slide_results.json`. Code cells are unchanged.

## Local checks

Run on Windows 11 from the repository folder.

| Command | Python | Result |
|---|---|---|
| `python reference.py` | 3.10.20, 3.11.15, 3.12.13, 3.13.14, 3.14.6 | Checks passed; generated B001 and B002 results match `expected/` byte for byte |
| `python -m unittest discover -s tests` | same five versions | 53 tests, OK |
| `python scripts/check_repo.py` | same five versions | 0 problems |

The tests cover English normalisation with preserved originals; missing, malformed and conflicting IDs; 26 possible pairs and 7 candidates, with an included and an excluded pair; Aurora's conflict priority, including an ignored approval; the Delta review scope and `PORTAL:P902` being held; stale approvals after a field, rule-version or evidence change; the A–B–C group guard and a recorded rejection; Gold value provenance and the billing fallback; idempotent snapshots and the B002 update; a full byte-for-byte comparison with `expected/`; a deliberately altered expected file that must make `reference.py` fail without being overwritten; the notebook's structure, compilation, embedded rules, table prefix and B001 assertions; speech word counts, timing arithmetic, PPTX notes against the Extended speech, 40 PDF pages; and the Messina display-label mapping.

`scripts/check_repo.py` was also run against a deliberately broken file and reported the broken link, missing image, missing anchor, user path and credential-like assignment.

## Consistency of the published facts

- B001: 9 records (4 CRM, 3 ERP, 2 portal), 26 possible pairs, 7 candidates, 3 automatic, 3 initially in review, 1 ID conflict, 1 approved review, 5 companies, 8 source links, 1 held record (`PORTAL:P902`).
- Aurora scores 100 with DEMO-002 against DEMO-009 and is rejected. Delta Services against Delta Service scores 95.714286. `Roma St., 12` normalises to `roma street 12`. Rule version `recon-demo-v2-en`; the saved Delta fingerprint matches the current records.
- B002: ten Bronze snapshots, nine current rows, five companies; Alfa keeps `CUS-a60635aa3160` and publishes `Roma Street 14`.
- The four rows of `messina_public_sample.csv` were compared with the municipality's published CSV on 10 October 2026 and match exactly.
- Speech words before Q&A: 3,678 (50-minute) and 4,484 (Extended), giving 33:26 and 40:46 of speech and 49:52 and 57:12 in total at 110 words per minute. The Extended PPTX notes are identical to the Extended speech, and no slide note contains a URL or a source line.

## External links

`python scripts/check_repo.py --external` requested the 33 external links in the documentation. 30 answered with HTTP 200. The other three:

- the CI badge returned 404 because the repository did not exist yet at the time of the check;
- `github.com/microsoft/fabric-samples/blob/main/docs-samples/Icons.zip` returned 503; the file exists (30,368,623 bytes, checked through the GitHub API), and the page times out for large binaries;
- the LinkedIn profile returned 999, LinkedIn's usual answer to automated requests.

## Not verified

- No run of the notebook in a Fabric workspace, and no Fabric screenshots or outputs.
- No rendering of the decks in PowerPoint and no new pixel comparison; no decoding of the LinkedIn QR code.
- No timed rehearsal of either speech.
- The 50-minute deck files, which are not included.
