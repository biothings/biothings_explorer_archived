# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
from collections import defaultdict
from biothings_schema import Schema

from .utils import load_json_or_yaml


class MappingParser():
    """Parse the mapping file between biothings schema and biothings API"""
    BIOTHINGS_SCHEMA_PATH = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'

    def __init__(self, mapping):
        self.mapping = load_json_or_yaml(mapping)
        self.se = Schema(self.BIOTHINGS_SCHEMA_PATH)
        # get all properties defined in biothings schema JSON-LD file
        self.defined_properties = [_item.name for _item in self.se.list_all_defined_properties()]
        # list all properties which are descendants of identifiers
        self.id_list = self.se.get_property("identifier",
                                            output_type="curie").descendant_properties
        # get all classes defined in biothings schema JSON-LD file
        self.defined_clses = [_item.name for _item in self.se.list_all_defined_classes()]

    def classify_cls_properties(self, _cls):
        """Classify properties into three categories, e.g. identifiers, links, and other"""
        result = defaultdict(list)
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
        return result

    def classify_keys_in_json(self, json_doc, rule):
        """ classify the keys in a json doc"""
        result = defaultdict(list)
        for _key in json_doc.keys():
            if _key in rule['id']:
                result['id'].append(_key)
            elif _key in rule['links']:
                result['links'].append(_key)
            else:
                result['other'].append(_key)
        return result





