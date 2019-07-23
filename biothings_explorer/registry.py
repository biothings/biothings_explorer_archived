# -*- coding: utf-8 -*-

"""
biothings_explorer.registry
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to parse the
smartAPI registry.
"""
import networkx as nx

from .mapping_parser import MappingParser


class Registry():
    """Construct network"""
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.BIOTHINGS = {'mygene.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mygene.info/schema.json',
                          'myvariant.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/myvariant.info/schema.json',
                          'mychem.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mychem.info/schema.json'}
        self.registry = {}
        self.load_biothings()

    def load_biothings(self):
        self.mp = MappingParser()
        for _api, _url in self.BIOTHINGS.items():
            self.registry[_api] = {}
            self.mp.load_mapping(_url, _api)
            self.registry[_api]['mapping'] = self.mp.mapping
            self.registry[_api]['graph'] = self.mp.connect()
            self.G = nx.compose(self.G, self.registry[_api]['graph'])
        return self.G
