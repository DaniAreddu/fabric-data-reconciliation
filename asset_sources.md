# Assets and sources

Updated for the English revision, 10 October 2026. Primary Microsoft medallion, Notebook activity, semantic-model and PostGIS distance documentation rechecked. Existing photographs, public rows and icon provenance retained. Visual tables, labels, arrows, diagrams and geographic annotation remain native editable slide objects. Product icons and photographs remain embedded images.

## Original project, reference architecture and examples

- **Speaker-supplied project facts:** Municipality of Messina street-name reconciliation and territorial data management; five to six sources; Maggioli/SIMEL context; reading from Maggioli and pushing validated results; Python/FastAPI, PostgreSQL/PostGIS, trigram search, React/TypeScript, ETL, Docker, deployment and production stabilisation.
- **Version:** no exact SIMEL release or module inventory is available in the supplied project materials. The deck uses SIMEL. An official procurement record verifies the SIMEL2 name and Maggioli services for another authority, not the Messina topology or contract.
- **Reference feed topology:** street register/toponymy, Messina public addresses, SITR/Geoportale Sicilia, cadastral extracts and office CSV/Excel exports make the diagram concrete. They are not an assertion that all were integrated in the original project. A supplier and its suite are one operational node, not two sources.
- **Proposed patterns:** readback/confirmation, retry/idempotency and richer decision/audit state are integration design patterns. They are not claimed as original production implementation details.
- **Example records:** MAG:ODN:000184, TOP:STR:000531, OFF:ROW:000009, CIV:ADR:012784 and their fields are synthetic teaching namespaces and schemas. They are not SIMEL API contracts. Via Adolfo Celi is verified in the municipal CSV. The abbreviated form and erroneous Piazza variant illustrate disagreement. The deck does not assert that Piazza Adolfo Celi exists.
- **Impact scenarios:** misdirected correspondence, fine notices, unusable service address links, wrong territorial context, duplicate counts/maps, manual repairs and delayed downstream updates are possible consequences. They are not documented incidents or an assertion that this platform operated those services.

## Asset inventory

