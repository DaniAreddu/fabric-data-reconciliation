# Contributing

Corrections and questions are welcome. Keep the example small enough that every decision can be traced by hand.

## Run the checks

Python 3.10 or later, no packages to install:

```bash
python reference.py
python -m unittest discover -s tests
python scripts/check_repo.py
```

`reference.py` writes its results to `output/` and fails if they differ from the versioned files in `expected/`. The tests cover the decision rules, the notebook's structure, the slides PDF and the Messina data files. `check_repo.py` checks links, file hygiene and the diagram sources. CI runs the same three commands, also from an extracted `git archive` of the commit; none of them needs Fabric or any credential.

## Reporting a problem

Open an issue with:

- what you ran (local reference, tests, or the notebook in Fabric) and the Python or Fabric runtime version;
- the exact command or notebook section;
- what you expected and what you got. For a result difference, include the printed metrics or the pair keys and routes involved, not screenshots of data you are not allowed to share.

For a Fabric run, say whether the Lakehouse was new and whether B002 had been ingested before. Those two facts explain most differences ([troubleshooting](docs/fabric-setup.md#9-troubleshooting)).

## Changing a rule

A rule change usually moves several things at once. Make them move together, in one pull request:

1. **Start from a pair.** Describe the record pair that the current rules get wrong and the decision you expect. Add it to `datasets/labelled_pairs.csv` if it belongs to the company fixture, or as a test case if it is a separate illustration like the A–B–C example.
2. **Change `reference.py`.** If you change any function above `main()`, copy the same code into the notebook's rules cell (section 1); a test fails if the two differ. If the notebook's Spark code implements the same rule separately (normalisation in section 3, candidates and scoring in section 4, review routing in section 5), change it there too.
3. **Bump `RULE_VERSION`** whenever a change can alter a score, a route or a fingerprint. The saved Delta review then becomes stale, which is correct: recompute its fingerprint and update `datasets/review_decisions.csv` only if the evidence still supports the decision.
4. **Regenerate the expected results deliberately:**

   ```bash
   python reference.py --output-dir expected
   git diff expected/
   ```

   Read the diff. Every changed route, score, customer ID or Gold value should be explained in the pull request description.
5. **Update the tests and documentation** that state the old values: `tests/test_reference.py`, `docs/reconciliation.md`, `docs/datasets.md`, `docs/fabric-setup.md` and the README results table.

CI never rewrites `expected/`. A pull request whose output differs from the committed files fails until the new expected files are committed with an explanation.

The slides describe rule version `recon-demo-v2-en` and are not generated from this repository. If a rule change makes them out of date, say so in the pull request.

## Changing data

Do not edit `datasets/messina_public_sample.csv`. It is a byte-for-byte copy of public rows; translations belong in `messina_display_labels.csv`. Dataset CSV files are stored with their original CRLF line endings (see `.gitattributes`).

New example records must be invented, not copied from a real system, and should be described in `asset_sources.md`. Do not add personal data, customer data or anything from the Messina project.

## Documentation and diagrams

Diagram sources live in `docs/diagrams/*.mmd`. The same Mermaid code is embedded in the Markdown pages; `scripts/check_repo.py` fails if an embedded copy and its source differ, so edit both.

Documentation is English and should follow a record through a decision. If you add a claim about Fabric behaviour, link the Microsoft Learn page that supports it.

## Licensing of contributions

Code contributions are accepted under the MIT license and documentation under CC BY 4.0, as described in [LICENSES.md](LICENSES.md). Do not add third-party assets unless their license allows redistribution, and record them in `asset_sources.md`.
