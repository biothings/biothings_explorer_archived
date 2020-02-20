.. biothings_explorer documentation master file, created by
   sphinx-quickstart on Wed Feb 19 13:46:00 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BioThings Explorer Documentation
************************************************

Introduction
================
BioThings Explorer is an engine for autonomously querying a distributed knowledge graph. The distributed knowledge graph is made up of biomedical APIs that have been annotated with semantically-precise descriptions of their inputs and outputs. The knowledge graph is currently comprised by the APIs in this figure:

.. image:: images/smartapi_metagraph.png
  :width: 800
  :alt: BioThings Explorer Meta Knowledge graph
  :align: center

Installation
================

Install using pip::

    pip install git+https://github.com/biothings/biothings_explorer#egg=biothings_explorer

Documentation for the Code
**************************
.. automodule:: biothings_explorer

Hint
=========================


.. automodule:: biothings_explorer.hint
   :members:

.. autoclass:: Hint
    :members: query

query
==========================
.. automodule:: biothings_explorer.user_query_dispatcher
    :members:

.. autoclass:: biothings_explorer.user_query_dispatcher.FindConnection
    :members: display_node_info


Documentation
=============
.. toctree::
    :maxdepth: 3
    :caption: Documentation



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
