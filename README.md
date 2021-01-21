# BioThings Explorer

![Test BioThings Explorer Python Package](https://github.com/biothings/biothings_explorer/workflows/Test%20BioThings%20Explorer%20Python%20Package/badge.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1213cfd2b04948e792e6f122944a4c5a)](https://app.codacy.com/gh/biothings/biothings_explorer?utm_source=github.com&utm_medium=referral&utm_content=biothings/biothings_explorer&utm_campaign=Badge_Grade_Dashboard)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/1213cfd2b04948e792e6f122944a4c5a)](https://app.codacy.com/gh/biothings/biothings_explorer?utm_source=github.com&utm_medium=referral&utm_content=biothings/biothings_explorer&utm_campaign=Badge_Coverage_Dashboard)
[![Documentation Status](https://readthedocs.org/projects/biothings-explorer/badge/?version=latest)](https://biothings-explorer.readthedocs.io/en/latest/?badge=latest)

## Introduction

This is the development repo for the python client of BioThings Explorer. This tool aims at helping users querying and linking results from a variety of biomedical relevant APIs through one interface. The project is funded by the NCATS Translator project.

## P.S. — Documentation is Available at [`//biothings-explorer.readthedocs.io`](https://biothings-explorer.readthedocs.io/en/latest/).

### Revelant Concepts

1. BioLink Model

   [The BioLink Model](https://biolink.github.io/biolink-model/) defines a high level datamodel of biological entities (genes, diseases, phenotypes, pathways, individuals, substances, etc) and their associations. BioThings Explorer restructures outputs from different APIs into the data model defined by BioLink, so that they can be easily connected and queried.

2. SmartAPI

   [SmartAPI](https://smart-api.info) aims to maximize the FAIRness (Findability, Accessibility, Interoperability, and Reusability) of web-based Application Programming Interfaces (APIs). Rich metadata is essential to properly describe your API so that it becomes discoverable, connected, and reusable. BioThings Explorer takes advantage of the rich metadata information described in SmartAPI and create a meta knowledge graph, allowing BioThings Explorer to autonomously query a distributed knowledge graph. The distributed knowledge graph is made up of biomedical APIs that have been annotated with semantically-precise descriptions of their inputs and outputs.

### Current Integrated APIs

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
   - [Automat CORD19 Scigraph API](https://automat.renci.org)
   - [Automat CORD19 Pharos API](https://automat.renci.org)
   - [Automat CORD19 hetio API](https://automat.renci.org)
   - [Automat CORD19 HMDB API](https://automat.renci.org)


### How to use the package

Official Documentation is Available at [`//biothings-explorer.readthedocs.io`](https://biothings-explorer.readthedocs.io/en/latest/)

Jupyter notebook demo is located at [this folder](https://github.com/kevinxin90/bte_schema/tree/master/jupyter%20notebooks).

Some real world use cases of BioThings Explorer.

   - [Why does imatinib have an effect on the treatment of chronic myelogenous leukemia (CML)?](https://colab.research.google.com/github/biothings/biothings_explorer/blob/master/jupyter%20notebooks/EXPLAIN_demo.ipynb)
   - [What drugs might be used to treat hyperphenylalaninemia?](https://colab.research.google.com/github/biothings/biothings_explorer/blob/master/jupyter%20notebooks/PREDICT_demo.ipynb)
   - [Finding New Uses for Existing Drugs to Treat Parkinson’s Disease](https://colab.research.google.com/github/biothings/biothings_explorer/blob/master/jupyter%20notebooks/TIDBIT%2002%20Finding%20New%20Uses%20for%20Existing%20Drugs%20to%20Treat%20Parkinson%E2%80%99s%20Disease.ipynb)
   - [Finding Marketed Drugs that Might Treat an Unknown Syndrome by Perturbing the Disease Mechanism Pathway](https://colab.research.google.com/github/biothings/biothings_explorer/blob/master/jupyter%20notebooks/TIDBIT%2004%20Finding%20Marketed%20Drugs%20that%20Might%20Treat%20an%20Unknown%20Syndrome%20by%20Perturbing%20the%20Disease%20Mechanism%20Pathway.ipynb)


