.. _api:

Developer Interface
===================

.. module:: biothings_explorer

This part of the documentation covers all the interfaces of BioThings Explorer. For
parts where Requests depends on external libraries, we document the most
important right here and provide links to the canonical documentation.

Main Interface
--------------

All of Requests' functionality can be accessed by these 7 methods.
They all return an instance of the :class:`Response <Response>` object.

query
==========================
.. automodule:: biothings_explorer.user_query_dispatcher
    :members:

.. autoclass:: biothings_explorer.user_query_dispatcher.FindConnection
    :members: display_node_info