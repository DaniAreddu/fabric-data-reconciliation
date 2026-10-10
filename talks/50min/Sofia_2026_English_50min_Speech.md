Hi everyone. Today we will follow records that describe the same thing in different ways. We start with addresses in Messina, then customers in Microsoft Fabric. We will decide which records to connect, what evidence we need, and how to handle an uncertain answer.

I'm Daniele Mario Areddu, a Backend and AI Developer at Global Technologies Italia and a Computer Science student at the University of Calabria. In Messina, I led the architecture, development and production delivery of a territorial data platform. That experience gives us our starting question.

What happens when the address exists in one system, but another system cannot find its street link? The office record says Adolfo Celi Street, number 253. Its street reference is missing. The other system says A. Celi Street. What would you check before using this address?

I would check which street the office record belongs to. The name helps us search. We still need evidence for the connection. A missing link does not tell us whether the physical address exists.

Reconciliation means we decide which records describe the same thing, and keep the evidence for that decision. We preserve the original rows and add a supported link that another process can use. Messina gives us the setting.

Let's start with a real project where I worked: a territorial data platform for the Municipality of Messina. The challenge was to connect records across five to six sources and make the validated links useful in the operational flow. We will follow that cycle from reading a reference to comparing it, reviewing the evidence and returning the validated link to Maggioli.

This is Messina, in Sicily. The platform brought together street names and territorial information. We built search, record links and an operator interface, using Python and FastAPI, React and TypeScript, and PostgreSQL with PostGIS. We read from Maggioli and returned validated links. Getting that loop to work in production required both data rules and reliable services.

Maggioli is the supplier. SIMEL is a municipal information system used by the local authority. We read its references and return validated links, so they appear as one operational node.

The other named feeds provide street codes, civic addresses, regional maps, property references and office corrections. One system can hold several datasets. A CSV is an extraction format, rather than another system. Counting every table as a separate system makes the diagram impressive and the meeting confusing. Follow the operational reference into the middle. The street register supplies another description of that object. The civic register adds addresses belonging to streets. The comparison creates a proposed link, and the return arrow carries a validated reference back. A property reference adds context, but a property and an address still need different keys.

A. Celi Street looks like an abbreviation of Adolfo Celi Street. That gives us a candidate: a pair worth checking. The third record says Adolfo Celi Square. Street and square describe different kinds of area. Removing that distinction could make two different objects look equal. We keep the name and area type as separate fields. The shorter name helps us find a candidate; the type helps us check whether it is the right kind of candidate. We still need evidence before approving the link.

Follow the letter. The records disagree, the link fails, and someone has to repair the case. A wrong link may send a letter or fine notice to the wrong destination. A missing link may delay a service. A territorial case may point to the wrong place, and duplicates may change maps or counts.

An operator then rebuilds references by hand. That can mean delays, complaints and possible payment collection difficulties. These are possible consequences, rather than documented Messina incidents or claims about the services our platform operated. A correction helps the next process only when the right system receives it.

Both records refer to Boccetta Avenue. One has civic number sixty-three, the other sixty-five. Their address IDs also differ. Follow the shared street reference down to the two address boxes. Each box keeps its own identity and civic number. Sharing a street does not make them the same address. Street, address and access point are different objects. For a street link, we check the street reference. For an address link, civic number and the local address identity also matter. Two entrances can serve one building. Even nearby points do not prove that the addresses are identical.

Searching A. Celi Street gives us Adolfo Celi Street as a candidate. PostgreSQL trigram search compares small groups of characters. FastAPI returns candidates and source references. PostGIS stores and queries geographic context.

Longitude and latitude use degrees. A distance rule may need metres. 

For a distance threshold, check the data type as well as the coordinate system. PostGIS geometry uses the units of its reference system. Geography distance uses metres. Geographic context can narrow our search. It still cannot prove the identity of a street or an address.

The names are close, and both records have the area type Street. That gives us a candidate. A checked reference table adds the evidence: it connects the Maggioli and street-register keys to the same street. We save that check as REF-CELI-01. The operator approves the street link and keeps its reason. Follow the two keys into the decision. MAG identifies the operational street row. TOP identifies the street-register row. The mapping supports those exact keys and that type of object. It does not approve a merge between two civic addresses. This narrow scope makes the decision easier to reuse and explain. The interface brings the evidence together, and FastAPI manages the connection. We have a validated local link, with one more step to complete.

