# -*- coding: utf-8 -*-
"""
Resolving Biomedical Identifiers through BioThings APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>
"""

from collections import defaultdict
from .config_new import ID_RESOLVING_APIS
from .apicall import BioThingsCaller


class IDResolver:
    """Resolving Biomedical Identifiers through BioThings APIs."""

    def __init__(self):
        """Load BTE registry and BTE API caller."""
        self.caller = BioThingsCaller()

    @staticmethod
    def fetch_id_mapping_file(semantic_type):
        """Fetch schema mapping file from the registry.

        :param: semantic_type: the id semantic type.
        """
        return ID_RESOLVING_APIS[semantic_type]["mapping"]

    @staticmethod
    def get_output_fields(mapping_file):
        fields = []
        for v in mapping_file.values():
            fields += v
        return ",".join(fields)

    @staticmethod
    def get_input_fields(mapping_file, _type):
        input_fields = mapping_file.get(_type)
        return ",".join(input_fields) if input_fields else None

    def resolve_ids(self, inputs, loop=None):
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
            # if id can not be converted, the equivalent id is itself
            if semantic_type not in ID_RESOLVING_APIS:
                for _id in ids:
                    self.results[_type + ":" + _id] = {_type: [_id]}
            else:
                self.construct_api_calls(semantic_type, _type, ids)
        # make API calls asynchronously and gather all outputs
        self.responses, _ = self.caller.call_apis(self.api_call_inputs, loop=loop)
        self.parse_api_responses()
        return self.results

    def parse_api_responses(self):
        """Parse the API responses from APICall module in BTE."""
        for _res, _map, _type in zip(self.responses, self.mapping_files, self.types):
            # if API response is empty, continue
            if not _res:
                continue
            for single_res in _res["result"]:
                # if query of the item returns no hit
                res_id = _type + ":" + single_res["query"]
                if "notfound" in single_res:
                    self.results[res_id] = {_type: [single_res["query"]]}
                    continue
                if res_id not in self.results:
                    self.results[res_id] = defaultdict(set)
                for k, v in _map.items():
                    for _v in v:
                        if _v in single_res:
                            val = single_res[_v]
                            if not isinstance(val, list):
                                self.results[res_id][k].add(str(val))
                            else:
                                self.results[res_id][k].update(set(val))
            for res_id, resolved_ids in self.results.items():
                for m in resolved_ids.keys():
                    if m == "name":
                        self.results[res_id][m] = sorted(
                            {(str(item)).upper() for item in resolved_ids[m]}
                        )
                    else:
                        self.results[res_id][m] = list(resolved_ids[m])

    def construct_api_calls(self, semantic_type, id_type, ids):
        """Construct API calls for BTE API call module.

        :param: api: name of API
        :param: _type: the prefix type of ids
        :param: ids: the list of identifiers to resolve
        """
        mapping_file = self.fetch_id_mapping_file(semantic_type)
        api = ID_RESOLVING_APIS[semantic_type]["api_name"]
        if self.get_input_fields(mapping_file, id_type):
            for i in range(0, len(ids), 1000):
                self.api_call_inputs.append(
                    {
                        "api": api,
                        "operation": {
                            "server": ID_RESOLVING_APIS[semantic_type]["url"],
                            "path": "/query",
                            "method": "post",
                            "parameters": {
                                "fields": self.get_output_fields(mapping_file),
                                "dotfield": "true",
                                "species": "human",
                            },
                            "requestBody": {
                                "body": {
                                    "q": "{inputs[0]}",
                                    "scopes": self.get_input_fields(
                                        mapping_file, id_type
                                    ),
                                },
                                "header": "application/x-www-form-urlencoded",
                            },
                        },
                        "value": ",".join(ids[i : i + 1000]),
                        "internal_query_id": 1,
                    }
                )
                self.types.append(id_type)
                self.mapping_files.append(mapping_file)
        else:
            for _id in ids:
                self.results[id_type + ":" + _id] = {id_type: [_id]}

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
            if " " in str(_id):
                self.results[_type + ":" + str(_id)] = {_type: [str(_id)]}
        ids = [str(i) for i in ids if " " not in str(i)]
        return ids
