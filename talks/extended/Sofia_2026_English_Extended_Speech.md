Hi everyone. Today we will follow records that describe the same thing in different ways. We start with addresses in Messina, then customers in Microsoft Fabric. We will decide which records to connect, what evidence we need, and how to handle an uncertain answer.

I'm Daniele Mario Areddu, a Backend and AI Developer at Global Technologies Italia and a Computer Science student at the University of Calabria. In Messina, I led the architecture, development and production delivery of a territorial data platform. That experience gives us our starting question.

What happens when the address exists in one system, but another system cannot find its street link? The office record here contains Adolfo Celi Street, number 253. The street reference is missing. The other system has a record for A. Celi Street. What would you check before using this address?

I would start by checking which street the office record belongs to. The name helps us search, but we still need evidence for the connection. A missing link also tells us nothing about whether the physical address exists. The problem here is the reference between records.

This is what I mean by reconciliation: we decide which records describe the same thing, and keep the evidence for that decision. We preserve the original rows and add a supported link. Another process can then use that link and understand why we created it. Let's see the setting behind this example.

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

Alfa appears in three places. CRM means customer relationship management. Here it provides the sales view. ERP means enterprise resource planning. Here it owns billing information. The portal record arrives through an API, an interface that lets another system read data.

The names differ. The portal address says number ten, while the other records say twelve. We are matching companies in this example. Sites, contacts and application accounts need their own identities.

Keep an eye on CRM C101, ERP E501 and portal P901.

Those local IDs let us find rows again. A company ID carries a different claim. We will test that claim separately from the name and address, and keep the row keys even when we publish one company. Before we choose the rules, we should understand the cost of choosing badly.

One company staying split can leave support with only part of its history. Joining different companies can send an invoice to the wrong company. Those errors have different costs. The business process guides the evidence we require. More links alone do not prove improvement.

The business risk gives us a reason to keep decisions visible. Fabric gives us a place to store the rows and run our rules. Follow the same source key through the layers. Each step adds information, while the original record remains available.

Follow CRM C101 at the left. Its received row enters Bronze, in a Lakehouse stored in OneLake. Pipeline starts the notebook when the extracts are ready. The dashed arrow shows that instruction.

The notebook uses PySpark, Python running on Spark, to add comparison fields in Silver. C101 keeps its source key. Next, the rules select Alfa pairs and check their evidence. Selecting a candidate has not approved a link. For a supported pair, the solid path continues to Gold, with the company result and its source links.

An uncertain pair takes the lower path to operator review. The operator records a decision with evidence. The return arrow brings that answer back to matching, where the rules check whether it still applies. A pending answer stays outside trusted publication under our policy. That loop is part of the flow.

We centralised the data. The disagreement came with it. The reconciliation logic is our application logic, implemented in this notebook. Let's start with what we preserve.

Files keeps the original extracts. Tables keeps source snapshots with their load context. A batch is one load. Alfa's received names remain unchanged. Source and batch information let us trace a decision back to those values.

Loading the same batch again avoids adding the same snapshot twice in our example.

B001 is the first batch. A snapshot is the version of a source row received in that load. We keep source, local ID and batch together. The same row can later appear in B002 without erasing B001. Source update time tells us when the source changed it. Load time tells us when we received it. Both help explain which version a decision used. A repeated batch with conflicting values is an error to investigate. The interface images show where files and tables are kept. Our source keys and batch values show how we preserve inputs before processing them. When a reviewer asks why a link was created last week, the current row alone may no longer explain it. The stored snapshot lets us return to the values that the earlier rule actually compared.

We add Notebook activity and select the notebook to start. The extracts must be ready first. Pipeline coordinates the activity, and the notebook runs the rules.

A completed activity tells us the work finished.

A production flow would also check whether the expected extracts arrived and whether publication passed its checks. A technical success with missing input can still produce an incomplete result. The screenshots show Microsoft documentation interfaces. Our pack supplies a notebook and source extracts. Live connections would be configured separately. We check the received batch and the published results, starting with the fields we compare.

