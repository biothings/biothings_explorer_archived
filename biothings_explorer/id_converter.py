# -*- coding: utf-8 -*-

"""
biothings_explorer.id_converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to resolve
different identifiers
"""

from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser
from .utils import unlist


class IDConverter():
    def __init__(self, ids, id_type, semantic_type, registry=None):
        self.ids = ids
        self.type = id_type
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.caller = BioThingsCaller(batch_mode=True)
        self.semantic_type = semantic_type
        self.semantic_type_api_mapping = {'Gene': 'mygene.info',
                                          'Variant': 'myvariant.info',
                                          'Chemical': 'mychem.info',
                                          'DiseaseOrPhenotypicFeature': "mydisease.info"}
        self.api = self.semantic_type_api_mapping.get(self.semantic_type)

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry"""
        return self.registry.registry[api]['mapping']

    def subset_mapping_file(self, mapping_file):
        return {k:v for (k,v) in mapping_file.items() if k in (["@context", "@type"] + self.registry.mp.id_list)}

    def get_output_fields(self, mapping_file):
        fields = []
        for k, v in mapping_file.items():
            if k in self.registry.mp.id_list:
                if isinstance(v, list):
                    fields += v
                elif isinstance(v, str):
                    fields.append(v)
        return ','.join(fields)

    def get_input_fields(self, mapping_file):
        input_fields = mapping_file[self.type]
        if isinstance(input_fields, list):
            return input_fields[0]
        else:
            return input_fields

    def convert_id(self):
        if isinstance(self.ids, str):
            self.ids = [self.ids]
        if self.semantic_type not in self.semantic_type_api_mapping:
            result = {}
            for _id in self.ids:
                result[_id] = {self.type: _id}
            return result
        self.ids = ','.join(self.ids)
        mapping_file = self.fetch_schema_mapping_file(self.api)
        mapping_file = self.subset_mapping_file(mapping_file)
        response = self.caller.call_api(self.api,
                                        self.get_input_fields(mapping_file),
                                        self.get_output_fields(mapping_file),
                                        self.ids)
        _res = OutputParser(response, mapping_file,
                            True,
                            self.api).parse()
        for k, v in _res.items():
            if '@context' in v:
                v.pop("@context")
            if '@type' in v:
                v.pop("@type")
        return unlist(_res)