The local platform has the validated link. The receiving system still shows it as missing, so the next process may use the old reference. We need to send the link and check whether the destination applied it.

Reading from and pushing to Maggioli were part of the project. Confirmation and safe retry here are proposed patterns that depend on the real contract. A successful send and a received update are different states. Keeping both visible shows where the process stopped.

If the destination rejects the update, the link remains locally validated but not confirmed there. A proposed retry must avoid creating duplicate effects. That requires a suitable destination contract.

Follow one reference around the loop. Acquisition keeps the source values. PostgreSQL and PostGIS hold records, geometry and indexes. FastAPI reads those records and returns search candidates. The path then reaches React and TypeScript, where the operator compares evidence. A validated link returns through the backend to Maggioli. ETL, Docker deployment and production support keep this operational loop working.

Now replace streets with customers. Different business, same problem. We still need supported decisions that reach the people using the result.

The municipal story ends with a link that another process can use. Replace the street with a company and the same questions return. We will follow Alfa through sales, billing and a portal, then compare what happens when evidence agrees, is missing or contradicts a link.

Alfa appears in three places. CRM means customer relationship management: our sales view. ERP means enterprise resource planning: our billing view. The portal arrives through an API, an interface for exchanging data.

The names differ. The portal address says ten; the other records say twelve. We are matching companies. Sites, contacts and accounts need their own identities.

Follow CRM C101, ERP E501 and portal P901. Those local IDs find source rows. The company ID makes a different claim about identity. We test that claim separately from name and address. All source keys remain when we publish one company. What happens if we choose badly?

One company staying split can leave support with only part of its history. Joining different companies can send an invoice to the wrong company. Those errors have different costs. The business process guides the evidence we require. More links alone do not prove improvement.

The business risk gives us a reason to keep decisions visible. Fabric gives us a place to store the rows and run our rules. Follow the same source key through the layers. Each step adds information, while the original record remains available.

Follow CRM C101 into Bronze, a Lakehouse in OneLake. Pipeline starts the notebook when the extracts are ready. That instruction follows the dashed arrow.

The notebook uses PySpark, Python running on Spark, to add comparison fields in Silver. C101 keeps its source key. Our rules then select Alfa pairs and check evidence. A candidate is a pair to check, not an approved link. Supported pairs continue along the solid path to Gold, with the company and source links.

Uncertain pairs take the lower review path. The operator records evidence and a decision. The return arrow brings that decision back to matching for validation. Pending answers stay outside trusted publication under our policy.

We centralised the data. The disagreement came with it. Reconciliation is our application logic. Fabric provides the storage and processing tools.

Files keeps the original extracts. Tables keeps source snapshots with their load context. A batch is one load. Alfa's received names remain unchanged. Source and batch information let us trace a decision back to those values.

Loading the same batch again avoids adding the same snapshot twice in our example.

B001 is the first batch. A snapshot is the version of a source row received in that load. We keep source, local ID and batch together. The same row can later appear in B002 without erasing B001. Source update time tells us when the source changed it. Load time tells us when we received it. Both help explain which version a decision used. A repeated batch with conflicting values is an error to investigate. The interface images show where files and tables are kept. Our source keys and batch values show how we preserve inputs before processing them.

We add Notebook activity and select the notebook. Extracts must be ready first. Pipeline coordinates the activity; the notebook runs our rules.

A completed activity means the work finished. Production also needs to check expected inputs and publication. Missing input can still give an incomplete result after technical success.

These screenshots show Microsoft documentation interfaces. The pack supplies a notebook and source extracts. Live connections would be configured separately; these images do not show a workspace execution. Let's check the comparison fields.

CRM C101 and ERP E501 keep their original names. We add a comparison field where case and punctuation follow the same rules. Both names now read alfa ltd. Our address rule expands St. to Street and removes punctuation, so Roma St., twelve and Roma Street twelve can be compared. This is normalisation: explicit rules make comparisons consistent. Portal P901 still has number ten. Cleaning preserves that meaningful difference. The comparison field sits beside the original value. A rule that removes a house number could hide the evidence that separates two addresses. Our normaliser is deliberately small. It handles these English address forms, not every international address. Before extending it, keep cases that must stay different and check that the new rule preserves them. Better comparison should help a decision, not erase the reason for it.