CRM C101 and ERP E501 keep their original names. We add a comparison field where case and punctuation follow the same rules. Both names now read alfa ltd. Our address rule expands St. to Street and removes punctuation, so Roma St., twelve and Roma Street twelve can be compared. This is normalisation: explicit rules make comparisons consistent. Portal P901 still has number ten. Cleaning preserves that meaningful difference. The comparison field sits beside the original value. A rule that removes a house number could hide the evidence that separates two addresses. Our normaliser is deliberately small. It handles these English address forms, not every international address. Before extending it, keep cases that must stay different and check that the new rule preserves them. Better comparison should help a decision, not erase the reason for it.

Delta's CRM record has no company ID. That means we lack that piece of evidence. Two missing IDs do not support a match. An unusable value is another situation: we retain the original and check why it failed validation.

Two usable IDs that disagree create a possible identity conflict. Our DEMO validator checks the format only. It does not verify which company owns the identifier. Missing, malformed and contradictory values need different actions.

Replacing every missing ID with the same placeholder would create false agreement. 

The notebook puts missing and malformed company IDs in an exception table with their source key. That lets an owner return to the exact row and investigate it. A missing local record key is more serious for traceability: the notebook rejects that input. We need a row we can find again before we can explain a later decision about it.

We have four CRM rows, three ERP rows and two portal rows. Comparing records across different sources gives twenty-six possible pairs. On larger datasets, comparing every pair becomes expensive.

We first select pairs with the same usable company ID. That keeps Alfa. We also select pairs with the same postcode and name prefix. That keeps the Delta candidate shown here. Nova Travel and Alfa meet neither rule, so we exclude that pair. Seven candidates remain.

Four times three gives twelve CRM to ERP pairs. Four times two gives eight CRM to portal pairs. Three times two gives six ERP to portal pairs. Together they make twenty-six. The notebook uses two keyed joins for the two selection rules, combines their results and removes repeated pairs. Alfa can satisfy both filters and still appears once per pair.

This filter is called blocking. It selects pairs for comparison. It has not approved them. The filter can also exclude a real match, and a later score cannot recover a pair it never receives. We need labelled examples that test which true pairs the filter misses.

CRM C101 finds a CRM row. ERP E501 finds an ERP row. The prefixes give the keys their namespaces, keeping one source's ID separate from another's.

Company ID can support identity across systems when we understand its meaning and trust its source. This example assumes reliable DEMO IDs. Valid format alone is not enough in real data. Both local keys remain after linking.

A local value such as C101 may be unique only inside CRM. Another source could use C101 for something unrelated. The namespace prevents that collision. Before using a company identifier across systems, we check its issuer, entity scope and reliability. A site ID or an account ID could be perfectly valid and still identify the wrong kind of object.

Which field supports connecting these two Alfa records?

The shared company ID, DEMO-001, supports the link under our reliability assumption. The local keys continue to identify two different source rows. We save their connection and the reason for it.

The portal record also has DEMO-001, even though its name is shorter and its address differs. Our rule gives that reliable shared ID priority over the similarity score.

The portal pair scores only forty-five because the short name and different address reduce field agreement. The reliable shared ID still supports company identity here. If we used the score alone, we could leave that company split. The rule stores the reason with the pair, so the result explains which evidence controlled the decision. Choosing company identity and choosing a billing address are separate decisions.

ERP E503 says Delta Services. Portal P902 says Delta Service. The names are close, and a text comparison can measure how close. Our notebook uses edit distance, which counts changes between character strings. Messina used trigram search. Both methods help us describe text similarity.

The portal has no company ID. The similar name gives us a candidate, but it cannot settle company identity. This pair needs review. Our score measures agreement between fields.

Delta Service reaches about ninety-six points against Delta Services. The similar name contributes about fifty-six. The equal address adds twenty-five and the postcode fifteen. Without a reliable shared ID, that total routes the pair to review. Our illustrative threshold is seventy. A non-exact pair below that threshold stays separate under this rule. An ID conflict still takes priority whatever the score.  It does not automatically give us an identity probability.

