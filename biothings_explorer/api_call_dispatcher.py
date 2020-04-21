# -*- coding: utf-8 -*-

"""
Make API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>

"""

from copy import deepcopy
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

    @staticmethod
    def subset_mapping_file(edges, mapping_file):
        """Only maintain a subset of mapping file based on edge label."""
        mapping_keys = [_item.get('mapping_key') for _item in edges]
        if mapping_keys:
            mapping_keys += ["@type", "@context"]
            return {k: v for (k, v) in mapping_file.items() if k in mapping_keys}
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

    def construct_api_calls(self, edges):
        """Construct API calls for apicall module using edge groups."""
        # store all API call inputs
        internal_query_id = 0
        query_id2inputs_mapping = {}
        for edge in edges:
            if edge.get('supportBatch'):
                edge['value'] = edge['separator'].join(edge['value'])
                edge['internal_query_id'] = internal_query_id
                query_id2inputs_mapping[internal_query_id] = edge
                internal_query_id += 1
            else:
                for val in edge['value']:
                    new_edge = deepcopy(edge)
                    new_edge['value'] = val
                    new_edge['internal_query_id'] = internal_query_id
                    query_id2inputs_mapping[internal_query_id] = new_edge
                    internal_query_id += 1
        return query_id2inputs_mapping

    @staticmethod
    def add_metadata_to_output(operation, res):
        if isinstance(res, dict):
            res.update(
                {
                    "$api": operation['api_name'],
                    "$source": operation.get("source"),
                    "@type": operation['output_type']
                }
            )
            return res
        res = {
            "$api": operation['api_name'],
            "$source": operation.get("source"),
            "@type": operation['output_type'],
            operation['output_id']: [res]
        }
        return res
            

    def dispatch(self, edges, verbose=False):
        """Send request to and parse response from API."""
        results = {}
        self.unique_apis = {_edge['api'] for _edge in edges if _edge}
        self.api_dict = {}
        for i, _api in enumerate(list(self.unique_apis)):
            self.api_dict[_api] = {'alphas': list(range(1, 10000)), 'num': str(i + 1)}
        query_id2inputs_mapping = self.construct_api_calls(edges)
        # print(apis, inputs, modes, vals, grped_edges)
        responses, self.log = self.caller.call_apis(query_id2inputs_mapping.values(), verbose=verbose)
        if verbose:
            print("\n\n==== Step #3: Output normalization ====\n")
        self.log.append("\n\n==== Step #3: Output normalization ====\n")
        for response in responses:
            if response['result'] == {}:
                continue
            output_types = []
            query_id = response['internal_query_id']
            operation = query_id2inputs_mapping[query_id]['operation']
            api_name = query_id2inputs_mapping[query_id]['api']
            if api_name in ['SEMMED API', 'CORD API']:
                output_types = [query_id2inputs_mapping[query_id]['output_type']]
            _res = APIPreprocess(response['result'], operation['api_type'], api_name, output_types).restructure()
            mapping = operation['response_mapping']
            _res = OutputParser(_res, mapping, operation['supportBatch'], api_name, operation['api_type']).parse()
            if not operation['supportBatch']:
                # preprocess biolink results
                # if val is not present in results dict and _res is not empty
                if not _res:
                    if verbose:
                        print("{} {}: No hits".format(query_id, api_name))
                    self.log.append("{} {}: No hits".format(query_id, api_name))
                    continue
                val = query_id2inputs_mapping[query_id]['value']
                if val not in results:
                    results[val] = {}
                # loop through API call response
                hits_cnt = 0
                for k, v in _res.items():
                    # if key is not present in final res, create a list
                    if k not in results[val]:
                        results[val][k] = []
                    if isinstance(v, list):
                        hits_cnt += len(v)
                        for _v in v:
                            _v = self.add_metadata_to_output(operation, _v)
                            results[val][k].append(_v)
                    else:
                        hits_cnt += 1
                        v = self.add_metadata_to_output(operation, v)
                        results[val][k].append(v)
                if verbose:
                    if hits_cnt > 0:
                        print("{} {}: {} hits".format(query_id, api_name, hits_cnt))
                    else:
                        print("{} {}: No hits".format(query_id, api_name))
                if hits_cnt > 0:
                    self.log.append("{} {}: {} hits".format(query_id, api_name, hits_cnt))
                else:
                    self.log.append("{} {}: No hits".format(query_id, api_name))
            else:
                if not _res:
                    if verbose:
                        print("{} {}: No hits".format(query_id, api_name))
                    self.log.append("{} {}: No hits".format(query_id, api_name))
                    continue
                hits_cnt = 0
                for m, n in _res.items():
                    if m not in results:
                        results[m] = {}
                    for k, v in n.items():
                        if k not in results[m]:
                            results[m][k] = []
                        if isinstance(v, list):
                            hits_cnt += len(v)
                            for _v in v:
                                _v = self.add_metadata_to_output(operation, _v)
                                results[m][k].append(_v)
                        elif isinstance(v, dict):
                            v = self.add_metadata_to_output(operation, v)
                            results[m][k].append(v)
                        else:
                            if k == 'query':
                                continue
                            hits_cnt += len(v)
                            v = self.add_metadata_to_output(operation, v)
                            results[m][k].append(v)
                if verbose:
                    if hits_cnt > 0:
                        print("{} {}: {} hits".format(query_id, api_name, hits_cnt))
                    else:
                        print("{} {}: No hits".format(query_id, api_name))
                if hits_cnt > 0:
                    self.log.append("{} {}: {} hits".format(query_id, api_name, hits_cnt))
                else:
                    self.log.append("{} {}: No hits".format(query_id, api_name))
        return (dict(results), self.log)
