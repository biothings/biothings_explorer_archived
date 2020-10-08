# -*- coding: utf-8 -*-
"""
Resolving Biomedical Identifiers through BioThings APIs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>
"""

from .config_new import ID_RESOLVING_APIS
from .apicall import BioThingsCaller


class Hint:
    """Resolving Biomedical Identifiers through BioThings APIs."""

    def __init__(self):
        """Load BTE API caller."""
        self.caller = BioThingsCaller()

    def get_primary_id(self, semantic_type, json_doc):
        """Get the primary id of a biological entity
        
        :param: json_doc: the API output
        :param: semantic_type: the main entity type of the output, e.g. Gene, SequenceVariant
        """
        # parse the id rank info from metadata
        ranks = self.ID_RESOLVING_APIS[semantic_type]["id_ranks"]
        res = {}
        # loop through the id rank list, e.g. ['chembl', 'drugbank', ...]
        # the id rank list is ranked based on priorirty
        for _id in ranks:
            # if an id of higher priority is found, set it as the primary id
            if _id in json_doc:
                res["identifier"] = _id
                res["cls"] = semantic_type
                res["value"] = json_doc[_id]
                break
        return res

    def get_display_message(self, semantic_type, json_doc):
        """Get the primary id of a biological entity
        
        :param: semantic_type: the main entity type of the output, e.g. Gene, SequenceVariant
        :param: json_doc: the output
        """
        # parse the id rank info from metadata
        res = ""
        for _id in self.ID_RESOLVING_APIS[semantic_type]["id_ranks"]:
            if _id in json_doc:
                res += _id + "(" + str(json_doc[_id]) + ") "
        return res.strip(" ")

    @staticmethod
    def get_query_fields(mapping_file):
        """Parse the mapping file to retrieve fields for query"""
        fields = []
        for v in mapping_file.values():
            fields += v
        return ",".join(fields)

    def query(self, _input, semantic_type=None):
        """Main function to resolve identifiers.
        
        :param: _input: any string input
        """
        if semantic_type:
            if semantic_type not in ID_RESOLVING_APIS:
                raise ValueError(
                    "{} is not a valid semantic type to resolve. Available semantic types are {}".format(
                        semantic_type, ",".join(ID_RESOLVING_APIS.keys())
                    )
                )
            self.ID_RESOLVING_APIS = {semantic_type: ID_RESOLVING_APIS[semantic_type]}
        else:
            self.ID_RESOLVING_APIS = ID_RESOLVING_APIS
        self.construct_api_calls(_input)
        # make API calls asynchronously and gather all outputs
        self.responses, _ = self.caller.call_apis(self.api_call_inputs)
        return self.parse_api_responses()

    def parse_api_responses(self):
        """Parse the API responses from APICall module in BTE."""
        # bp,  pathway,  cc, mf shares the same API for id resolving
        TYPE_MAPPING = {
            "bp": "BiologicalProcess",
            "pathway": "Pathway",
            "cc": "CellularComponent",
            "mf": "MolecularActivity",
        }
        parsed_response = {k: [] for k in self.ID_RESOLVING_APIS}
        for _res in self.responses:
            # if API response is empty, continue
            if not _res:
                continue
            semantic_type = _res.get("internal_query_id")
            if not _res.get("result"):
                continue
            for single_res in _res["result"]:
                if single_res.get("notfound"):
                    continue
                tmp = {}
                if single_res.get("type") in TYPE_MAPPING.keys():
                    semantic_type = TYPE_MAPPING[single_res.get("type")]
                mapping = ID_RESOLVING_APIS[semantic_type]["mapping"]
                for k, v in mapping.items():
                    for _v in v:
                        if _v in single_res:
                            val = single_res[_v]
                            if not isinstance(val, list):
                                tmp[k] = val
                            elif len(val) > 0:
                                tmp[k] = val[0]
                            break
                tmp["primary"] = self.get_primary_id(semantic_type, tmp)
                tmp["display"] = self.get_display_message(semantic_type, tmp)
                tmp["type"] = semantic_type
                parsed_response[semantic_type].append(tmp)

        return parsed_response

    def construct_api_calls(self, _id):
        """Construct API calls for BTE API call module.
        """
        self.api_call_inputs = []
        unique_base_urls = set()
        for semantic_type, api_data in self.ID_RESOLVING_APIS.items():
            server_url = api_data.get("url")
            if server_url in unique_base_urls:
                continue
            unique_base_urls.add(server_url)
            query_id = semantic_type
            query_fields = self.get_query_fields(api_data["mapping"])
            if api_data["api_name"] == "geneset API":
                query_id = api_data["api_name"]
                query_fields = "go,umls,name,reactome,wikipathways,kegg,pharmgkb,type"
            self.api_call_inputs.append(
                {
                    "api": api_data["api_name"],
                    "operation": {
                        "server": server_url,
                        "path": "/query",
                        "method": "post",
                        "parameters": {
                            "fields": query_fields,
                            "dotfield": "true",
                            "species": "human",
                            "size": "5",
                        },
                        "requestBody": {
                            "body": {"q": '"{inputs[0]}"', "scopes": query_fields},
                            "header": "application/x-www-form-urlencoded",
                        },
                    },
                    "value": _id,
                    "internal_query_id": query_id,
                }
            )
