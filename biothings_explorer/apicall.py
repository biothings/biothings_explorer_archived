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
    def __init__(self, batch=False):
        self.url_pattern = {'mygene.info': "http://mygene.info/v3/query",
                            'myvariant.info': 'http://myvariant.info/v1/query',
                            "mychem.info": "http://mychem.info/v1/query"}
        self.batch = batch

    def construct_query_param(self, input_fields, output_fields, value):
        get_params = 'q={input}:{value}&fields={output}'
        post_params = 'q={value}&scopes={input}&fields={output}'
        params = post_params if self.batch else get_params
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def call_api(self, api, _input, _output, value):
        params = self.construct_query_param(_input, _output, value)
        if not self.batch:
            return requests.get(self.url_pattern[api], params=params).json()
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            return requests.post(self.url_pattern[api],
                                 data=params,
                                 headers=headers).json()
