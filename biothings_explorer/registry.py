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
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = set([d[-1]['label'] for d in self.all_edges_info])
        self.all_inputs = set([d[0] for d in self.all_edges_info])
        self.all_outputs = set([d[1] for d in self.all_edges_info])

    def load_biothings(self):
        """load biothings API into registry network graph"""
        self.mp = MappingParser()
        for _api, _url in self.BIOTHINGS.items():
            self.registry[_api] = {}
            self.mp.load_mapping(_url, _api)
            self.registry[_api]['mapping'] = self.mp.mapping
            self.registry[_api]['graph'] = self.mp.connect()
            self.G = nx.compose(self.G, self.registry[_api]['graph'])
        return self.G

    def class2id(self, _cls):
        """find identifiers associated with a class"""
        scls = self.mp.se.get_class(_cls, output_type="curie")
        return [_item['curie'] for _item in scls.list_properties(class_specific=False, group_by_class=False) if _item['curie'] in self.mp.id_list]

    def filter_edges(self, input_cls=None, output_cls=None, edge_label=None):
        if edge_label:
            if type(edge_label) == str:
                edge_label = [edge_label]
        else:
            edge_label = self.all_labels
        if not input_cls:
            input_ids = self.all_inputs
        else:
            input_ids = self.class2id(input_cls)
        if not output_cls:
            output_ids = self.all_outputs
        else:
            output_ids = self.class2id(output_cls)
        return [d for u,v,d in self.all_edges_info if u in input_ids and v in output_ids and d['label'] in edge_label]

