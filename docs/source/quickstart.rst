.. _quickstart:

Quickstart
===================

Eager to get started? This page gives a good introduction in how to get started with BioThings Explorer.

First, make sure that:
* biothings_explorer is installed.

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