# -*- coding: utf-8 -*-

"""
biothings_explorer.id_converter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to resolve
different identifiers
"""
import time
from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser


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
                                          'DiseaseOrPhenotypicFeature': "mydisease.info",
                                          "AnatomicalEntity": "semmedanatomy",
                                          "PhenotypicFeature": "semmedphenotype",
                                          "Pathway": "pathway",
                                          "MolecularActivity": "mf",
                                          "CellularComponent": "cc",
                                          "BiologicalProcess": "bp",
                                          }

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry"""
        return self.registry.registry[api]['mapping']

    def subset_mapping_file(self, mapping_file):
        return {k:v for (k,v) in mapping_file.items() if k in (self.registry.mp.id_list + ["bts:name"])}

    def get_output_fields(self, mapping_file):
        fields = []
        for k, v in mapping_file.items():
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
        types = []
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
                    results[_type + ':' + _id] = {'bts:' + _type: [_id]}
            else:
                mapping_file = self.fetch_schema_mapping_file(api)
                mapping_file = self.subset_mapping_file(mapping_file)
                if self.get_input_fields(mapping_file, _type):
                    if type(ids) == list and len(ids) > 1000:
                        for i in range(0, len(ids), 1000):
                            api_call_inputs.append({"api": api,
                                                "input": self.get_input_fields(mapping_file, _type),
                                                "output": self.get_output_fields(mapping_file),
                                                "values": ','.join(ids[i:i+1000]),
                                                "batch_mode": True
                                                })
                            types.append(_type)
                            mapping_files.append(mapping_file)
                            apis.append(api)
                    else:
                        api_call_inputs.append({"api": api,
                                                "input": self.get_input_fields(mapping_file, _type),
                                                "output": self.get_output_fields(mapping_file),
                                                "values": ','.join(ids),
                                                "batch_mode": True
                                                })
                        types.append(_type)
                        mapping_files.append(mapping_file)
                        apis.append(api)
                else:
                    if _type.startswith("bts:"):
                        _type = _type[4:]
                    for _id in ids:
                        results[_type + ':' + _id] = {'bts:' + _type: [_id]}
        # make API calls asynchronously and gather all outputs
        responses = self.caller.call_apis(api_call_inputs, size=10)
        # loop through outputs
        for _res, _map, _api, _type in zip(responses, mapping_files,
                                                 apis, types):
            # restructure API output based on mapping file
            new_res = OutputParser(_res, _map, True, _api).parse()
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
                    results[_type + ':' + k] = {'bts:' + _type: [k]}
        return results
