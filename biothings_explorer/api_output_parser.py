# -*- coding: utf-8 -*-

"""
biothings_explorer.dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to and receive from APIs. It serves as a glue between "apicall" module and "api_output_parser" module.
"""

from .json_transformer import Transformer
from .utils import load_json_or_yaml

class OutputParser():
    def __init__(self, response, mapping, predicate, api=None):
        self.api = api
        self.response = response
        self.mapping = mapping
        self.predicate = predicate
        self.BIOTHINGS = ['mygene.info', 'myvariant.info', 'mychem.info']

    def parse(self):
        if not self.response:
            return None
        if self.api in self.BIOTHINGS:
            if self.response['total'] == 0:
                return None
            else:
                new_res = []
                for _res in self.response['hits']:
                    transformed_json = Transformer(_res, self.mapping).transform()
                    new_res += transformed_json[self.predicate]
                return new_res
        else:
            return Transformer(self.response, self.mapping).transform()
