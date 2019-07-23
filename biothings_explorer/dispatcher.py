# -*- coding: utf-8 -*-

"""
biothings_explorer.dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to and receive from APIs. It serves as a glue between "apicall" module and "api_output_parser" module.
"""
from collections import defaultdict

from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser

class Dispatcher():
    def __init__(self, edges, values):
        self.edges = edges
        self.registry = Registry().registry
        self.values = values
        self.caller = BioThingsCaller()

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry"""
        return self.registry[api]['mapping']

    def subset_mapping_file(self, edge, mapping_file):
        """Only maintain a subset of mapping file based on edge label"""
        return {k:v for (k,v) in mapping_file.items() if k in ["@context", "@type", edge["label"]]}

    def dispatch(self):
        results = defaultdict(list)
        for _edge in self.edges.values():
            mapping = self.fetch_schema_mapping_file(_edge['api'])
            subset_mapping = self.subset_mapping_file(_edge, mapping)
            response = self.caller.call_api(_edge['api'],
                                            _edge['input_field'],
                                            _edge['output_field'],
                                            self.values)
            _res = OutputParser(response, subset_mapping,
                                _edge['label'], _edge['api']).parse()
            results[_edge['label']] += _res
        return dict(results)
