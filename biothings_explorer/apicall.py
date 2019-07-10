# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
import requests

from .registry import Registry
from .mapping_parser import MappingParser


class BioThingsCaller():
    """call biothings APIs"""
    def __init__(self):
        self.url_pattern = {'mygene.info': "http://mygene.info/v3/query",
                            'myvariant.info': 'http://myvariant.info/v1/query',
                            "mychem.info": "http://mychem.info/v1/query"}
        self.registry = Registry()

    def construct_query_param(self, input_fields, output_fields, value):
        params = 'q={input}:{value}&fields={output}'
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def call_api(self, _input, _output, value):
        edge_info = self.registry.G[_input][_output]
        api = edge_info['api']
        self.mp = MappingParser(self.registry.BIOTHINGS[api], api)
        label = edge_info['label']
        input_field = self.mp.find_corresponding_input_field(_input)
        output_field = self.mp.find_corresponding_output_field(_output, label)
        params = self.construct_query_param(input_field, output_field, value)
        return requests.get(self.url_pattern[api], params=params).json()