| Asset / use | Primary source | Treatment and attribution |
|---|---|---|
| Messina photograph, slide 5 | https://commons.wikimedia.org/wiki/File:Messina_Strait.jpg | Jeroen P, CC BY 2.0. Original photographic asset reused from the existing deck. Native cover crop, no content alteration. Attribution on the slide and in the final speech bibliography. https://creativecommons.org/licenses/by/2.0/ |
| Original context map, retained asset only | https://tile.openstreetmap.org/14/8899/6308.png | Actual map tile from OpenStreetMap. © OpenStreetMap contributors. Removed from the stage deck because its labels are Italian. The original asset is retained for provenance only. Slide 9 now uses native English tables and an address diagram. Public WGS84 coordinates remain in the sample CSV. https://www.openstreetmap.org/copyright |
| Public street names and civic rows, slides 7 and 9 | https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194 | Comune di Messina, Indirizzario, CC BY 4.0 with the published OSM addendum. Dataset metadata and CSV retrieved. A four-row unmodified-field sample is included in datasets/messina_public_sample.csv. |
| Public CSV | https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194/resource/fce8cc08-6654-4c00-bf94-e3157d5da534/download/indirizzario.csv | IDs and civics remain as published. Names have English display translations in slide 9; the unmodified names and WGS84 coordinates remain in the public CSV. UUIDs are shortened only for display. Coordinates remain in the sample CSV; they are not displayed as surveyed entrance positions. |
| Address dataset catalog | https://www.dati.gov.it/node/view-dataset/dataset?id=68adbea8-8e6d-486d-8804-d8782c2bbe3c | Primary metadata from the municipality, published through the national data catalog. |
| Municipal territorial responsibilities | https://www.comune.messina.it/it/unita_organizzative/dipartimento-servizi-territoriali-ed-urbanistici | Street register, geographical/toponymic responsibilities and SITR context. Supports the reference-feed labels, not project integration claims. |
| Regional territorial context | https://www.sitr.regione.sicilia.it/ | SITR is the regional territorial information system. Regional maps are a reference source in slide 6; its label is translated into English. No SITR screenshot or operational connection is claimed. |
| SIMEL2 expansion and Maggioli services | https://trasparenza.adspmaresiciliaorientale.it/appalti-190/detail.aspx?app=799&tp1=40 | Official procurement for the Autorità di Sistema Portuale del Mare di Sicilia Orientale. Supports the product-name expansion; the stage uses the English translation “Multichannel Information System for Local Authorities” and supplier services, not Messina's version, ownership, contract or topology. |
| Fabric component SVG icons, slides 18 and 34 | https://learn.microsoft.com/en-us/fabric/fundamentals/icons | Official Microsoft package: https://github.com/microsoft/fabric-samples/blob/main/docs-samples/Icons.zip . Notebook, Pipeline, Semantic Model and OneLake icons retain original colours and proportions. Names sit beside components. Package license copied to assets. |
| Lakehouse screenshot, slide 19 | https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data | Authentic Microsoft Learn documentation image. Cropped natively to the explorer containing Files/Tables. Its sample table names are unchanged and do not represent our workspace. Original image: https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-engineering/media/lakehouse-notebook-explore/load-data-menu.png |
| Pipeline screenshot, slide 20 | https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity | Authentic Microsoft Learn documentation image, natively cropped around Notebook activity and settings. It does not represent a pipeline provisioned or run for this deck. Original image: https://raw.githubusercontent.com/MicrosoftDocs/fabric-docs/main/docs/data-factory/media/notebook-activity/notebook-connection-workspace-parameters.png |
| Outcome table, slide 36 | reference.py + expected/B001_results.json in this pack | Verified local reference counts in a native table. Unnecessary shortened Gold IDs removed. No Fabric execution claimed. |
| Production comparison, slide 37 | Author-created native table; README production limits | Distinguishes teaching implementation from proposed production requirements. It is not an execution output. |
| Takeaways and first action, slide 38 | Author-created native text and shapes | Reuses Messina, Aurora, Delta and Alfa; no new source rows or evidence. |
| Operator comparison, slide 11 | Author-created native tables and diagram objects | Reconstructed operator view. Example keys and state are synthetic. No production app screenshot is claimed. |
| Bronze, review and Gold views, slides 19, 31 and 34 | Companion reference.py and synthetic fixtures | Native teaching tables. Local reference results, not screenshots of a Fabric execution. Table-role names omit recon_demo_ for readability; the notebook uses the full prefix. |
| Speaker photograph, social icons and LinkedIn QR, slides 2 and 40 | Supplied Toronto stage-ready PPTX | Retained source assets and links. No new portrait, QR target or repository URL was generated. |
| Sofia logo, dark background and green accents | Supplied Data Saturdays Sofia 2026 Template.pdf | Retained original logo image, proportions and palette. Template Source Sans Pro typography retained. |

## Exact public rows shown

Slide 9 uses public address IDs 019e5e6c-85d2-7c04-9a36-83f3168ca0a0 (VIALE BOCCETTA, civic 63) and 019e5e66-65b4-783a-9192-2f37fbc19e9f (same odonym, civic 65). Original coordinate fields remain in the sample CSV. Both retain their own address identity. The shared street context does not establish a production street link.

## Technical references

- OneLake and medallion roles: https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture
- Pipeline Notebook activity: https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity
- Lakehouse/Notebook: https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data
- Item lineage: https://learn.microsoft.com/en-us/fabric/governance/lineage
- Explicit semantic model creation: https://learn.microsoft.com/en-us/fabric/data-warehouse/create-semantic-model
- Trigram similarity and search indexes: https://www.postgresql.org/docs/current/pgtrgm.html
- Spatial distance units: https://postgis.net/docs/ST_DWithin.html
- Spark edit-distance function: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.levenshtein.html

