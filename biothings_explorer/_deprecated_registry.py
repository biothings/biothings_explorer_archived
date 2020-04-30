# -*- coding: utf-8 -*-
"""
Storing metadata information and connectivity of APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""
from copy import deepcopy
import networkx as nx
from ._deprecated_mapping_parser import MappingParser
from .config import metadata
from .utils.simple_semmed import semmed
from .utils.cord import cord, SEMANTIC_TYPE_ID_MAPPING
from pathlib import Path
CURRENT_PATH = Path(__file__)

class Registry():

    """Convert metadata information of APIs into a networkx graph."""

    def __init__(self):
        """Initialize networkx graph and load biothings apis."""
        self.G = nx.MultiDiGraph()
        self.registry = {}
        # self.load_biothings()
        self.all_edges_info = self.G.edges(data=True)
        self.all_labels = {d[-1]['label'] for d in self.all_edges_info}
        self.all_inputs = {d[-1]['input_type'] for d in self.all_edges_info}
        self.all_outputs = {d[-1]['output_type'] for d in self.all_edges_info}

    @staticmethod
    def _auto_generate_cord_mapping(doc_type):
        """Auto-generate schema mapping file for all CORD APIs
        
        :param: doc_type: the document type of the specific cord API
        """
        res = {
            "@context": "http://schema.org",
            "@type": doc_type
        }
        for id_type in SEMANTIC_TYPE_ID_MAPPING[doc_type]:
            res[id_type.lower()] = id_type.lower()
        for pred, output_types in cord[doc_type].items():
            res[pred] = []
            for output_type in output_types:
                tmp = {
                    "@type": output_type,
                    "$source": "CORD",
                    "pmd": "associated_with.pmc",
                }
                for input_id_type in SEMANTIC_TYPE_ID_MAPPING[doc_type]:
                    for output_id_type in SEMANTIC_TYPE_ID_MAPPING[output_type]:
                        tmp[output_id_type.lower()] = "associated_with." + output_id_type.lower()
                    tmp["$input"] = input_id_type.lower()
                    res[pred].append(tmp)
        return res

    @staticmethod
    def _auto_generate_semmed_operation_list(doc_type):
        res = []
        for pred, output_types in semmed[doc_type].items():
            for output_type in output_types:
                _id = '-'.join([doc_type, pred, output_type])
                res.append({'$ref': "#/components/x-bte-kgs-operations/" + _id})
        return res

    @staticmethod
    def _auto_generate_semmed_operation(doc_type):
        x_operation_template = {
            "inputSeparator": ",",
            "inputs": [
                {
                    "id": "UMLS"
                }
            ],
            "method": "post",
            "source": "SEMMED",
            "outputs": [
                {
                    "id": "UMLS"
                }
            ],
            "parameters": {
                "fields": ""
            },
            "path": "/query",
            "requestBody": {
                "body": {
                    "q": "{inputs[0]}",
                    "scopes": "umls"
                }
            },
            "supportBatch": True,
            "response_mapping": {
                "$ref": ""
            }
        }
        res = {}
        for pred, output_types in semmed[doc_type].items():
            for output_type in output_types:
                _id = '-'.join([doc_type, pred, output_type])
                tmp = deepcopy(x_operation_template)
                tmp['parameters']['fields'] = pred
                tmp['inputs'][0]['semantic'] = doc_type
                tmp['outputs'][0]['semantic'] = output_type
                tmp['predicate'] = pred
                tmp['response_mapping']["$ref"] = '#/components/x-bte-response-mapping/' + _id
                res[_id] = [tmp]
        return res


    @staticmethod
    def _auto_generate_semmed_mapping(doc_type):
        """Auto-generate schema mapping file for all SEMMED APIs
        
        :param: doc_type: the document type of the specific semmed API
        """
        result = {}
        for pred, output_types in semmed[doc_type].items():
            for output_type in output_types:
                _id = '-'.join([doc_type, pred, output_type])
                result[_id] = {
                    "umls": pred + '.umls',
                    "pmid": pred + '.pmid',
                }
        return result

    def load_biothings(self):
        """Load biothings API into registry network graph."""
        # load biothings schema
        self.mp = MappingParser()
        # loop through API metadata
        for _api, _info in metadata.items():
            # use the mapping parser module to load relationship of each API
            # into the network
            if _info.get('api_name') == 'CORD API':
                mapping_file = self._auto_generate_cord_mapping(_info.get('doc_type'))
            elif _info.get('api_name') == 'SEMMED API':
                mapping_file = self._auto_generate_semmed_mapping(_info.get('doc_type'))
            elif 'mapping_url' in _info:
                self.registry[_api] = {}
                mapping_file = Path.joinpath(CURRENT_PATH.parent,
                                             'smartapi/schema', _api + '.json')
            else:
                continue
            self.mp.load_mapping(mapping_file, api=_api)
            self.registry[_api] = {
                'mapping': self.mp.mapping,
                'graph': self.mp.connect(),
                'type': self.mp.type
            }
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
