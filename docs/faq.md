# Questions

**Is reconciliation a Fabric feature I can switch on?**
No. Fabric stores the data and runs the notebook; the decisions about which records describe the same company are rules you write and own. The notebook is one way to implement them.

**Why not merge records whose score is high?**
Because Aurora scores 100 and is two companies. A score counts agreeing fields. It cannot see the evidence that contradicts a link, which is why the ID conflict is checked first.

**Why does Alfa link with a score of 45?**
The portal row carries the same reliable ID, DEMO-001, as the CRM and ERP rows. In this exercise that ID is stipulated to be trustworthy, so it outweighs a shorter name and an older address. With IDs of unknown quality, that pair should go to review instead.

**Does a missing ID count against a match?**
No, and it does not count in favour either. Two empty IDs are two pieces of missing evidence. Treating them as equal would link every pair of rows without an ID.

**Why is PORTAL:P902 held if CRM and ERP Delta are linked?**
The review evidence, ONB-DELTA-42, is about `CRM:C103` and `ERP:E503`. It says nothing about the portal row. Approving the portal pairs would need their own evidence.

**Does the fingerprint prove the review is still right?**
It proves the compared values and the rule version have not changed since the review. It cannot tell whether the evidence itself was later withdrawn; a production flow needs a separate process for that.

**Why keep the portal's "Roma Street 10" if it is not published?**
It may be another site, an older address or an error. Bronze and Silver keep it with its source key, so someone can still check it. Gold publishes the billing address chosen by policy.

**Can I trust the format check on company IDs?**
Only as a format check. `DEMO-` plus three digits says the value is well-formed, not that it belongs to this company.

**What does "blocking" lose?**
Any true match that fails both filters: different or missing IDs, and a different postcode or name prefix. Such pairs are never scored. Measure how many true pairs your filter misses on a labelled sample.

**Are the B001 counts an accuracy result?**
No. They show the example follows its rules. Accuracy needs an independent labelled sample.

**Has the notebook been run in Fabric?**
Not for this repository. The local reference and its tests pass, and the notebook's cells compile and embed the same rules. See [the setup guide](fabric-setup.md) for the first run in your own workspace.

**Does portal.json connect to a portal?**
No. It is a saved API response used as an extract. The repository has no live connectors.

**Can I use the Messina address data?**
The four public rows are published by the Comune di Messina under CC BY 4.0; credit the municipality. See [LICENSES.md](../LICENSES.md). The other Messina records (`MAG:`, `TOP:`, `OFF:` keys) are invented for the talk.

**Where should I start with my own data?**
Pick two sources. Keep their original keys. Label a small set of pairs, including difficult negatives, before choosing matching rules.
