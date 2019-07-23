# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
import requests


class BioThingsCaller():
    """call biothings APIs"""
    def __init__(self):
        self.url_pattern = {'mygene.info': "http://mygene.info/v3/query",
                            'myvariant.info': 'http://myvariant.info/v1/query',
                            "mychem.info": "http://mychem.info/v1/query"}

    def construct_query_param(self, input_fields, output_fields, value):
        params = 'q={input}:{value}&fields={output}'
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def call_api(self, api, _input, _output, value):
        params = self.construct_query_param(_input, _output, value)
        return requests.get(self.url_pattern[api], params=params).json()
