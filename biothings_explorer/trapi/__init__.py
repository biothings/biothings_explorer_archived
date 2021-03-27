import requests
import pandas as pd
from .config import LEVEL_1_INFO, LEVEL_2_INFO


class TRAPI:
    def __init__(self):
        self._url = "https://dev.api.bte.ncats.io/v1/query"
        self._query_graph = None
        self._response = None

    @property
    def response(self):
        return self._response

    @property
    def url(self):
        return self._url

    # a setter function
    @url.setter
    def url(self, query_url):
        if not isinstance(query_url, str):
            raise Exception("Url must be a string!")
        self._url = query_url

    @property
    def query_graph(self):
        return self._query_graph

    # a setter function
    @query_graph.setter
    def query_graph(self, qg):
        if not isinstance(qg, dict):
            raise Exception("Query Graph must be a dictionary!")
        self._query_graph = qg

    def query(self, qg=None):
        if not qg:
            qg = self._query_graph
        if not qg:
            raise Exception("Query Graph is not provided.")
        try:
            r = requests.post(self._url, json=qg)
        except:
            raise Exception("Your query fails")
        if r.status_code != 200:
            raise Exception(
                "Your query fails with status code {}. Error is {}".format(
                    r.status_code, r.content
                )
            )
        self._response = r.json()
        return self._response

    def _get_kg_edge_ids(self, qg_edge_id):
        res = set()
        for rec in self._response["message"]["results"]:
            if "edge_bindings" in rec and qg_edge_id in rec["edge_bindings"]:
                for item in rec["edge_bindings"][qg_edge_id]:
                    if "id" in item:
                        res.add(item["id"])
        return res

    def _get_kg_edge_info(self, kg_edge_id):
        res = {}
        if kg_edge_id in self._response["message"]["knowledge_graph"]["edges"]:
            rec = self._response["message"]["knowledge_graph"]["edges"][kg_edge_id]
            res["subject"] = rec.get("subject")
            res.update(self._get_kg_node_info(res["subject"], "subject"))
            res["predicate"] = rec.get("predicate")
            res["object"] = rec.get("object")
            res.update(self._get_kg_node_info(res["object"], "object"))
            for attr in rec.get("attributes", []):
                res[attr["name"]] = attr["value"]
        return res

    def _get_kg_node_info(self, kg_node_id, _type):
        res = {}
        if kg_node_id in self._response["message"]["knowledge_graph"]["nodes"]:
            rec = self._response["message"]["knowledge_graph"]["nodes"][kg_node_id]
            res[_type + "_name"] = rec.get("name")
            res[_type + "_category"] = rec.get("category")
            for attr in rec.get("attributes", []):
                res[_type + "_" + attr["name"]] = attr["value"]
        return res

    def _get_all_edge_info(self, qg_edge_id):
        res = []
        edges = self._get_kg_edge_ids(qg_edge_id)
        for edge in edges:
            res.append(self._get_kg_edge_info(edge))
        return res

    def to_dataframe(self, qg_edge_id, info_level=2):
        if not isinstance(info_level, int) or not info_level in [1, 2, 3]:
            raise Exception("info_level parameter should only be 1 or 2 or 3")
        info = self._get_all_edge_info(qg_edge_id)
        df = pd.DataFrame(info)
        column_names = df.columns.values.tolist()
        if info_level == 1:
            return df[LEVEL_1_INFO].drop_duplicates()
        if info_level == 2:
            return_column_names = list(
                set(column_names).intersection(set(LEVEL_1_INFO + LEVEL_2_INFO))
            )
            return_column_names.sort()
            return df[return_column_names]
        return df