## Execution status

The standalone local reference passes. Every PySpark notebook code cell compiles. The notebook has not been executed in a signed-in Fabric workspace. No visual is described as an authentic run of this notebook. First workspace execution requires validation. No live CRM/ERP/API connection, pipeline provisioning, review application or production identity registry is supplied.


## Final community revision — two editions

- The 40-slide order, dividers (4, 14, 17, 32), portrait, contacts and six questions (3, 25, 27, 30, 33, 35) are retained. Both editions have the same visual content.
- Slide 18 shows one record journey with an explicit candidate stage, data/decision arrows and dashed activity coordination. Official Microsoft icons retain their colours. Review returns its recorded decision to matching.
- Slide 29 removes the three unrelated case summaries and shows only the separate A–B–C whole-group conflict. The grouping guard is preserved.
- Slide 31 concentrates on fingerprint, rule version, complete saved evidence and the branch to review again. Withdrawal of evidence is identified as a production extension.
- Slide 34 separates source membership arrows from a native field-provenance table. Alfa's full customer ID remains visible on slides 34 and 35 and in the regenerated expected JSON.
- Slide 35 displays the before/after billing value, stable customer ID and conditions that require another check. Slide 36 separates fixture counts from accuracy measurement.
- Slide 37 consolidates driver grouping, snapshot recomputation and deterministic identity-anchor limits. Slide 38 gives the three takeaways and the next-day sample-labelling action. The old Aurora table on slide 38 is replaced; Aurora's verified score/conflict remains in slides 27–28 and the expected output.
- Lakehouse and Pipeline documentation images on slides 19–20 retain their authentic native crops. No demo workspace was provisioned or executed.
- All note bodies are spoken paragraphs only. Both complete scripts put their sources in a single final bibliography. Required attribution remains visible on the photograph and public-record diagram.
- Primary medallion, Notebook activity, semantic-model and PostGIS ST_DWithin pages were rechecked on 9 October 2026. The precise Messina SIMEL release remains unverified; SIMEL2 evidence refers to another authority.

## English revision — stage and materials

- Slide 4 now introduces the actual Municipality of Messina project on which the speaker worked. Architecture, development, production delivery, five–six sources and bidirectional Maggioli integration are supplied project facts.
- Data-origin captions are removed from stage slides and spoken notes. This does not turn the illustrative records or reference assertions into production exports. Their origin remains recorded above and in the evidence file.
- English display labels: Street, Square and Avenue replace Italian area-type words; feed names and the SIMEL expansion are translated. Official municipal source values remain unmodified in messina_public_sample.csv, with a separate display-label mapping.
- The company fixture itself now uses English names and addresses: Alfa Ltd / ALFA LTD; Delta Services in CRM/ERP and Delta Service in PORTAL; Roma Street / Roma St.; Verdi Street; Port Street; Milan Street. This is a translation of the existing instructional fixture, not a new actual business dataset.
- English address normalisation expands St. to Street. The rule version is recon-demo-v2-en. Review fingerprints and B001/B002 expected outputs are regenerated. Delta’s portal similarity score changes from 87.142857 to 95.714286; its review status is preserved. All seven candidate routes, five published companies, eight source links, the held portal record and Alfa’s stable customer ID are rechecked locally.
- REF-CELI-01 is the renamed street-reference assertion formerly labelled TRAINING-CELI-01. It remains illustrative evidence with STREET_LINK_ONLY scope. ONB-DELTA-42 remains scoped to CRM:C103 and ERP:E503. Neither is an original project document.
- Slide 9 contains no map tile, geographic coordinates or purported entrance measurements. Its native diagram shows shared street-name context and distinct address identities. The public record attribution remains on the slide.
- Microsoft screenshots, icons, portrait, contacts and QR are retained. No Fabric execution or live source connection is newly claimed.
