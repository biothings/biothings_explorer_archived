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


class Registry():
    """Construct network"""
    def __init__(self):

        self.G = nx.MultiDiGraph()
        self.registry = {}
        self.load_biothings()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = set([d[-1]['label'] for d in self.all_edges_info])
        self.all_inputs = set([d[-1]['input_type'] for d in self.all_edges_info])
        self.all_outputs = set([d[-1]['output_type'] for d in self.all_edges_info])

    def load_biothings(self):
        """load biothings API into registry network graph"""
        # load biothings schema
        BIOTHINGS_SCHEMA_PATH = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'
        se = Schema(BIOTHINGS_SCHEMA_PATH)
        self.mp = MappingParser(se)
        # loop through API metadata
        for _api, _info in metadata.items():
            # use the mapping parser module to load relationship of each API
            # into the network
            if 'mapping_url' in _info:
                self.registry[_api] = {}
                self.mp.load_mapping(_info['mapping_url'], _api)
                self.registry[_api]['mapping'] = self.mp.mapping
                self.registry[_api]['graph'] = self.mp.connect()
                self.registry[_api]['type'] = self.mp.type
                self.G.add_edges_from(self.registry[_api]['graph'].edges(data=True))
        return self.G

    def class2id(self, _cls):
        """find identifiers associated with a class

        params
        ------
        _cls: str, schema class name
        """
        scls = self.mp.se.get_class(_cls, output_type="curie")
        return [_item['curie'] for _item in scls.list_properties(class_specific=False, group_by_class=False) if _item['curie'] in self.mp.id_list]

    def filter_edges(self, input_cls=None, output_cls=None, edge_label=None):
        """filter edges based on input, output and label

        The relationship between bio-entities is represented as a networkx MultiDiGraph in BioThings explorer. This function helps you filter for the relationships of your interest based on input/output/edge info.

        Params
        ------
        input_cls: str or list or None, the semantic type(s) of the input.
                   Optional
        output_cls: str or list or None, the semantic type(s) of the output.
                    Optional
        edge_label: str or list or None, the relationship between input and
                    output

        """
        if edge_label:
            if isinstance(edge_label, str):
                edge_label = [edge_label]
        # if no edge label is specified, set it as all labels
        else:
            edge_label = self.all_labels
        # if no input_cls is specified, set it as all input types
        if not input_cls:
            input_cls = self.all_inputs
        # if input_cls is str, convert it to list of one element
        elif type(input_cls) == str:
            input_cls = [input_cls]
        # if no output_cls is specified, set it as all output types
        if not output_cls:
            output_cls = self.all_outputs
        elif type(output_cls) == str:
            output_cls = [output_cls]
        return [d for u,v,d in self.all_edges_info if d['input_type'] in input_cls and d['output_type'] in output_cls and d['label'] in edge_label]
