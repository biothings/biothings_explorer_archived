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
        """Fetch schema mapping file from the registry.
        
        Parameters
        ----------
        api (str) : the name of API
        """
        return self.registry.registry[api]['mapping']

    def subset_mapping_file(self, mapping_file):
        return {k:v for (k,v) in mapping_file.items() if k in (self.registry.mp.id_list + ["bts:name"])}

    def get_output_fields(self, mapping_file):
        fields = []
        for v in mapping_file.values():
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
        # this parameter stores the final id conversion outputs
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
            for _id in ids:
                if ' ' in str(_id):
                    results[_type[4:] + ':' + str(_id)] = {_type: [str(_id)]}
            if isinstance(ids, list):
                ids = [str(i) for i in ids if ' ' not in str(i)]
            #if _type == 'bts:efo':
            #    ids = [i.split(':')[-1] for i in ids]
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
                    if isinstance(ids, list) and len(ids) > 1000:
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
        responses = self.caller.call_apis(api_call_inputs, size=10, dotfield=True)
        for _res, _map, _type in zip(responses, mapping_files, types):
            if _type.startswith("bts:"):
                _type = _type[4:]
            # if API response is empty, continue
            if not _res:
                continue
            for single_res in _res:
                # if query of the item returns no hit
                if 'notfound' in single_res:
                    results[_type + ':' + single_res['query']] = {'bts:' + _type: [single_res['query']]}
                    continue
                else:
                    new_res = {}
                    for k, v in _map.items():
                        if type(v) != list:
                            v = [v]
                        for _v in v:
                            if _v in single_res:
                                val = single_res[_v]
                                if type(val) != list:
                                    val = [val]
                                new_res[k] = val
                    results[_type + ':' + single_res['query']] = new_res
        return results
