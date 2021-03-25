import unittest
from biothings_explorer.trapi import TRAPI


class TestTRAPIClass(unittest.TestCase):
    def test_if_url_not_string_raise_exception(self):
        tp = TRAPI()
        with self.assertRaises(Exception):
            tp.url = {"a": "b"}

    def test_url_is_correctly_set(self):
        tp = TRAPI()
        self.assertEqual(tp.url, "https://dev.api.bte.ncats.io/query")
        tp.url = "https://api.bte.ncats.io/query"
        self.assertEqual(tp.url, "https://api.bte.ncats.io/query")

    def test_if_query_graph_not_dict_raise_exception(self):
        tp = TRAPI()
        qg = 1
        with self.assertRaises(Exception):
            tp.query_graph = qg

    def test_query_graph_is_correctly_set(self):
        qg = {"a": "b"}
        tp = TRAPI()
        tp.query_graph = qg
        self.assertEqual(qg, tp.query_graph)
