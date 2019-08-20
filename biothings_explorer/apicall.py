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
    def __init__(self, batch_mode=False):
        self.url_pattern = {'mygene.info': "http://mygene.info/v3/query",
                            'myvariant.info': 'http://myvariant.info/v1/query',
                            "mychem.info": "http://mychem.info/v1/query",
                            "mydisease.info": "http://mydisease.info/v1/query",
                            "semmed": "http://pending.biothings.io/semmed/query"}
        self._batch_mode = batch_mode

    @property
    def batch_mode(self):
        return self._batch_mode

    @batch_mode.setter
    def batch_mode(self, value):
        self._batch_mode = value

    def construct_query_param(self, input_fields, output_fields, value):
        """construct query parameters with input, output and value"""
        get_params = 'q={input}:{value}&fields={output}'
        post_params = 'q={value}&scopes={input}&fields={output}'
        if ',' in input_fields and not self._batch_mode:
            _input = ' OR'.join([(_item + ':' + value) for _item in input_fields.split(',')])
            return get_params.replace('{input}:{value}', _input).replace('{output}', output_fields)
        params = post_params if self._batch_mode else get_params
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def call_api(self, api, _input, _output, value):
        """make api calls"""
        params = self.construct_query_param(_input, _output, value)
        if not self._batch_mode:
            return requests.get(self.url_pattern[api], params=params).json()
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            return requests.post(self.url_pattern[api],
                                 data=params,
                                 headers=headers).json()