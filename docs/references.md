# References

Primary sources used for the talk, the notebook and this documentation. Microsoft Learn pages were rechecked on 10 October 2026.

## Microsoft Fabric

- [Implement medallion lakehouse architecture in Fabric](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture): Bronze, Silver and Gold roles; one Lakehouse per layer, ideally in separate workspaces.
- [Load data into your lakehouse with a notebook](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-notebook-load-data): relative and ABFS paths, the `/lakehouse/default/` mount.
- [How to use notebooks](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook): importing `.ipynb` files, adding and pinning a default Lakehouse, the security context of interactive, pipeline and scheduled runs.
- [Navigate the Lakehouse explorer](https://learn.microsoft.com/en-us/fabric/data-engineering/navigate-lakehouse-explorer): Files and Tables, subfolders and uploads.
- [Troubleshoot lakehouse errors](https://learn.microsoft.com/en-us/fabric/data-engineering/troubleshoot-lakehouse): file locations and Spark paths.
- [Notebook activity](https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity): running a notebook from a pipeline.
- [Create a Power BI semantic model](https://learn.microsoft.com/en-us/fabric/data-warehouse/create-semantic-model): explicit creation; default semantic models are no longer created automatically.
- [Lineage in Fabric](https://learn.microsoft.com/en-us/fabric/governance/lineage): item-level dependencies.
- [Fabric icons](https://learn.microsoft.com/en-us/fabric/fundamentals/icons) and the [icon package](https://github.com/microsoft/fabric-samples/blob/main/docs-samples/Icons.zip).

## Matching and geometry

- [Spark `levenshtein` function](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.levenshtein.html): edit distance used for name similarity in the notebook.
- [Spark `DataFrame.unionByName`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.unionByName.html): combining the extracts and the two candidate joins.
- [PostgreSQL `pg_trgm`](https://www.postgresql.org/docs/current/pgtrgm.html): trigram similarity and indexes, as used for street-name search in the Messina platform.
- [PostGIS indexing](https://postgis.net/workshops/postgis-intro/indexing.html) and [`ST_DWithin`](https://postgis.net/docs/ST_DWithin.html): spatial indexes and distance units for `geometry` and `geography`.

## Messina and territorial data

- [Indirizzario del Comune di Messina](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194) and its [CSV](https://dati.comune.messina.it/dataset/08f64302-54e3-4d77-be2b-e9f2abaa1194/resource/fce8cc08-6654-4c00-bf94-e3157d5da534/download/indirizzario.csv): public address register, CC BY 4.0.
- [National catalogue entry](https://www.dati.gov.it/node/view-dataset/dataset?id=68adbea8-8e6d-486d-8804-d8782c2bbe3c) for the same dataset.
- [Comune di Messina, territorial and urban services department](https://www.comune.messina.it/it/unita_organizzative/dipartimento-servizi-territoriali-ed-urbanistici).
- [SITR, Regione Siciliana](https://www.sitr.regione.sicilia.it/).
- [Procurement record naming SIMEL2 and Maggioli services](https://trasparenza.adspmaresiciliaorientale.it/appalti-190/detail.aspx?app=799&tp1=40), for another authority; it does not describe the Messina installation.
- [Messina Strait photograph](https://commons.wikimedia.org/wiki/File:Messina_Strait.jpg), Jeroen P, CC BY 2.0.

## Licenses

- [MIT license text](https://choosealicense.com/licenses/mit/)
- [CC BY 4.0 legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en) and [Creative Commons FAQ](https://creativecommons.org/faq/)
- [GitHub: licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
