# -*- coding: utf-8 -*-

"""
Make API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>

"""

from itertools import groupby
from operator import itemgetter
from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser
from .config import metadata
from .api_preprocess import APIPreprocess

BIOTHINGS_APIs = [k for k, v in metadata.items() if v.get("api_type") == 'biothings']


class Dispatcher():

    """Dispatch API calls."""

    def __init__(self, registry=None):
        """Load BTE registry and API caller."""
        if not registry:
            self.registry = Registry().registry
        else:
            self.registry = registry.registry
        self.caller = BioThingsCaller()

    def fetch_schema_mapping_file(self, api):
        """Fetch schema mapping file from the registry."""
        return self.registry[api]['mapping']

    @staticmethod
    def subset_mapping_file(edges, mapping_file):
        """Only maintain a subset of mapping file based on edge label."""
        mapping_keys = [_item.get('mapping_key') for _item in edges]
        if mapping_keys:
            mapping_keys += ["@type", "@context"]
            return {k: v for (k, v) in mapping_file.items() if k in mapping_keys}
        else:
            return mapping_file

    @staticmethod
    def group_edges(edges):
        """Group edges based on API and API input."""
        grouper = itemgetter("api", "input_field")
        groups = []
        # group all edges based on their API and input_field value
        for _, grp in groupby(sorted(edges, key=grouper), grouper):
            groups.append(list(grp))
        return groups

    def construct_api_calls(self, edge_groups):
        """Construct API calls for apicall module using edge groups."""
        # store all API call inputs
        api_call_inputs = []
        apis = []
        batch_modes = []
        input_values = []
        edges = []
        # loop through each edge group
        for grp in edge_groups:
            outputs = set()
            values = set()
            # loop through edges in each edge group
            for _item in grp:
                api = _item['api']
                input_field = _item['input_field']
                # add output fields
                if isinstance(_item['output_field'], list):
                    for i in _item['output_field']:
                        outputs.add(i)
                else:
                    outputs.add(_item['output_field'])
                # add values
                if isinstance(_item['value'], list):
                    values |= set(_item['value'])
                else:
                    values.add(_item['value'])
            # if API is BioThings API, use batch query feature
            if api in BIOTHINGS_APIs:
                # construct API call inputs for each edge group
                api_call_inputs.append({"api": api,
                                        "input": input_field,
                                        "output": ','.join(outputs),
                                        "values": ','.join(set(values)),
                                        "batch_mode": True,
                                        "query_id": 'API ' + self.api_dict[api]['num'] + '.' + str(self.api_dict[api]['alphas'].pop(0))
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
                                            "batch_mode": False,
                                            "query_id": 'API ' + self.api_dict[api]['num'] + '.' + str(self.api_dict[api]['alphas'].pop(0))
                                            })
                    apis.append(api)
                    batch_modes.append(False)
                    input_values.append(_value)
                    edges.append(grp)
        return (apis, api_call_inputs, batch_modes, input_values, edges)

    def dispatch(self, edges, verbose=False):
        """Send request to and parse response from API."""
        results = {}
        self.unique_apis = set([_edge['api'] for _edge in edges if _edge])
        self.api_dict = {}
        for i, _api in enumerate(list(self.unique_apis)):
            self.api_dict[_api] = {'alphas': list(range(1, 10000)), 'num': str(i + 1)}
        grped_edges = self.group_edges(edges)
        apis, inputs, modes, vals, grped_edges = self.construct_api_calls(grped_edges)
        # print(apis, inputs, modes, vals, grped_edges)
        responses = self.caller.call_apis(inputs, verbose=verbose)
        if verbose:
            print("\n\n==== Step #3: Output normalization ====\n")
        for api, _res, batch, val, edges, _input in zip(apis, responses, modes, vals, grped_edges, inputs):
            _res = APIPreprocess(_res, metadata[api]['api_type'], api).restructure()
            mapping = self.fetch_schema_mapping_file(api)
            subset_mapping = self.subset_mapping_file(edges, mapping)
            _res = OutputParser(_res, subset_mapping, batch, api).parse()
            if not batch:
                # preprocess biolink results
                # if val is not present in results dict and _res is not empty
                if not _res:
                    if verbose:
                        print("{} {}: No hits".format(_input['query_id'], api))
                    continue
                if val not in results:
                    results[val] = {}
                # loop through API call response
                hits_cnt = 0
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
                        if isinstance(v, list):
                            hits_cnt += len(v)
                            for _v in v:
                                if isinstance(_v, dict):
                                    _v.update({"$api": edges[0]['api']})
                                    results[val][k1].append(_v)
                                else:
                                    item = {"@type": edges[0]['output_type'],
                                        edges[0]['output_id']: [_v],
                                        "$source": edges[0]['api'], "$api": edges[0]['api']}
                                    results[val][k1].append(item)
                        elif isinstance(v, dict):
                            hits_cnt += 1
                            v.update({"$api": edges[0]['api']})
                            results[val][k1].append(v)
                        else:
                            hits_cnt += 1
                            item = {"@type": edges[0]['output_type'],
                                    edges[0]['output_id']: [v],
                                    "$source": edges[0]['api'],
                                    "$api": edges[0]['api']}
                            results[val][k1].append(item)
                if verbose:
                    if hits_cnt > 0:
                        print("{} {}: {} hits".format(_input['query_id'], api, hits_cnt))
                    else:
                        print("{} {}: No hits".format(_input['query_id'], api))
            else:
                if not _res:
                    if verbose:
                        print("{} {}: No hits".format(_input['query_id'], api))
                    continue
                hits_cnt = 0
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
                            if isinstance(v, list):
                                hits_cnt += len(v)
                                for _v in v:
                                    if isinstance(_v, dict):
                                        _v.update({"$api": edges[0]['api']})
                                        results[m][k1].append(_v)
                                    else:
                                        item = {"@type": edges[0]['output_type'],
                                            edges[0]['output_id']: [_v],
                                            "$source": edges[0]['api'],
                                            "$api": edges[0]['api']}
                                        results[m][k1].append(item)
                            elif isinstance(v, dict):
                                hits_cnt += len(v)
                                v.update({'$api': edges[0]['api']})
                                results[m][k1].append(v)
                            else:
                                hits_cnt += len(v)
                                item = {"@type": edges[0]['output_type'],
                                        edges[0]['output_id']: [v],
                                        "$source": edges[0]['api'],
                                        "$api": edges[0]['api']}
                                results[val][k1].append(item)
                if verbose:
                    if hits_cnt > 0:
                        print("{} {}: {} hits".format(_input['query_id'], api, hits_cnt))
                    else:
                        print("{} {}: No hits".format(_input['query_id'], api))
        return dict(results)
