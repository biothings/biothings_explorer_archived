BioThings Explorer Jupyter Notebook
===================================

## Prerequisite

1. Set up your python virtual environment [instructions](https://virtualenv.pypa.io/en/latest/). Please use Python version higher than 3.6.
2. Install Jupyter `pip install jupyter`
3. Downgrade Notebook `pip install notebook==5.7.5`
4. Downgrade tornado `pip install tornado==4.5.3`
5. Install biothings-explorer `pip install git+https://github.com/kevinxin90/bte_schema#egg=biothings_explorer`
6. Install biothings-schema `pip install git+https://github.com/biothings/biothings_schema.py#egg=biothings_schema`

**Important: In order for biothings explorer to work with jupyter notebooks, you must downgrade Notebook to 5.7.5 and tornado to 4.5.3 (these two packages will have conflict with Python's aysncio module)**

**Note: There might be warning or error during installation of biothings-explorer or biothings-schema. Don't worry. As long as it "shows Successfully built biothings-explorer" in the end, you will be fine**


## Notebooks

### 1. BioThings Explorer Metadata 
------------------------------
[link to notebook](https://github.com/kevinxin90/bte_schema/blob/master/jupyter%20notebooks/BioThings%20Explorer%20Metadata.ipynb)

This notebook list how to find metadata information about biothings-explorer, including:
- Find all semantic types used in BioThings Explorer
- Find all identifier types used in BioThings Explorer
- Find all predicates used in BioThings Explorer
- Find all associations between semantic types in BioThings Explorer
- Filter associations based on input/output semantic types as well as predicate

- **Please take a look at this notebook first before querying BioThings Explorer!**


### 2. BioThings Explorer Demo
--------------------------
[link to notebook](https://github.com/kevinxin90/bte_schema/blob/master/jupyter%20notebooks/BioThings%20Explorer%20Demo.ipynb)

This notebook shows you some of the basic features of biothings-explorer, incluing:
- Single Hop Query (Connecting from one entity to another through one hop query)
- Multi Hop Query (Connecting from one entity to another through mulitple hops query)
- Connect (Discover connections between two entities through intermediate nodes)


