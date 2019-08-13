# -*- coding: utf-8 -*-

"""
biothings_explorer.api_call_dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to
and receive from APIs. It serves as a glue between "apicall" module and
 "api_output_parser" module.
"""

from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser


class Dispatcher():
    def __init__(self, edges=None, values=None, batch_mode=False, registry=None):
        self._edges = edges
        if not registry:
            self.registry = Registry().registry
        else:
            self.registry = registry.registry
        self._batch_mode = batch_mode
        self._values = self.preprocess_input_values(values)
        self.caller = BioThingsCaller(batch_mode=batch_mode)

    @property
    def batch_mode(self):
        return self._batch_mode

    @batch_mode.setter
    def batch_mode(self, value):
        self._batch_mode = value
        self._values = self.preprocess_input_values(self._values)

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = self.preprocess_input_values(value)

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, value):
        self._edges = value

    def preprocess_input_values(self, values):
        """Preprocess the input values

        If batch_mode is set to be True, convert input values into a string
        separated by ',' 
        """
        if not self._batch_mode or not values:
            return values
        else:
            if type(values) == str:
                return values
            elif type(values) == list:
                return ','.join(values)
            else:
                raise ValueError('{} should be str or list'.format(values))

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry"""
        return self.registry[api]['mapping']

    def subset_mapping_file(self, edge, mapping_file):
        """Only maintain a subset of mapping file based on edge label"""
        if edge["mapping_key"]:
            return {k:v for (k,v) in mapping_file.items() if k in ["@context", "@type", edge["mapping_key"]]}
        else:
            return mapping_file

    def dispatch(self):
        """send request to and parse response from API"""
        results = {}
        for _edge in self._edges:
            mapping = self.fetch_schema_mapping_file(_edge['api'])
            subset_mapping = self.subset_mapping_file(_edge, mapping)
            self.caller.batch_mode = self._batch_mode
            response = self.caller.call_api(_edge['api'],
                                            _edge['input_field'],
                                            _edge['output_field'],
                                            self._values)
            _res = OutputParser(response, subset_mapping,
                                self._batch_mode,
                                _edge['api']).parse()
            if not self._batch_mode:
                if self.values not in results:
                    results[self.values] = _res
                else:
                    for k, v in _res.items():
                        if k in ["@context", "@type"]:
                            results[self.values][k] = v
                        else:
                            if k not in results[self.values]:
                                results[self.values][k] = []
                            if type(v) == list:
                                results[self.values][k] += v
                            else:
                                results[self.values][k].append(v)
            else:
                for m, n in _res.items():
                    if m not in results:
                        results[m] = n
                    else:
                        for k, v in n.items():
                            if k in ["@context", "@type"]:
                                results[m][k] = v
                            else:
                                if k not in results[m]:
                                    results[m][k] = []
                                if type(v) == list:
                                    results[m][k] += v
                                else:
                                    results[m][k].append(v)
        return dict(results)
