# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
import time
from collections import defaultdict
import itertools

import networkx as nx
from biothings_schema import Schema

from .utils import load_json_or_yaml


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

    def classify_cls_properties(self, _cls):
        """Classify properties into three categories, e.g. id, links, and other"""
        if _cls in self.cls_prop_clsf:
            return self.cls_prop_clsf[_cls]
        else:
            result = defaultdict(list)
            _cls = self.se.get_class(_cls)
            # list all properties associated with a class
            props = _cls.list_properties(class_specific=False,
                                         group_by_class=False)
            for _prop in [_item['object'] for _item in props]:
                # if property belongs to id
                if _prop.name in self.id_list:
                    result['id'].append(_prop.name)
                # if the range of properties is defined in schema
                elif set([_item.name for _item in _prop.range]) & set(self.defined_clses):
                    result['links'].append(_prop.name)
                else:
                    result['other'].append(_prop.name)
            self.cls_prop_clsf[_cls.label] = result
            return result

    def classify_keys_in_json(self, json_doc):
        """ classify the keys in a json doc"""
        result = defaultdict(list)
        for _key in json_doc.keys():
            if _key in self.defined_clses:
                result['id'].append(_key)
            elif _key in self.linked_prop_list:
                result['links'].append(_key)
        return result

    def connect(self):
        t1 = time.time()
        G = nx.MultiDiGraph()
        # classify the keys in the JSON doc
        clsf = self.classify_keys_in_json(self.mapping)
        # for each "links" properties, find its ids
        for predicate in clsf['links']:
            if "@type" in self.mapping[predicate]:
                sp = self.se.get_property(predicate)
                obj_type = self.mapping[predicate]["@type"]
                obj_clsf = self.classify_keys_in_json(self.mapping[predicate])
                for _edge in itertools.product(clsf['id'], obj_clsf['id']):
                    output_field = self.mapping[predicate][_edge[1]]
                    input_field = self.mapping[_edge[0]]
                    G.add_edge(_edge[0], _edge[1], label=predicate,
                               api=self.api,
                               input_field=input_field,
                               output_field=output_field)
                    G.add_edge(_edge[1], _edge[0], api=self.api,
                               input_field=output_field,
                               output_field=input_field,
                               label=sp.inverse_property)
        t2 = time.time()
        print('Creating network for {} took {}'.format(self.api, t2 - t1))
        return G

    def find_corresponding_output_field(self, object, label):
        return self.mapping[label][object]

    def find_corresponding_input_field(self, subject):
        return self.mapping[subject]
