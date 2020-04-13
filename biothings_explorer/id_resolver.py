# -*- coding: utf-8 -*-
"""
Resolving Biomedical Identifiers through BioThings APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>
"""

from .config import metadata
from .registry import Registry
from .apicall import BioThingsCaller


class IDResolver():
    """Resolving Biomedical Identifiers through BioThings APIs."""

    def __init__(self, registry=None):
        """Load BTE registry and BTE API caller.

        :param: registry: BTE registry object
        """
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.caller = BioThingsCaller(batch_mode=True)
        self.semantic_type_api_mapping = {v['doc_type']: k for k, v
                                          in metadata.items()
                                          if 'hint' in v and k != 'umlschem'}

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry.

        :param: api: the name of API.
        """
        return self.registry.registry[api]['mapping']

    def subset_mapping_file(self, mapping_file):
        """Retrieve a subset of the mapping file which only contains ids.

        :param: mapping_file: schema mapping file from smartapi registry
        """
        return {k: v for (k, v) in mapping_file.items() if k
                in (self.registry.mp.id_list + ["name"])}

    @staticmethod
    def get_output_fields(mapping_file):
        fields = []
        for v in mapping_file.values():
            if isinstance(v, list):
                fields += v
            elif isinstance(v, str):
                fields.append(v)
        return ','.join(fields)

    @staticmethod
    def get_input_fields(mapping_file, _type):
        input_fields = mapping_file.get(_type)
        if isinstance(input_fields, list):
            return input_fields[0]
        return input_fields

    def resolve_ids(self, inputs):
        """Main function to resolve identifiers.
        
        :param: inputs: A list of tuples, [(ids, prefix, semantic_type), ...]
        """
        # this parameter stores the final id conversion outputs
        self.results = {}
        self.api_call_inputs = []
        self.mapping_files = []
        self.types = []
        for _input in inputs:
            ids, _type, semantic_type = _input
            # convert id to list
            ids = self.preprocess_ids(ids, _type)
            # if _type == 'efo':
            # ids = [i.split(':')[-1] for i in ids]
            api = self.semantic_type_api_mapping.get(semantic_type)
            # if id can not be converted, the equivalent id is itself
            if not api:
                for _id in ids:
                    self.results[_type + ':' + _id] = {_type: [_id]}
            else:
                self.construct_api_calls(api, _type, ids)
        # make API calls asynchronously and gather all outputs
        self.responses, _ = self.caller.call_apis(self.api_call_inputs,
                                                  size=10,
                                                  dotfield=True)
        self.parse_api_responses()
        return self.results

    def parse_api_responses(self):
        """Parse the API responses from APICall module in BTE."""
        for _res, _map, _type in zip(self.responses,
                                     self.mapping_files,
                                     self.types):
            # if API response is empty, continue
            if not _res:
                continue
            for single_res in _res:
                # if query of the item returns no hit
                if 'notfound' in single_res:
                    self.results[_type + ':' +
                                 single_res['query']] = {_type:
                                                         [single_res['query']]}
                    continue
                new_res = {}
                for k, v in _map.items():
                    if not isinstance(v, list):
                        v = [v]
                    for _v in v:
                        if _v in single_res:
                            val = single_res[_v]
                            if not isinstance(val, list):
                                val = [val]
                            new_res[k] = val
                self.results[_type + ':' + single_res['query']] = new_res

    def construct_api_calls(self, api, _type, ids):
        """Construct API calls for BTE API call module.

        :param: api: name of API
        :param: _type: the prefix type of ids
        :param: ids: the list of identifiers to resolve
        """
        mapping_file = self.fetch_schema_mapping_file(api)
        mapping_file = self.subset_mapping_file(mapping_file)
        if self.get_input_fields(mapping_file, _type):
            for i in range(0, len(ids), 1000):
                self.api_call_inputs.append({"api": api,
                                             "input": self.get_input_fields(
                                                        mapping_file, _type),
                                             "output": self.get_output_fields(
                                                        mapping_file),
                                             "values": ','.join(ids[i:i+1000]),
                                             "batch_mode": True
                                             })
                self.types.append(_type)
                self.mapping_files.append(mapping_file)
        else:
            for _id in ids:
                self.results[_type + ':' + _id] = {_type: [_id]}

    def preprocess_ids(self, ids, _type):
        """Preprocess ids to become a list of strings.

        :param: ids: list of input ids
        :param: _type: the prefix type
        """
        # convert id to list
        if isinstance(ids, str):
            ids = [ids]
        # make sure all ids in id list is str
        for _id in ids:
            if ' ' in str(_id):
                self.results[_type + ':' + str(_id)] = {_type: [str(_id)]}
        ids = [str(i) for i in ids if ' ' not in str(i)]
        return ids