Delta's CRM company ID is missing. We lack that evidence. Two missing IDs do not support a match. A malformed value stays available for investigation.

Two usable IDs that disagree create an identity conflict. Our DEMO validator checks format, not company ownership. Replacing missing IDs with one placeholder would create false agreement. Missing, malformed and contradictory values need different actions.

The notebook puts missing and malformed IDs in an exception table with source keys, so an owner can find each row. A missing local record key prevents traceability: the notebook rejects that input. We need to find the original row again to explain a later decision.

Four CRM rows, three ERP rows and two portal rows give twenty-six possible cross-source pairs. At scale, comparing every pair costs too much.

First, we select equal usable company IDs. That keeps Alfa. We also select equal postcodes with the same name prefix. That keeps the Delta candidate. Nova Travel and Alfa meet neither rule, so we exclude that pair. Seven candidates remain.

The notebook uses two keyed joins, combines their results and removes repeated pairs. Alfa can pass both filters and still appears once per pair.

This is blocking: selecting pairs for comparison, before approval. A filter can exclude a real match. A later score cannot recover a pair it never receives. Labelled examples must also test what the filter misses.

CRM C101 finds a CRM row. ERP E501 finds an ERP row. The prefixes give the keys their namespaces, keeping one source's ID separate from another's.

Company ID can support identity across systems when we understand its meaning and trust its source. This example assumes reliable DEMO IDs. Valid format alone is not enough in real data. Both local keys remain after linking.

A local value such as C101 may be unique only inside CRM. Another source could use C101 for something unrelated. The namespace prevents that collision. Before using a company identifier across systems, we check its issuer, entity scope and reliability. A site ID or an account ID could be perfectly valid and still identify the wrong kind of object.

Which field supports connecting these two Alfa records?

Their shared company ID, DEMO-001, supports the link under our reliability assumption. Local keys identify separate source rows. We save their connection and reason.

The portal also has DEMO-001, but its shorter name and different address give its pair only forty-five points. Our rule gives a reliable shared ID priority over similarity. Using the score alone could leave this company split.

The reason stays with the pair, so we can explain which evidence controlled the decision. Company identity and the choice of billing address are separate decisions.

ERP E503 says Delta Services. Portal P902 says Delta Service. Edit distance measures changes between these strings. Messina used trigram search; both describe text similarity.

The portal has no company ID. Similarity gives a candidate, but cannot settle identity. This pair needs review.

It reaches about ninety-six points: about fifty-six from the name, twenty-five from equal address and fifteen from postcode. Without a reliable shared ID, our threshold of seventy routes it to review. A non-exact pair below seventy stays separate under this rule. A usable ID conflict takes priority whatever the score. Points measure field agreement under our rules, not automatically an identity probability.

Both records say Aurora Consulting and have the same address. What would you check next before linking them?

The company IDs are a useful next check. Name and address make a strong candidate, but companies can share offices or similar trading names. We need evidence that could change the decision, and we must understand its reliability. The name starts the search. Identity evidence decides whether we can finish it.

CRM has DEMO-002; ERP has DEMO-009. We trust these company IDs in this example, so the records stay separate.

Their score is still one hundred: sixty for name, twenty-five for address, fifteen for postcode. Every scored field agrees, while identity evidence contradicts the link.

Rule order matters. First check usable ID conflicts, then reliable shared IDs, then score other pairs. Putting high-score approval before conflict detection would change Aurora's result. A successful pipeline could still successfully produce the wrong answer.

One hundred points is field agreement, not a probability. If the IDs were unreliable, we would investigate the conflict and require evidence before approving the link.

Follow the proposed links from left to right. A has DEMO-002, B has no company ID, and C has DEMO-009. We trust the usable IDs.

Suppose we accept the proposed A and B link. Before adding C through B, we inspect all members of the resulting group. DEMO-002 and DEMO-009 conflict, so we stop. B's empty ID cannot remove that conflict.

We also stop a group that would contain a previously rejected pair. An approved pair can still fail this whole-group guard. Joining groups changes the identity claims we publish. The result must satisfy our rules, even when a reviewer supplied the missing evidence for one pair.

CRM C103 and ERP E503 both say Delta Services at Port Street five. CRM has no company ID. What extra evidence would justify this link?

The checked onboarding reference ONB-DELTA-42 connects CRM C103 to DEMO-003, already carried by ERP E503. It supports those exact source keys, so the reviewer can approve their pair beyond matching text.

