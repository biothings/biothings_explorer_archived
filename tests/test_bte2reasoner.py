# import unittest
# from biothings_explorer.user_query_dispatcher import (
#     FindConnection,
#     SingleEdgeQueryDispatcher,
# )
# from biothings_explorer.hint import Hint
# import requests
# import json


# class TestFindConnection(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         ht = Hint()
#         cxcr4 = ht.query("CXCR4")["Gene"][0]
#         fc = FindConnection(
#             input_obj=cxcr4, output_obj="ChemicalSubstance", intermediate_nodes=None
#         )
#         fc.connect(verbose=True)
#         cls.response = fc.to_reasoner_std()

#     def test_result_section(cls):
#         res = requests.post(
#             "http://transltr.io:7071/validate_result",
#             headers={"accept": "text/plain", "content-type": "application/json"},
#             data=json.dumps(cls.response["results"]),
#         ).json()
#         cls.assertEqual(res, "Successfully validated")

#     def test_query_graph_section(cls):
#         res = requests.post(
#             "http://transltr.io:7071/validate_querygraph",
#             headers={"accept": "text/plain", "content-type": "application/json"},
#             data=json.dumps(cls.response["query_graph"]),
#         ).json()
#         cls.assertEqual(res, "Successfully validated")

#     def test_knowledge_graph_section(cls):
#         res = requests.post(
#             "http://transltr.io:7071/validate_knowledgegraph",
#             headers={"accept": "text/plain", "content-type": "application/json"},
#             json=json.dumps(cls.response["knowledge_graph"]),
#         ).json()
#         cls.assertEqual(res, "Successfully validated")


# class TestSingleEdgeQuery(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         seqd = SingleEdgeQueryDispatcher(
#             input_cls="ChemicalSubstance",
#             output_cls="Protein",
#             pred="",
#             input_id="CHEMBL.COMPOUND",
#             values="CHEMBL112",
#         )
#         seqd.query()
#         cls.response = seqd.to_reasoner_std()

#     def test_result_section(cls):
#         res = requests.post(
#             "http://transltr.io:7071/validate_result",
#             headers={"accept": "text/plain", "content-type": "application/json"},
#             data=json.dumps(cls.response["results"]),
#         ).json()
#         cls.assertEqual(res, "Successfully validated")

#     def test_query_graph_section(cls):
#         d = json.dumps(cls.response["query_graph"])
#         res = requests.post(
#             "http://transltr.io:7071/validate_querygraph", data=d,
#         ).json()
#         cls.assertEqual(res, "Successfully validated")

#     def test_knowledge_graph_section(cls):
#         res = requests.post(
#             "http://transltr.io:7071/validate_knowledgegraph",
#             headers={"accept": "text/plain", "content-type": "application/json"},
#             data=json.dumps(cls.response["knowledge_graph"]),
#         ).json()
#         cls.assertEqual(res, "Successfully validated")

#     def test_knowledge_graph_node_id(cls):
#         nodes = [item["id"] for item in cls.response["knowledge_graph"]["nodes"]]
#         cls.assertIn("CHEMBL.COMPOUND:CHEMBL112", nodes)
#         cls.assertIn("PR:000011298", nodes)

#     def test_results_node_binding(cls):
#         nodes = [item["kg_id"] for item in cls.response["results"]["node_bindings"]]
#         cls.assertIn("CHEMBL.COMPOUND:CHEMBL112", nodes)
#         cls.assertIn("PR:000011298", nodes)
