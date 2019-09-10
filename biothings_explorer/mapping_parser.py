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
from biothings_schema import Schema

from .utils import load_json_or_yaml, find_common_path, get_dict_values
from .config import metadata


class MappingParser():
    """Parse the mapping file between biothings schema and biothings API"""
    BIOTHINGS_SCHEMA_PATH = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'

    def __init__(self):
        self.se = Schema(self.BIOTHINGS_SCHEMA_PATH)
        # list all properties which are descendants of identifiers
        self.id_list = self.se.get_property("identifier",
                                            output_type="curie").descendant_properties
        # get all classes defined in biothings schema JSON-LD file
        self.defined_clses = [_item.name for _item in self.se.list_all_defined_classes()]
        # list of properties whose "range" is among defined classes
        self.linked_prop_list = [_prop.name for _prop in self.se.list_all_defined_properties() if set([_item.name for _item in _prop.range]) & set(self.defined_clses)]
        self.cls_prop_clsf = {}

    def load_mapping(self, mapping, api=None):
        self.mapping = load_json_or_yaml(mapping)
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
        G = nx.MultiDiGraph()
        self.type = self.mapping.get("@type")
        # classify the keys in the JSON doc
        clsf = self.classify_keys_in_json(self.mapping)
        # for each "links" properties, find its ids
        for predicate in clsf['links']:
            if type(self.mapping[predicate]) == dict:
                self.mapping[predicate] = [self.mapping[predicate]]
            for _pred in self.mapping[predicate]:
                if "@type" in _pred:
                    sp = self.se.get_property(predicate)
                    obj_clsf = self.classify_keys_in_json(_pred)
                    common_prefix = find_common_path(get_dict_values(_pred))
                    input_id = [_pred['$input']] if '$input' in _pred else clsf['id']
                    source = _pred['$source'] if '$source' in _pred else self.api
                    for _edge in itertools.product(input_id, obj_clsf['id']):
                        output_field = _pred[_edge[1]]
                        input_field = self.mapping[_edge[0]]
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
                          inverse_property = None if not sp.inverse_property else sp.inverse_property.name
                          if not inverse_property:
                              print(predicate)
                          G.add_edge(_edge[1], _edge[0], api=self.api,
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
