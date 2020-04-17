# BioThings Explorer

[![Build Status](https://travis-ci.org/biothings/biothings_explorer.svg?branch=master)](https://travis-ci.org/biothings/biothings_explorer)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1213cfd2b04948e792e6f122944a4c5a)](https://app.codacy.com/gh/biothings/biothings_explorer?utm_source=github.com&utm_medium=referral&utm_content=biothings/biothings_explorer&utm_campaign=Badge_Grade_Dashboard)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/1213cfd2b04948e792e6f122944a4c5a)](https://app.codacy.com/gh/biothings/biothings_explorer?utm_source=github.com&utm_medium=referral&utm_content=biothings/biothings_explorer&utm_campaign=Badge_Coverage_Dashboard)
[![Documentation Status](https://readthedocs.org/projects/biothings-explorer/badge/?version=latest)](https://biothings-explorer.readthedocs.io/en/latest/?badge=latest)

## Introduction

This is the development repo for the python client of BioThings Explorer. This tool aims at helping users querying and linking results from a variety of biomedical relevant APIs through one interface. The project is funded by the NCATS Translator project.

## P.S. — Documentation is Available at [`//biothings-explorer.readthedocs.io`](https://biothings-explorer.readthedocs.io/en/latest/).

### Revelant Concepts

1. BioLink Model

   [The BioLink Model](https://biolink.github.io/biolink-model/) defines a high level datamodel of biological entities (genes, diseases, phenotypes, pathways, individuals, substances, etc) and their associations. BioThings Explorer restructures outputs from different APIs into the data model defined by BioLink, so that they can be easily connected and queried.

2. Schema.org

   [Schema.org](https://schema.org) is a collaborative, community activity with a mission to create, maintain, and promote schemas for structured data on the Internet, on web pages, in email messages, and beyond. We convert the BioLink Model into the Schema.org format. You could visualize it through the [CD2H schema playground](https://discovery.biothings.io/bts62675/).

3. Current Integrated APIs

   - [MyGene.info API](https://mygene.info)
   - [MyVariant.info API](https://myvariant.info)
   - [MyChem.info API](https://mychem.info)
   - [MyDisease.info API](http://mydisease.info)
   - [Semmed API](https://pending.biothings.io/semmed)
   - [BioLink API](https://api.monarchinitiative.org/api)
   - [DGIdb API](http://dgidb.org/api)
   - [CORD Gene API](https://biothings.ncats.io/cord_gene)
   - [CORD Protein API](https://biothings.ncats.io/cord_protein)
   - [CORD Chemical API](https://biothings.ncats.io/cord_chemical)
   - [CORD Cell API](https://biothings.ncats.io/cord_cell)
   - [CORD Disease API](https://biothings.ncats.io/cord_disease)
   - [CORD Molecular Activity API](https://biothings.ncats.io/cord_ma)
   - [CORD Biological Process API](https://biothings.ncats.io/cord_bp)
   - [CORD Genomic Entity API](https://biothings.ncats.io/cord_genomic_entity)
   - [CORD Anatomy API](https://biothings.ncats.io/cord_anatomy)
   - [CORD Cellular Component API](https://biothings.ncats.io/cord_cc)
   - [EBIgene2phenotype API](https://biothings.ncats.io/ebigene2phenotype)
   - [DISEASES API](https://biothings.ncats.io/DISEASES)
   - [PFOCR API](https://biothings.ncats.io/pfocr)
   - [QuickGO API](https://www.ebi.ac.uk/QuickGO)
   - [LitVar API](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/LitVar/#!?query=)
   - [Ontology Lookup Service API](https://www.ebi.ac.uk/ols)
   - [Stanford Biosample API](http://api.kp.metadatacenter.org/)
   - [ChEMBL API](https://www.ebi.ac.uk/chembl)
   - [CTD API](http://ctdbase.org)
   - [OpenTarget API](https://platform-api.opentargets.io)
   - [RGD API](https://rest.rgd.mcw.edu)
   - [Automat CORD19 Scibite API](https://automat.renci.org)

4. Schema Mapping File

    Schema Mapping File is a JSON document aiding the conversion from the original API output into the BioLink Model. The mapping files for those already integrated APIs are stored in the [NCATS Translator API registry repo](https://github.com/NCATS-Tangerine/translator-api-registry/tree/openapi_2.0).

### How to use the package

Jupyter notebook demo is located at [this folder](https://github.com/kevinxin90/bte_schema/tree/master/jupyter%20notebooks). An official documentation will come soon.  
