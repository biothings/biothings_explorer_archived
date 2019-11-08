BioThings Explorer Jupyter Notebook
===================================

## Introduction

BioThings Explorer is an engine for autonomously querying a distributed knowledge graph. The distributed knowledge graph is made up of biomedical APIs that have been annotated with semantically-precise descriptions of their inputs and outputs.  The knowledge graph is currently comprised by the APIs in this figure:

![BTE Metagraph](img/smartapi_metagraph.png "BioThings Explorer Metagraph" =500x)


## Prerequisite

1. Set up your python virtual environment [instructions](https://virtualenv.pypa.io/en/latest/). Please use Python version higher than 3.6.
2. Install biothings-explorer `pip install git+https://github.com/kevinxin90/bte_schema#egg=biothings_explorer`
3. Install biothings-schema `pip install git+https://github.com/biothings/biothings_schema.py#egg=biothings_schema`

**Important: In order for biothings explorer to work with jupyter notebooks, we use Notebook version 5.7.5 and tornado version 4.5.3 (these two packages will have conflict with Python's aysncio module). These packages are already added as dependency for biothings-explorer. If you accidentally upgraded these packages, please downgrade to the version specified above.**


## Demonstration notebooks
BioThings Explorer can answer two classes of queries -- "PREDICT" and "EXPLAIN".  We have prepared two notebooks that demonstrate each of these query types.  A more detailed overview of the BioThings Explorer system is provided in [these slides](https://docs.google.com/presentation/d/1QWQqqQhPD_pzKryh6Wijm4YQswv8pAjleVORCPyJyDE/edit?usp=sharing).

### EXPLAIN queries

EXPLAIN queries are designed to **identify plausible reasoning chains to explain the relationship between two entities**.  For example, in [EXPLAIN_demo.ipynb](EXPLAIN_demo.ipynb) we explore the question:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"*Why does imatinib have an effect on the treatment of chronic myelogenous leukemia (CML)?*"

### PREDICT queries

PREDICT queries are designed to **predict plausible relationships between one entity and an entity class**.  For example, in [PREDICT_demo.ipynb](PREDICT_demo.ipynb), we explore the question:  

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*"What drugs might be used to treat hyperphenylalaninemia?"*

There are still many areas for improvement (and some areas in which BioThings Explorer is still buggy).  And of course, BioThings Explorer is dependent on the accessibility of the APIs that comprise the distributed knowledge graph.  Nevertheless, we encourage users to try other variants of the PREDICT queries demonstrated in this notebook.
