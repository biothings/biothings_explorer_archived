 # -*- coding: utf-8 -*-

"""
biothings_explorer.dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to and \
    receive from APIs. It serves as a glue between "apicall" module and "api_output_parser" module.
"""
from .json_transformer import Transformer
from .config import metadata


class OutputParser():
    def __init__(self, res, mapping, batch_mode=False, api=None):
        self.api = api
        self.response = res
        self.mapping = mapping
        self.batch_mode = batch_mode
        self.BIOTHINGS = [k for k, v in metadata.items() if v.get("api_type") == 'biothings']

    def parse_biothings_get_res(self):
        """Parse the API response from biothings API using GET method"""
        if self.response['total'] == 0:
            return None
        else:
            new_res = {}
            for _res in self.response['hits']:
                transformed_json = Transformer(_res, self.mapping).transform()
                if isinstance(transformed_json, dict):
                    for k, v in transformed_json.items():
                        if k in ["@context", "@type"]:
                            new_res[k] = v
                        else:
                            if k not in new_res:
                                new_res[k] = []
                            if isinstance(v, list):
                                new_res[k] += v
                            else:
                                new_res[k].append(v)
                else:
                    continue
            return new_res

    def parse_biothings_post_res(self):
        """Parse the API response from biothings API using POST method"""
        new_res = {}
        for _res in self.response:
            if not isinstance(_res, dict):
                continue
            # handle case where the queried item is not found
            if _res.get('notfound'):
                # check if the item is already in final res
                if _res['query'] in new_res:
                    continue
                new_res[_res['query']] = {}
            else:
                if metadata[self.api].get('api_name') == 'semmed':
                    transformed_json = _res
                else:
                    transformed_json = Transformer(_res, self.mapping).transform()
                if _res['query'] not in new_res:
                    new_res[_res['query']] = transformed_json
                else:
                    if isinstance(transformed_json, dict):
                        for k, v in transformed_json.items():
                            if k in ["@context", "@type"]:
                                new_res[_res['query']][k] = v
                            else:
                                if k not in new_res[_res['query']]:
                                    new_res[_res['query']][k] = []
                                if isinstance(v, list):
                                    new_res[_res['query']][k] += v
                                else:
                                    new_res[_res['query']][k].append(v)
        return dict(new_res)

    def parse(self):
        if not self.response:
            return None
        # parse the results from BioThings APIs
        if self.api in self.BIOTHINGS:
            if self.batch_mode:
                return self.parse_biothings_post_res()
            return self.parse_biothings_get_res()
        # parse the results from non-BioThings APIs
        return Transformer(self.response, self.mapping).transform()
