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
import time


class IDConverter():
    def __init__(self, registry=None):
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.caller = BioThingsCaller(batch_mode=True)
        self.semantic_type_api_mapping = {'Gene': 'mygene.info',
                                          'Variant': 'myvariant.info',
                                          'ChemicalSubstance': 'mychem.info',
                                          'DiseaseOrPhenotypicFeature': "mydisease.info"}

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

    def get_input_fields(self, mapping_file, _type):
        input_fields = mapping_file.get(_type)
        if isinstance(input_fields, list):
            return input_fields[0]
        else:
            return input_fields

    def convert_ids(self, inputs):
        results = {}
        api_call_inputs = []
        mapping_files = []
        apis = []
        ids_list = []
        types = []
        t1 = time.time()
        for _input in inputs:
            ids, _type, semantic_type = _input
            # convert id to list
            if isinstance(ids, str):
                ids = [ids]
            # make sure all ids in id list is str
            if isinstance(ids, list):
                ids = [str(i) for i in ids]
            api = self.semantic_type_api_mapping.get(semantic_type)
            # if id can not be converted, the equivalent id is itself
            if not api:
                if _type.startswith("bts:"):
                    _type = _type[4:]
                for _id in ids:
                    results[_type + ':' + _id] = {_type: _id}
            else:
                ids_list.append(ids)
                ids = ','.join(ids)
                ids_list.append(ids)
                types.append(_type)
                mapping_file = self.fetch_schema_mapping_file(api)
                mapping_file = self.subset_mapping_file(mapping_file)
                mapping_files.append(mapping_file)
                apis.append(api)
                if self.get_input_fields(mapping_file, _type):
                    api_call_inputs.append({"api": api,
                                            "input": self.get_input_fields(mapping_file, _type),
                                            "output": self.get_output_fields(mapping_file),
                                            "values": ids,
                                            "batch_mode": True
                                            })
                else:
                    if _type.startswith("bts:"):
                        _type = _type[4:]
                    for _id in ids.split(','):
                        results[_type + ':' + _id] = {_type: _id}
        t2 = time.time()
        # make API calls asynchronously and gather all outputs
        responses = self.caller.call_apis(api_call_inputs)
        t3 = time.time()
        # loop through outputs
        for _res, _map, _api, _ids, _type in zip(responses, mapping_files,
                                                 apis, ids_list, types):
            t4 = time.time()
            # restructure API output based on mapping file
            new_res = OutputParser(_res, _map, True, _api).parse()
            t5 = time.time()
            # remove "@context" and "@type" from result
            for k, v in new_res.items():
                if '@context' in v:
                    v.pop("@context")
                if '@type' in v:
                    v.pop("@type")
                if _type.startswith("bts:"):
                    _type = _type[4:]
                # remove duplicates
                for m, n in v.items():
                    if n and type(n) == list:
                        v[m] = list(set(n))
                # after removing @context and @type, check if the dict is empty
                if v:
                    results[_type + ':' + k] = v
                # if the dict is empty, just return itself as its value
                else:
                    results[_type + ':' + k] = {_type: k}
        return results
