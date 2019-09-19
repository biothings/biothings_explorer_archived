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
from .config import metadata
from .utils import restructure_biolink_response
from .config import metadata

BIOTHINGS_APIs = ['mygene.info', 'myvariant.info', 'mychem.info',
                  'mydisease.info', 'semmeddisease', 'semmedanatomy',
                  'semmedbp', 'semmedchemical', 'semmedgene',
                  'semmedphenotype']


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

    def subset_mapping_file(self, edges, mapping_file):
        """Only maintain a subset of mapping file based on edge label"""
        mapping_keys = [_item.get('mapping_key') for _item in edges]
        if mapping_keys:
            mapping_keys += ["@type", "@context"]
            return {k: v for (k, v) in mapping_file.items() if k in mapping_keys}
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
        edges = []
        # loop through each edge group
        for grp in edge_groups:
            outputs = set()
            values = []
            # loop through edges in each edge group
            for _item in grp:
                api = _item['api']
                input_field = _item['input_field']
                # add output fields
                if type(_item['output_field']) == list:
                    for i in _item['output_field']:
                        outputs.add(i)
                else:
                    outputs.add(_item['output_field'])
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
                                        "output": ','.join(outputs),
                                        "values": ','.join(set(values)),
                                        "batch_mode": True
                                        })
                apis.append(api)
                batch_modes.append(True)
                input_values.append(values)
                edges.append(grp)
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
                    edges.append(grp)
        return (apis, api_call_inputs, batch_modes, input_values, edges)

    def dispatch(self, edges):
        """send request to and parse response from API"""
        results = {}
        grped_edges = self.group_edges(edges)
        # print('grped_edges', grped_edges)
        apis, inputs, modes, vals, grped_edges = self.construct_api_calls(grped_edges)
        responses = self.caller.call_apis(inputs)
        for api, _res, batch, val, edges in zip(apis, responses, modes, vals, grped_edges):
            if metadata[api]['api_type'] == 'biolink':
                _res = restructure_biolink_response(_res)
            mapping = self.fetch_schema_mapping_file(api)
            subset_mapping = self.subset_mapping_file(edges, mapping)
            _res = OutputParser(_res, subset_mapping, batch, api).parse()
            if not batch:
                # preprocess biolink results
                # if val is not present in results dict and _res is not empty
                if not _res:
                    continue
                if val not in results:
                    results[val] = {}
                # loop through API call response
                for k, v in _res.items():
                    k1 = k
                    # if key is "@context", "@type", keep the value
                    if k1 in ["@context", "@type"]:
                        results[val][k1] = v
                    else:
                        if edges[0]['label'] != edges[0]['mapping_key']:
                            k1 = edges[0]['label']
                        # if key is not present in final res, create a list
                        if k1 not in results[val]:
                            results[val][k1] = []
                        if type(v) == list:
                            for _v in v:
                                if type(_v) == dict:
                                    _v.update({"$api": edges[0]['api']})
                                    results[val][k1].append(_v)
                                else:
                                    item = {"@type": edges[0]['output_type'],
                                        edges[0]['output_id']: [_v],
                                        "$source": edges[0]['api'], "$api": edges[0]['api']}
                                    results[val][k1].append(item)
                        elif type(v) == dict:
                            v.update({"$api": edges[0]['api']})
                            results[val][k1].append(v)
                        else:
                            item = {"@type": edges[0]['output_type'],
                                    edges[0]['output_id']: [v],
                                    "$source": edges[0]['api'],
                                    "$api": edges[0]['api']}
                            results[val][k1].append(item)
            else:
                if not _res:
                    continue
                for m, n in _res.items():
                    if m not in results:
                        results[m] = {}
                    for k, v in n.items():
                        k1 = k
                        if k1 in ["@context", "@type"]:
                            results[m][k1] = v
                        else:
                            if edges[0]['label'] != edges[0]['mapping_key']:
                                k1 = edges[0]['label']
                            if k1 not in results[m]:
                                results[m][k1] = []
                            if type(v) == list:
                                for _v in v:
                                    if type(_v) == dict:
                                        _v.update({"$api": edges[0]['api']})
                                        results[m][k1].append(_v)
                                    else:
                                        item = {"@type": edges[0]['output_type'],
                                            edges[0]['output_id']: [_v],
                                            "$source": edges[0]['api'],
                                            "$api": edges[0]['api']}
                                        results[m][k1].append(item)
                            elif type(v) == dict:
                                v.update({'$api': edges[0]['api']})
                                results[m][k1].append(v)
                            else:
                                item = {"@type": edges[0]['output_type'],
                                        edges[0]['output_id']: [v],
                                        "$source": edges[0]['api'],
                                        "$api": edges[0]['api']}
                                results[val][k1].append(item)
        return dict(results)
