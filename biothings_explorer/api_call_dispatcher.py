# -*- coding: utf-8 -*-

"""
Make API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>

"""
from collections import defaultdict
from copy import deepcopy
from itertools import groupby
from operator import itemgetter
from .registry import Registry
from .apicall import BioThingsCaller
from .api_output_parser import OutputParser
from .api_preprocess import APIPreprocess

class Dispatcher:

    """Dispatch API calls."""

    def __init__(self, registry=None):
        """Load BTE registry and API caller."""
        if not registry:
            self.registry = Registry().registry
        else:
            self.registry = registry.registry
        self.caller = BioThingsCaller()

    @staticmethod
    def get_unique_edge_id(edge):
        operation = edge["operation"]
        _id = "-".join(
            [
                str(edge["value"]),
                operation["server"],
                operation["method"],
                operation["path"],
            ]
        )
        request_body = operation.get("requestBody")
        if request_body and request_body.get("body"):
            for k in sorted(request_body.get("body").keys()):
                _id += "-" + k + "-" + str(request_body.get("body")[k])
        parameters = operation.get("parameters")
        if parameters:
            for k in sorted(parameters.keys()):
                _id += "-" + k + "-" + str(parameters[k])
        return _id

    @staticmethod
    def get_all_edges(query_id2inputs_mapping):
        res = []
        for v in query_id2inputs_mapping.values():
            if isinstance(v, list) and len(v) > 0:
                res.append(v[0])
        return res

    @staticmethod
    def group_edges(edges):
        grouper = itemgetter("operation_id")
        new_edges = []
        # group all edges based on their API and input_field value
        for _, grp in groupby(sorted(edges, key=grouper), grouper):
            grp = list(grp)
            new_edge = deepcopy(grp[0])
            values = set()
            for edge in grp:
                if isinstance(edge["value"], list):
                    values |= set(edge["value"])
                else:
                    values.add(edge["value"])
            new_edge["value"] = values
            new_edges.append(new_edge)
        return new_edges

    @staticmethod
    def subset_mapping_file(edges, mapping_file):
        """Only maintain a subset of mapping file based on edge label."""
        mapping_keys = [_item.get("mapping_key") for _item in edges]
        if mapping_keys:
            mapping_keys += ["@type", "@context"]
            return {k: v for (k, v) in mapping_file.items() if k in mapping_keys}
        return mapping_file

    def construct_api_calls(self, edges):
        """Construct API calls for apicall module using edge groups."""
        unique_edge_ids = set()
        edge_id2query_id_mapping = {}
        query_id2inputs_mapping = defaultdict(list)
        edges = self.group_edges(edges)
        for edge in edges:
            api = edge["api"]
            if edge["operation"].get("supportBatch"):
                edge["value"] = edge["operation"]["inputSeparator"].join(edge["value"])
                edge_id = self.get_unique_edge_id(edge)
                if edge_id in unique_edge_ids:
                    internal_query_id = edge_id2query_id_mapping[edge_id]
                else:
                    internal_query_id = (
                        "API "
                        + self.api_dict[api]["num"]
                        + "."
                        + str(self.api_dict[api]["alphas"].pop(0))
                    )
                    edge["internal_query_id"] = internal_query_id
                    edge_id2query_id_mapping[edge_id] = internal_query_id
                    unique_edge_ids.add(edge_id)
                edge["internal_query_id"] = internal_query_id
                query_id2inputs_mapping[internal_query_id].append(edge)
                # internal_query_id += 1
            else:
                for val in edge["value"]:
                    new_edge = deepcopy(edge)
                    new_edge["value"] = val
                    edge_id = self.get_unique_edge_id(new_edge)
                    if edge_id in unique_edge_ids:
                        internal_query_id = edge_id2query_id_mapping[edge_id]
                    else:
                        internal_query_id = (
                            "API "
                            + self.api_dict[api]["num"]
                            + "."
                            + str(self.api_dict[api]["alphas"].pop(0))
                        )
                        edge_id2query_id_mapping[edge_id] = internal_query_id
                        unique_edge_ids.add(edge_id)
                    new_edge["internal_query_id"] = internal_query_id
                    query_id2inputs_mapping[internal_query_id].append(new_edge)
                    # internal_query_id += 1
        return query_id2inputs_mapping

    @staticmethod
    def add_metadata_to_output(operation, res, output_id):
        if isinstance(res, dict):
            if output_id not in res:
                return []
            if not isinstance(res[output_id], list):
                res[output_id] = [res[output_id]]
            new_res = []
            for val in res[output_id]:
                tmp = deepcopy(res)
                tmp[output_id] = val
                tmp.update(
                    {
                        "$api": operation["api_name"],
                        "$source": operation.get("source"),
                        "@type": operation["output_type"],
                    }
                )
                new_res.append(tmp)
            return new_res
        res = {
            "$api": operation["api_name"],
            "$source": operation.get("source"),
            "@type": operation["output_type"],
            operation["output_id"]: [res],
        }
        return [res]

    @staticmethod
    def count_hits(res):
        cnt = 0
        if not res:
            return cnt
        for pred_infos in res.values():
            if pred_infos:
                for info in pred_infos.values():
                    cnt += len(info)
        return cnt

    def dispatch(self, edges, verbose=False, loop=None):
        """Send request to and parse response from API."""
        results = {}
        self.unique_apis = {_edge["api"] for _edge in edges if _edge}
        self.api_dict = {}
        for i, _api in enumerate(list(self.unique_apis)):
            self.api_dict[_api] = {"alphas": list(range(1, 10000)), "num": str(i + 1)}
        query_id2inputs_mapping = self.construct_api_calls(edges)
        # print(apis, inputs, modes, vals, grped_edges)
        responses, self.log = self.caller.call_apis(
            self.get_all_edges(query_id2inputs_mapping), verbose=verbose, loop=loop
        )
        if verbose:
            print("\n\n==== Step #3: Output normalization ====\n")
        self.log.append("\n\n==== Step #3: Output normalization ====\n")
        for response in responses:
            if response["result"] == {}:
                continue
            output_types = []
            query_id = response["internal_query_id"]
            total_hits = 0
            for edge in query_id2inputs_mapping[query_id]:
                operation = edge["operation"]
                api_name = edge["api"]
                if api_name[:4] in ["semm", "cord"]:
                    output_types = [edge["output_type"]]
                _res = APIPreprocess(
                    response["result"], operation["api_type"], api_name, output_types
                ).restructure()
                mapping = operation["response_mapping"]
                _res = OutputParser(
                    _res,
                    mapping,
                    operation["supportBatch"],
                    api_name,
                    operation["api_type"],
                ).parse()
                if not operation["supportBatch"]:
                    # preprocess biolink results
                    # if val is not present in results dict and _res is not empty
                    if not _res:
                        continue
                    val = edge["value"]
                    if val not in results:
                        results[val] = {}
                    # loop through API call response
                    for k, v in _res.items():
                        # if key is not present in final res, create a list
                        if k not in results[val]:
                            results[val][k] = []
                        if isinstance(v, list):
                            for _v in v:
                                _v = self.add_metadata_to_output(
                                    operation, _v, operation["output_id"]
                                )
                                total_hits += len(_v)
                                results[val][k] += _v
                        else:
                            v = self.add_metadata_to_output(
                                operation, v, operation["output_id"]
                            )
                            total_hits += len(v)
                            results[val][k] += v
                else:
                    if not _res:
                        continue
                    for m, n in _res.items():
                        if m not in results:
                            results[m] = {}
                        for k, v in n.items():
                            if k not in results[m]:
                                results[m][k] = []
                            if isinstance(v, list):
                                for _v in v:
                                    _v = self.add_metadata_to_output(
                                        operation, _v, operation["output_id"]
                                    )
                                    total_hits += len(_v)
                                    results[m][k] += _v
                            elif isinstance(v, dict):
                                v = self.add_metadata_to_output(
                                    operation, v, operation["output_id"]
                                )
                                total_hits += len(v)
                                results[m][k] += v
                            else:
                                if k == "query":
                                    continue
                                v = self.add_metadata_to_output(
                                    operation, v, operation["output_id"]
                                )
                                total_hits += len(v)
                                results[m][k] += v
            if verbose:
                if total_hits > 0:
                    print("{} {}: {} hits".format(query_id, api_name, total_hits))
                else:
                    print("{} {}: No hits".format(query_id, api_name))
            if total_hits > 0:
                self.log.append("{} {}: {} hits".format(query_id, api_name, total_hits))
            else:
                self.log.append("{} {}: No hits".format(query_id, api_name))
        return (dict(results), self.log)
