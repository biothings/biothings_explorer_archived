# -*- coding: utf-8 -*-

"""
biothings_explorer.registry
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to parse the
smartAPI registry.
"""
import networkx as nx
from biothings_schema import Schema

from .mapping_parser import MappingParser
from .config import metadata

BIOTHINGS_SCHEMA_PATH = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'


class Registry():
    """Construct network"""
    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.BIOTHINGS = {'mygene.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mygene.info/schema.json',
                          'myvariant.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/myvariant.info/schema.json',
                          'mychem.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mychem.info/schema.json',
                          'mydisease.info': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mydisease.info/schema.json',
                          'semmed': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmed/schema.json',
                          'semmedanatomy': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedanatomy/schema.json',
                          'semmedbp': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedbp/schema.json',
                          'semmedchemical': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedchemical/schema.json',
                          'semmedgene': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedgene/schema.json',
                          'semmedphenotype': 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json'}
        self.registry = {}
        self.load_biothings()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = set([d[-1]['label'] for d in self.all_edges_info])
        self.all_inputs = set([d[-1]['input_type'] for d in self.all_edges_info])
        self.all_outputs = set([d[-1]['output_type'] for d in self.all_edges_info])

    def load_biothings(self):
        """load biothings API into registry network graph"""
        self.se = Schema(BIOTHINGS_SCHEMA_PATH)
        self.mp = MappingParser(self.se)
        for _api, _info in metadata.items():
            if 'mapping_url' in _info:
                self.registry[_api] = {}
                self.mp.load_mapping(_info['mapping_url'], _api)
                self.registry[_api]['mapping'] = self.mp.mapping
                self.registry[_api]['graph'] = self.mp.connect()
                self.registry[_api]['type'] = self.mp.type
                # check why it delete some edges
                # self.G = nx.compose(self.G, self.registry[_api]['graph'])
                self.G.add_edges_from(self.registry[_api]['graph'].edges(data=True))
        return self.G

    def class2id(self, _cls):
        """find identifiers associated with a class"""
        scls = self.mp.se.get_class(_cls, output_type="curie")
        return [_item['curie'] for _item in scls.list_properties(class_specific=False, group_by_class=False) if _item['curie'] in self.mp.id_list]

    def filter_edges(self, input_cls=None, output_cls=None, edge_label=None):
        """filter edges based on input, output and label"""
        if edge_label:
            if isinstance(edge_label, str):
                edge_label = [edge_label]
        else:
            edge_label = self.all_labels
        if not input_cls:
            input_cls = self.all_inputs
        else:
            input_cls = [input_cls]
        if not output_cls:
            output_cls = self.all_outputs
        else:
            output_cls = [output_cls]
        return [d for u,v,d in self.all_edges_info if d['input_type'] in input_cls and d['output_type'] in output_cls and d['label'] in edge_label]