Portal P902, Delta Service, is outside that assertion and needs its own evidence. Its two candidate pairs remain open. The supported CRM and ERP group can publish under our policy. Two open pairs concern one portal row, not two extra customers. Saving the pair scope lets the next run apply the answer correctly.

Follow the saved Delta decision at the left: pair keys, reviewer, time, evidence, rule version and fingerprint. A fingerprint summarises the comparison fields and rule version.

The middle check compares it with the current pair. The expected rule version, reviewer and evidence reference must also be present. Passing these checks applies the approval back in matching. The whole-group guard still runs.

A changed field, changed rule or incomplete answer sends the pair for review again. The fingerprint checks input changes, not identity. Production also needs to flag withdrawn evidence, even if the record fields have not changed. Reuse depends on both the inputs and the continued validity of the supporting evidence.

We can explain why a pair was approved, and when that approval needs review again. We still need a usable company record. The next decision chooses its published fields, keeps their source references and checks what happens when the source sends a later update.

Which source would you use for Alfa's billing address?

ERP is reasonable when it owns billing. Keeping distinct address roles is also reasonable: billing, delivery and sites can differ. Our example selects ERP for billing and CRM for the name.

This is survivorship: selecting the published value for a field and its purpose. The notebook takes the first non-empty value in that field's source priority. If ERP is empty, billing can fall back to CRM.

Priority is a business policy, not a guarantee that the value is suitable. Production needs address validation and a reason for fallback. We keep the chosen source. The portal address remains in its original row; it could describe another site or an older value.

Follow CRM C101, ERP E501 and portal P901 to Alfa's customer ID in the middle. Source links answer which records belong to the company and let us find the original rows.

Follow a different path through the field table below. Billing address Roma St., twelve comes from ERP E501. The name comes from CRM C101. These references explain the source chosen for each value: field provenance. Group membership and value choice are different questions.

At the right, we create a semantic model from Gold tables for analytics. Applications need a separate backend. Fabric item lineage shows item dependencies; our mappings and field references explain the customer inside them. What if ERP changes its address?

ERP E501 sends Roma Street fourteen. Should this change create a new customer?

Its company ID remains DEMO-001. Follow B001 to B002 at the top. Bronze keeps both versions. The current view selects B002 and billing publishes the new ERP address. Alfa keeps its company identity and customer ID below.

One new snapshot gives ten stored versions and nine current rows. Repeating B002 adds none. The notebook ingests the update but recomputes candidates on the current snapshot. Incremental ingestion and incremental matching are separate tasks.

A contradictory company ID would stop automatic linking. Changed fields in Delta's review would need another check. Delta's evidence is unchanged in this batch, so its saved approval remains usable.

Alfa is one company. Aurora is two because reliable IDs disagree. Delta is one supported CRM and ERP group. Nova Travel has no candidate and publishes separately under this example policy. We have five companies, eight source links and one held portal row, P902.

These checked local reference counts verify the exercise rules. They do not measure accuracy on enterprise data.

A false link joins different entities; a missed link leaves the same entity split. Measure them with an independent labelled sample, including true pairs excluded by blocking. Candidate coverage asks whether a true pair reached comparison. The unresolved portal labels remain uncertain, outside forced accuracy calculations. The labels need evidence too.

The production table shows three changes. Our group function collects nine rows to the driver, the process coordinating Spark work. Larger data needs distributed grouping with the same conflict checks.

Our notebook ingests B002 but recomputes candidates on a small snapshot. Production must track affected blocks and groups, with policies for deletions, late updates and version ties. Later load time does not always mean a newer source value.

Our customer ID comes from a reliable company ID or a source anchor. Alfa stays stable for this address update. Correcting that anchor could change the derived ID. Production needs a persistent identity registry: a stored history of entities, mappings and corrections, including merges and splits.

These are production requirements, not notebook features. Fabric supplies tools; we design the identity lifecycle. Where can you start?

Take three questions into your project. Are we linking the same kind of object? Messina separated street and address. What supports or contradicts the link? Aurora and Delta showed both. Can we trace a published value? Alfa kept mappings and field sources.

The flow in thirty seconds: preserve originals, add comparison fields, select candidates, check evidence, record decisions, check groups, publish supported results and revisit changed evidence.

