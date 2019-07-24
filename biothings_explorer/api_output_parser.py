# -*- coding: utf-8 -*-

"""
biothings_explorer.dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to and receive from APIs. It serves as a glue between "apicall" module and "api_output_parser" module.
"""
from collections import defaultdict

from .json_transformer import Transformer
from .utils import load_json_or_yaml

class OutputParser():
    def __init__(self, res, mapping, predicate, batch_mode=False, api=None):
        self.api = api
        self.response = res
        self.mapping = mapping
        self.predicate = predicate
        self.batch_mode = batch_mode
        self.BIOTHINGS = ['mygene.info', 'myvariant.info', 'mychem.info']

    def parse_biothings_get_res(self):
        """Parse the API response from biothings API using GET method"""
        if self.response['total'] == 0:
            return None
        else:
            new_res = []
            for _res in self.response['hits']:
                transformed_json = Transformer(_res, self.mapping).transform()
                new_res += transformed_json[self.predicate]
            return new_res

    def parse_biothings_post_res(self):
        """Parse the API response from biothings API using POST method"""
        new_res = defaultdict(list)
        for _res in self.response:
            # handle case where the queried item is not found
            if _res.get('notfound'):
                new_res[_res['query']] = None
            else:
                transformed_json = Transformer(_res, self.mapping).transform()
                new_res[_res['query']] += transformed_json[self.predicate]
        return dict(new_res)

    def parse(self):
        if not self.response:
            return None
        # parse the results from BioThings APIs
        if self.api in self.BIOTHINGS:
            if self.batch_mode:
                return self.parse_biothings_post_res()
            else:
                return self.parse_biothings_get_res()
        # parse the results from non-BioThings APIs
        else:
            return Transformer(self.response, self.mapping).transform()