Both records say Aurora Consulting. They have the same address too. What would you check next before linking them?

The company-ID field is a useful next check. The matching name and address make this a strong candidate, but companies can share an office or similar trading names. We need to look for evidence that could change the decision, and understand how reliable that evidence is. The name starts the search. The identity evidence decides whether we can finish it.

The CRM has DEMO-002. The ERP has DEMO-009. In this example, we trust those company IDs, so we keep the records separate.

The score still reaches one hundred. The name contributes sixty points, the address twenty-five and the postcode fifteen. Every scored field agrees. The identity evidence contradicts the link. That is why our conflict rule takes priority over the score.

The order of the rules matters. We check a usable ID conflict first. Then we check a reliable shared ID. Only after those checks do we use the score to route other pairs. Moving the conflict check below a high-score approval would change Aurora's outcome. The priority is part of the rule and must be tested. A successful pipeline could still successfully produce the wrong answer.

One hundred points describes field agreement. It is not a probability. If the IDs came from an unreliable source, we would investigate the conflict and require evidence before approving a connection.

A pair can look safe and still create a problem for its group. Follow the proposed links from left to right. A has DEMO-002. B has no company ID. C has DEMO-009. We trust the usable IDs in this example.

Suppose we accept the proposed A and B link. Before adding C through B, we inspect the group that would result. It would contain both DEMO-002 and DEMO-009. That conflict stops the union. The empty ID in B provides no evidence that could remove it.

This is why we check all members before accepting another link. We also check whether the proposed group would contain a pair already rejected. An approved pair can reach this guard and still fail the group check. Joining groups changes the set of identity claims we publish. The resulting company must satisfy the same rules as its individual links. A reviewer can help with missing evidence, but must also respect that boundary.

CRM C103 and ERP E503 both say Delta Services at Port Street five. The CRM company ID is missing. What extra evidence would justify this link?

A checked onboarding reference can support it. Here, ONB-DELTA-42 connects CRM C103 to DEMO-003, which ERP E503 already carries. That assertion supports these two source keys. We can explain why the reviewer approves the pair, beyond their matching text.

Portal P902, Delta Service, is outside that assertion. It still needs its own evidence. Its two candidate pairs stay open, while the supported CRM and ERP group can publish under our policy. We have two questions about one portal row, rather than two extra customers. The review decision must preserve its scope, so the next run can apply the answer to the same pair.

Follow the Delta approval into the saved decision at the left. It contains the pair keys, reviewer, time and evidence reference. We also save the rule version and a fingerprint. A fingerprint is a compact summary of the fields used in the comparison and the rule version.

The middle check asks whether that summary still matches the current pair. We also require the expected rule version, a reviewer and an evidence reference. If these checks pass, the right-hand arrow applies the saved approval back in matching. The whole-group guard still runs after that.

If a relevant field or the rule changes, the lower path sends the pair for review again. An incomplete saved answer also stays pending. A fingerprint tells us whether these inputs changed. It does not prove company identity. In a real process, the evidence owner may also withdraw an earlier reference. We need a way to flag that decision for review even when the record fields stay the same.

We can explain why a pair was approved, and when that approval needs review again. We still need a usable company record. The next decision chooses its published fields, keeps their source references and checks what happens when the source sends a later update.

Which source would you use for Alfa's billing address?

ERP is a reasonable choice when it owns billing information. Keeping separate address roles is also reasonable. A company may have a billing address, a delivery address and several sites. In our example, we choose ERP for billing and CRM for the company name.

This is survivorship: choosing the published value for a field. The policy follows the field and its business purpose.

Our notebook chooses the first non-empty value in the source priority for that field. If ERP has no address, the policy can fall back to CRM. The priority is a business policy. A value from ERP still needs to be suitable for billing. A production process also validates the address for its intended use and records why a fallback was needed. We retain the source of the chosen value. The portal address remains available in the original record. It could describe another site or an older value, so we preserve it while publishing the billing address selected by our policy.