Tomorrow, choose one entity and label a small sample as same, different or uncertain. Keep reasons. The pack contains the notebook, data and expected results. Its reference was checked locally. Validate a real Fabric run before claiming one. The pack is ready for a repository; a public material link is not yet published.

Which match would your system refuse to make? We have eight minutes for questions about the evidence, the rules or the architecture. Feel free to bring a difficult pair from your own data. We can use the same reasoning: define the object, check what supports the link, and look for anything that contradicts it.

Thank you for thinking through these decisions with me. This QR opens LinkedIn. You can also find me on GitHub and Sessionize. The notebook and datasets are in the session pack. I would be happy to hear about your own sources. Enjoy the rest of Data Saturday Sofia.

## Sources
Microsoft Fabric roles, interfaces and implementation references:

- [OneLake and medallion Lakehouse architecture](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture).
- [Notebook activity in Data Factory](https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity).
- [Explore Lakehouse data with a notebook](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data).
- [Create a semantic model](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-semantic-model).
- [Fabric lineage](https://learn.microsoft.com/en-us/fabric/governance/lineage).
- [Official Fabric icons](https://learn.microsoft.com/en-us/fabric/fundamentals/icons), with the [Microsoft icon package](https://github.com/microsoft/fabric-samples/blob/main/docs-samples/Icons.zip).
- [Lakehouse documentation image](https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-engineering/media/lakehouse-notebook-explore/load-data-menu.png) and [Notebook activity documentation image](https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-factory/media/notebook-activity/notebook-connection-workspace-parameters.png). These are authentic documentation assets, not screenshots of this notebook running.

Messina, territorial data and visual assets:

- [Municipality of Messina: public address register](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194), including the [public CSV](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194/resource/fce8cc08-6654-4c00-bf94-e3157d5da534/download/indirizzario.csv). Street name and civic rows used in the examples. Attribution and dataset licence details are in asset_sources.md.
- [National catalog entry for the address dataset](https://www.dati.gov.it/node/view-dataset/dataset?id=68adbea8-8e6d-486d-8804-d8782c2bbe3c).
- [Municipality of Messina: territorial and urban services](https://www.comune.messina.it/it/unita_organizzative/dipartimento-servizi-territoriali-ed-urbanistici).
- [Sicily regional GIS / SITR](https://www.sitr.regione.sicilia.it/). Territorial context for the reconstructed reference architecture.
- [Official procurement reference for SIMEL2 and Maggioli services](https://trasparenza.adspmaresiciliaorientale.it/appalti-190/detail.aspx?app=799&tp1=40). This concerns another authority. It supports the product name and supplier context, not a particular SIMEL release, module inventory or contract for the Messina project.
- [Messina Strait photograph](https://commons.wikimedia.org/wiki/File:Messina_Strait.jpg), Jeroen P, [CC BY 2.0](https://creativecommons.org/licenses/by/2.0/), cropped in the deck.

Matching and geographic implementation references:

- [PostgreSQL pg_trgm](https://www.postgresql.org/docs/current/pgtrgm.html).
- [PostGIS ST_DWithin and distance units](https://postgis.net/docs/ST_DWithin.html).
- [Spark levenshtein function](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.levenshtein.html).

Supplied project and example materials:

- Speaker-supplied Messina project account: end-to-end architecture and development, Python/FastAPI, React/TypeScript, PostgreSQL/PostGIS, trigram search, ETL, Docker, deployment and production support, five to six sources, reading from and returning validated links to Maggioli. Record and integration-view provenance is documented in asset_sources.md. Exact SIMEL release and vendor contracts were not supplied.
- Source revision: Sofia_2026_Community_Extended_Final.pptx. Earlier revisions derive from the supplied Sofia and Toronto materials. Sofia identity derives from Data Saturdays Sofia 2026 Template.pdf. Portrait, contact assets and LinkedIn QR derive from Day_of_Data_Toronto_2026_Daniele_Areddu_stage_ready.pptx.
- Session pack: reference.py, fabric_reconciliation.ipynb, datasets, expected/B001_results.json and expected/B002_results.json. Results are from the local reference. The notebook has not been run in Fabric in this preparation.
- Full asset provenance, adaptations, licences and the distinction between project facts, public data, documentation images and reconstruction: asset_sources.md in the session pack.
- Record origin, translated display labels and scoped review assertions: asset_sources.md, datasets/messina_display_labels.csv and datasets/teaching_evidence.json in the session pack.
