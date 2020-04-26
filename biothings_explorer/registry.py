# -*- coding: utf-8 -*-
"""
Storing metadata information and connectivity of APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""
import networkx as nx
from .config_new import API_LIST
from .smartapi_parser import SmartAPIParser
from pathlib import Path
CURRENT_PATH = Path(__file__)

class Registry():

    """Convert metadata information of APIs into a networkx graph."""

    def __init__(self):
        """Initialize networkx graph and load biothings apis."""
        self.G = nx.MultiDiGraph()
        self.smp = SmartAPIParser()
        self.registry = {}
        self.api_list = API_LIST
        self.load_smartapis()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = {d[-1]['label'] for d in self.all_edges_info}
        self.all_inputs = {d[-1]['input_type'] for d in self.all_edges_info}
        self.all_outputs = {d[-1]['output_type'] for d in self.all_edges_info}

    def _reload_registry(self):
        """Reconstruct BTE Registry.
        
        note: This one is called everytime the API_LIST changes.
        """
        self.G = nx.MultiDiGraph()
        self.load_smartapis()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = {d[-1]['label'] for d in self.all_edges_info}
        self.all_inputs = {d[-1]['input_type'] for d in self.all_edges_info}
        self.all_outputs = {d[-1]['output_type'] for d in self.all_edges_info}

    def show_all_apis(self):
        """List all APIs in the BTE Registry."""
        return self.api_list

    def remove_apis(self, apis):
        """Remove one or a list of APIs from registry
        
        :param: apis: list of APIs to be removed from BTE Registry.
        """
        if not isinstance(apis, list):
            apis = [apis]
        for api in apis:
            if api in self.api_list:
                self.api_list.remove(api)
                print("{} has been successfully removed!".format(api))
            else:
                raise ValueError("{} is not in the API list.".format(api))
        self._reload_registry()

    def refine_api_list(self, apis):
        """Set the API List.
        
        :params: apis: list of APIs to include in the BTE Registry
        """
        if not isinstance(apis, list):
            apis = [apis]
        self.api_list = []
        for api in apis:
            if api in API_LIST:
                self.api_list.append(api)
            else:
                self.api_list = API_LIST
                self._reload_registry()
                raise ValueError("{} is not in the API list.".format(api))
        self._reload_registry()

    def load_smartapis(self):
        """Load biothings API into registry network graph."""
        # load biothings schema
        # loop through API metadata
        for api in self.api_list:
            smartapi_file = Path.joinpath(CURRENT_PATH.parent,
                                          'smartapi/new_specs', api + '.json')
            self.smp.load_spec(smartapi_file)
            ops = self.smp.fetch_endpoint_info()
            for op in ops:
                self.G.add_edge(
                    op['input_id'],
                    op['output_id'],
                    operation_id=op['id'],
                    label=op['predicate'],
                    api=api,
                    api_type=op['api_type'],
                    input_type=op['input_type'],
                    output_type=op['output_type'],
                    operation=op
                )
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