Start with the three source keys at the left. CRM C101, ERP E501 and portal P901 point to one supported Alfa customer ID in the middle. These mappings answer which source records belong to that company. A consumer can use them to return to the original rows.

Now follow a different path through the field table below. The billing address is Roma St., twelve, and its source is ERP E501. The name comes from CRM C101. Those references answer why this particular value appears in the published record. That is field provenance. It explains our source choice for a value, alongside the mappings that explain group membership.

At the right, we create a semantic model from the intended Gold tables for analytics. Applications need a separately implemented backend. Fabric item lineage can show dependencies between items. Our row mappings and field references add the evidence needed to explain a customer inside those items. The result is usable, and we can trace its choices. What happens when ERP sends a new address?

ERP E501 now sends Roma Street fourteen. Should this change create a new customer?

The company ID is still DEMO-001. Follow the address change from B001 to B002 at the top. Bronze preserves both versions. The latest source view selects B002, and our billing policy publishes the new ERP address. Below that change, Alfa keeps the same supported company identity and customer ID.

The new batch adds one snapshot. We now have ten stored source versions and nine current rows. Repeating B002 adds no extra snapshot in this example. The notebook ingests that changed row and then rebuilds candidates from the current snapshot. Incremental ingestion and incremental matching are separate tasks.

An identity change needs different treatment. A new contradictory company ID would stop automatic linking under our rules. Changes to fields used in Delta's review would require another check. Delta's evidence is unchanged in this batch, so its saved approval remains usable. We update what the new evidence supports and keep the previous versions available.

Read the company table first. Alfa gives us one company. Aurora gives us two, because its reliable IDs disagree. Delta gives us one supported CRM and ERP group. Nova Travel has no candidate under our rules and publishes separately under this example policy. That makes five companies, with eight source links. Portal P902 is one held source row.

These are the checked local reference outputs. They tell us that the exercise follows its rules. They do not tell us the accuracy on new enterprise data.

A false link joins different entities. A missed link leaves the same entity split. To measure those errors, use an independent labelled sample, including true pairs excluded by blocking. Candidate coverage asks whether a true pair reached comparison at all. The unresolved portal labels remain uncertain, so we keep them outside a forced accuracy calculation. We need evidence for the labels as well as the links. That gives us a basis for improving the rules before using them at larger scale.

The production table shows where the current implementation needs to change. Our group function collects nine rows to the driver, the process coordinating Spark work. For larger data, grouping needs distributed processing with the same conflict checks. Simply collecting more rows would create a memory problem without solving identity.

The notebook ingests B002 but recomputes candidates on the small current snapshot. A production flow needs to track affected blocks and groups. It also needs explicit policies for deleted rows, late updates and ties between source versions. A later load time alone does not mean a more recent source value.

The customer ID here comes from a reliable company ID, or a source anchor when none exists. That keeps Alfa stable for the demonstrated address change. Correcting the identity anchor could change the derived ID. Production therefore needs a persistent identity registry: a stored history of entities, mappings and corrections. It must record merges and splits, rather than silently replacing IDs.

These are production requirements, not features supplied by our notebook. Fabric provides storage and processing tools. We still design the identity lifecycle and operational rules. That brings us to a practical first step.

Take these questions into your next project. Are we connecting the same kind of object? Messina showed why a street and an address need separate identities. What evidence supports the link, and what could contradict it? Aurora and Delta gave us different answers. Can we explain the published value from its sources? Alfa kept both mappings and field references.

Here is the flow in thirty seconds. Preserve originals. Add comparable fields. Select candidates and check their evidence. Record decisions, check their groups, publish supported results and revisit decisions when relevant evidence changes.

Tomorrow, choose one entity and label a small sample as same, different or uncertain. Keep the reasons. The session pack provides the notebook, data, expected results and checklist. The reference was checked locally. Validate the first notebook run in Fabric before claiming a workspace execution. The pack is ready for your repository, but a public material link has not been published.

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
