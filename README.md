# bte_schema

## Introduction

This is the development repo for the python client of BioThings Explorer. This tool aims at helping users querying and linking results from a variety of biomedical relevant APIs through one interface. The project is funded by the NCATS Translator project.

### Revelant Concepts

1. BioLink Model

[The BioLink Model](https://biolink.github.io/biolink-model/) defines a high level datamodel of biological entities (genes, diseases, phenotypes, pathways, individuals, substances, etc) and their associations. BioThings Explorer restructures outputs from different APIs into the data model defined by BioLink, so that they can be easily connected and queried.

---
2. Schema.org

[Schema.org](https://schema.org) is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet, on web pages, in email messages, and beyond. We convert the BioLink Model into the Schema.org format. You could visualize it through the [CD2H schema playground](https://discovery.biothings.io/bts62675/).

---
3. Current Integrated APIs

- [MyGene.info API](https://mygene.info)
- [MyVariant.info API](https://myvariant.info)
- [MyChem.info API](https://mychem.info)
- [MyDisease.info API](http://mydisease.info)
- [Semmed API](https://pending.biothings.io/semmed)
- [BioLink API](https://api.monarchinitiative.org/api)
- [DGIdb API](http://dgidb.org/api)
---
4. Schema Mapping File

Schema Mapping File is a JSON document aiding the conversion from the original API output into the BioLink Model. The mapping files for those already integrated APIs are stored in the [NCATS Translator API registry repo](https://github.com/NCATS-Tangerine/translator-api-registry/tree/openapi_2.0).

### How to use the package
Jupyter notebook demo is located at [this folder](https://github.com/kevinxin90/bte_schema/tree/master/jupyter%20notebooks). An official documentation will come soon.  
