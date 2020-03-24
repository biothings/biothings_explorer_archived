# -*- coding: utf-8 -*-
"""
Storing metadata information and connectivity of APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""
import networkx as nx
from .mapping_parser import MappingParser
from .config import metadata
from pathlib import Path
import sys
CURRENT_PATH = Path(__file__)

class Registry():

    """Convert metadata information of APIs into a networkx graph."""

    def __init__(self):
        """Initialize networkx graph and load biothings apis."""
        self.G = nx.MultiDiGraph()
        self.registry = {}
        self.load_biothings()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = {d[-1]['label'] for d in self.all_edges_info}
        self.all_inputs = {d[-1]['input_type'] for d in self.all_edges_info}
        self.all_outputs = {d[-1]['output_type'] for d in self.all_edges_info}

    def load_biothings(self):
        """Load biothings API into registry network graph."""
        # load biothings schema
        self.mp = MappingParser()
        # loop through API metadata
        for _api, _info in metadata.items():
            # use the mapping parser module to load relationship of each API
            # into the network
            if 'mapping_url' in _info:
                self.registry[_api] = {}
                if sys.version.startswith('3.5'):
                    self.mp.load_mapping(Path.joinpath(CURRENT_PATH.parent.parent,
                                                       'smartapi/schema', _api + '.json'),
                                                       _api)
                else:
                    self.mp.load_mapping(Path.joinpath(CURRENT_PATH.parent,
                                                       'smartapi/schema', _api + '.json'),
                                                       _api)
                self.registry[_api]['mapping'] = self.mp.mapping
                self.registry[_api]['graph'] = self.mp.connect()
                self.registry[_api]['type'] = self.mp.type
                self.G.add_edges_from(self.registry[_api]['graph'].edges(data=True))
        return self.G

    def filter_edges(self, input_cls=None, output_cls=None, edge_label=None):
        """
        Filter edges based on input, output and label.

        The relationship between bio-entities is represented as a networkx MultiDiGraph \
            in BioThings explorer. This function helps you filter for the relationships of your interest based on input/output/edge info.

        :param: input_cls (str|list|None) : the semantic type(s) of the input.
                   Optional
        :param: output_cls (str|list|None) : the semantic type(s) of the output.
                    Optional
        :param: edge_label (str|list|None) : the relationship between input and output.

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
        elif isinstance(input_cls, str):
            input_cls = [input_cls]
        # if no output_cls is specified, set it as all output types
        if not output_cls:
            output_cls = self.all_outputs
        elif isinstance(output_cls, str):
            output_cls = [output_cls]
        return [d for u,v,d in self.all_edges_info if d['input_type'] in input_cls and d['output_type'] in output_cls and d['label'] in edge_label]
