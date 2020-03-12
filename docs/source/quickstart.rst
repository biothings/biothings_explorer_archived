.. _quickstart:

Quickstart
===================

Eager to get started? This page gives a good introduction in how to get started with BioThings Explorer.

First, make sure that: biothings_explorer is installed.

Let's get started with some simple examples.

Find all chemicals related to a gene
------------------------------------

* Begin by importing the biothings_explorer modules

>>> from biothings_explorer.hint import Hint
>>> from biothings_explorer.user_query_dispatcher import FindConnection

* Find representation of "CXCR4" Gene in BioThings Explorer

>>> ht = Hint()
>>> cxcr4_hint = ht.query("cxcr4")
>>> cxcr4 = cxcr4_hint['Gene'][0]
>>> cxcr4

* Now we have the representation of cxcr4 in BTE, let's go ahead and find all chemicals that are related to cxcr4

>>> fc = FindConnection(input_obj=cxcr4, output_obj='ChemicalSubstance', intermediate_nodes=None)
>>> fc.connect(verbose=True)

* So far, BTE has queried all APIs which could connects from CXCR4 to chemical substances. Now we could go ahead and explore the results, e.g. as a pandas data frame, as a graphml file, a reasoner API standard JSON file

>>> fc.display_table_view()
>>> fc.to_graphml('cxcr4_chemical.graphml')
>>> fc.to_reasoner_std()


Find all chemicals that target genes that are associated with gene PRDX1
------------------------------------------------------------------------

This is a more complicated example with intermediate nodes involved. It requires:


1. First, find all genes that associate with PRDX1
2. Second, find all chemicals that target these genes




* Begin by importing the biothings_explorer modules

>>> from biothings_explorer.hint import Hint
>>> from biothings_explorer.user_query_dispatcher import FindConnection

* Find representation of "PRDX1" Gene in BioThings Explorer

>>> ht = Hint()
>>> prdx1_hint = ht.query("PRDX1")
>>> prdx1 = prdx1_hint['Gene'][0]
>>> prdx1

* Now we have the representation of PRDX1 in BTE, let's go ahead and find all chemicals that target genes which associate with PRDX1

>>> fc = FindConnection(input_obj=prdx1, output_obj='ChemicalSubstance', intermediate_nodes=['Gene'])
>>> fc.connect(verbose=True)

* So far, BTE has queried all APIs which could connects from PRDX1 to genes, then to chemical substances. Now we could go ahead and explore the results, e.g. as a pandas data frame, as a graphml file, a reasoner API standard JSON file

>>> fc.display_table_view()
>>> fc.to_graphml('prdx1_chemical.graphml')
>>> fc.to_reasoner_std()

* full jupyer notebook demo is available at the link below

`Finding Marketed Drugs that Might Treat an Unknown Syndrome by Perturbing the Disease Mechanism Pathway <https://github.com/biothings/biothings_explorer/blob/master/jupyter%20notebooks/TIDBIT%2004%20Finding%20Marketed%20Drugs%20that%20Might%20Treat%20an%20Unknown%20Syndrome%20by%20Perturbing%20the%20Disease%20Mechanism%20Pathway.ipynb>`_


More advanced usages
------------------------
* For more complicated examples, please check out jupyter notebooks at:

1. `Finding New Uses for Existing Drugs to Treat Parkinson’s Disease.ipynb <https://github.com/biothings/biothings_explorer/blob/master/jupyter%20notebooks/TIDBIT%2002%20Finding%20New%20Uses%20for%20Existing%20Drugs%20to%20Treat%20Parkinson%E2%80%99s%20Disease.ipynb>`_
2. `What drugs might be used to treat hyperphenylalaninemia? <https://github.com/biothings/biothings_explorer/blob/master/jupyter%20notebooks/PREDICT_demo.ipynb>`_
3. `Why does imatinib have an effect on the treatment of chronic myelogenous leukemia (CML)? <https://github.com/biothings/biothings_explorer/blob/master/jupyter%20notebooks/EXPLAIN_demo.ipynb>`_
