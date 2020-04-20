# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
from collections import defaultdict
import itertools

import networkx as nx
from .schema_parser import SchemaParser
from .utils.dataload import load_json_or_yaml
from .utils.common import find_longest_common_path, get_dict_values, remove_prefix
from .utils.cord import cord, SEMANTIC_TYPE_ID_MAPPING
from .utils.semmed import semmed
from .config import metadata, PREFIX_TO_REMOVE


class MappingParser():
    """Parse the mapping file between biothings schema and biothings API"""
    BIOTHINGS_SCHEMA_PATH = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'

    def __init__(self):
        self.se = SchemaParser()
        # list all properties which are descendants of identifiers
        self.id_list = self.se.ids
        # get all classes defined in biothings schema JSON-LD file
        self.defined_clses = self.se.clses
        # list of properties whose "range" is among defined classes
        self.linked_prop_list = self.se.properties.keys()
        self.cls_prop_clsf = {}

    def load_mapping(self, mapping, api=None):
        self.mapping = load_json_or_yaml(mapping)
        self.mapping = remove_prefix(self.mapping, PREFIX_TO_REMOVE)
        self.api = api

    def classify_keys_in_json(self, json_doc):
        """ classify the keys in a json doc"""
        result = defaultdict(list)
        for _key in json_doc.keys():
            if _key in self.id_list:
                result['id'].append(_key)
            elif _key in self.linked_prop_list:
                result['links'].append(_key)
        return result

    def connect(self):
        # G is used to store the relationship between input and output in a schema mapping file
        G = nx.MultiDiGraph()
        # get the document type
        self.type = self.mapping.get("@type")
        if metadata[self.api].get('api_name') == 'CORD API':
            for pred, info in cord[self.type].items():
                for output_type in info:
                    for input_id in SEMANTIC_TYPE_ID_MAPPING[self.type]:
                        for output_id in SEMANTIC_TYPE_ID_MAPPING[output_type]:
                            G.add_edge(
                                input_id.lower(), output_id.lower(),
                                label=pred,
                                mapping_key=pred,
                                api=self.api,
                                source='CORD API',
                                input_field=input_id.lower(),
                                input_id=input_id.lower(),
                                input_type=self.type,
                                output_id=output_id.lower(),
                                output_field=pred,
                                output_type=output_type
                            )
        elif metadata[self.api].get('api_name') == 'SEMMED API':
            for pred, info in semmed[self.type].items():
                for output_type in info:
                    G.add_edge(
                        'umls', 'umls',
                        label=pred,
                        mapping_key=pred,
                        api=self.api,
                        source='SEMMED API',
                        input_field='umls',
                        input_id='umls',
                        input_type=self.type,
                        output_id='umls',
                        output_field=pred,
                        output_type=output_type
                    )
        else:
            # classify the keys in the JSON doc into IDs or Links
            clsf = self.classify_keys_in_json(self.mapping)
            # for each "links" properties, find its ids
            for predicate in clsf['links']:
                if isinstance(self.mapping[predicate], dict):
                    self.mapping[predicate] = [self.mapping[predicate]]
                for _pred in self.mapping[predicate]:
                    if "@type" in _pred:
                        sp = self.se.properties.get(predicate)
                        obj_clsf = self.classify_keys_in_json(_pred)
                        common_prefix = find_longest_common_path(get_dict_values(_pred))
                        input_id = [_pred['$input']] if '$input' in _pred else clsf['id']
                        source = _pred['$source'] if '$source' in _pred else self.api
                        for _edge in itertools.product(input_id, obj_clsf['id']):
                            output_field = _pred[_edge[1]]
                            input_field = self.mapping[_edge[0]]
                            if isinstance(input_field, list):
                                input_field = ','.join(input_field)
                            if isinstance(output_field, list):
                                output_field = ','.join(output_field)
                            G.add_edge(_edge[0], _edge[1], label=predicate,
                                    mapping_key=predicate,
                                    api=self.api,
                                    source=source,
                                    input_field=input_field,
                                    input_type=self.mapping["@type"],
                                    input_id=_edge[0],
                                    output_id=_edge[1],
                                    output_type=_pred["@type"],
                                    output_field=common_prefix if common_prefix else output_field)
                            if metadata[self.api].get('api_type') == 'biothings':
                                inverse_property = sp.get('inverse_property')
                                if not inverse_property:
                                    print(predicate)
                                G.add_edge(_edge[1], _edge[0],
                                            api=self.api,
                                            input_field=output_field,
                                            input_type=_pred["@type"],
                                            source=source,
                                            input_id=_edge[1],
                                            output_id=_edge[0],
                                            output_type=self.mapping["@type"],
                                            output_field=input_field,
                                            label=inverse_property,
                                            mapping_key=_edge[0])
        return G
