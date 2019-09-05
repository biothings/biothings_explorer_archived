# -*- coding: utf-8 -*-

"""
biothings_explorer.api_call_dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code that biothings_explorer use to communicate to
and receive from APIs. It serves as a glue between "apicall" module and
 "api_output_parser" module.
"""
from itertools import groupby
from operator import itemgetter
from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser

BIOTHINGS_APIs = ['mygene.info', 'myvariant.info',
                  'mychem.info', 'mydisease.info']


class Dispatcher():
    def __init__(self, registry=None):
        if not registry:
            self.registry = Registry().registry
        else:
            self.registry = registry.registry
        self.caller = BioThingsCaller()

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry"""
        return self.registry[api]['mapping']

    def subset_mapping_file(self, edge, mapping_file):
        """Only maintain a subset of mapping file based on edge label"""
        if edge["mapping_key"]:
            return {k:v for (k,v) in mapping_file.items() if k in ["@context", "@type", edge["mapping_key"]]}
        else:
            return mapping_file

    def group_edges(self, edges):
        """Group edges based on API and API input"""
        grouper = itemgetter("api", "input_field")
        groups = []
        # group all edges based on their API and input_field value
        for key, grp in groupby(sorted(edges, key=grouper), grouper):
            groups.append(list(grp))
        return groups

    def construct_api_calls(self, edge_groups):
        """Construct API calls for apicall module using edge groups"""
        # store all API call inputs
        api_call_inputs = []
        apis = []
        batch_modes = []
        input_values = []
        # loop through each edge group
        for grp in edge_groups:
            outputs = []
            values = []
            # loop through edges in each edge group
            for _item in grp:
                api = _item['api']
                input_field = _item['input_field']
                # add output fields
                outputs.append(_item['output_field'])
                # add values
                if type(_item['value']) == list:
                    values += _item['value']
                else:
                    values.append(_item['value'])
            # if API is BioThings API, use batch query feature
            if api in BIOTHINGS_APIs:
                # construct API call inputs for each edge group
                api_call_inputs.append({"api": api,
                                        "input": input_field,
                                        "output": ','.join(set(outputs)),
                                        "values": ','.join(set(values)),
                                        "batch_mode": True
                                        })
                apis.append(api)
                batch_modes.append(True)
                input_values.append(values)
            # if API is non-BioThings APIs, query each input one by one
            else:
                for _value in values:
                    api_call_inputs.append({"api": api,
                                            "input": input_field,
                                            "output": ','.join(set(outputs)),
                                            "values": _value,
                                            "batch_mode": False
                                            })
                    apis.append(api)
                    batch_modes.append(False)
                    input_values.append(_value)
        return (apis, api_call_inputs, batch_modes, values)

    def dispatch(self, edges):
        """send request to and parse response from API"""
        results = {}
        grped_edges = self.group_edges(edges)
        apis, inputs, modes, vals = self.construct_api_calls(grped_edges)
        responses = self.caller.call_apis(inputs)
        for api, _res, batch, val in zip(apis, responses, modes, vals):
            mapping = self.fetch_schema_mapping_file(api)
            _res = OutputParser(_res, mapping, batch, api).parse()
            if not batch:
                # if val is not present in results dict and _res is not empty
                if val not in results and _res:
                    results[val] = _res
                else:
                    # if result is empty
                    if not _res:
                        continue
                    # loop through API call response
                    for k, v in _res.items():
                        # if key is "@context", "@type", keep the value
                        if k in ["@context", "@type"]:
                            results[val][k] = v
                        else:
                            # if key is not present in final res, create a list
                            if k not in results[val]:
                                results[val][k] = []
                            if type(v) == list:
                                results[val][k] += v
                            else:
                                results[val][k].append(v)
            else:
                if not _res:
                    continue
                for m, n in _res.items():
                    if m not in results:
                        results[m] = n
                    else:
                        for k, v in n.items():
                            if k in ["@context", "@type"]:
                                results[m][k] = v
                            else:
                                if k not in results[m]:
                                    results[m][k] = []
                                if type(v) == list:
                                    results[m][k] += v
                                else:
                                    results[m][k].append(v)
        return dict(results)
