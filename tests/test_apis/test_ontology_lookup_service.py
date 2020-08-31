# import unittest
# from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
# from .utils import get_apis

# class TestSingleHopQuery(unittest.TestCase):

#     def test_disease2disease(self):
#         # test <gene, enableMF, mf>
#         seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
#                                          input_id='DOID',
#                                          output_cls='Disease',
#                                          output_id='DOID',
#                                          pred='has_subclass',
#                                          values='DOID:0050686')
#         seqd.query()
#         self.assertTrue('DOID:193' in seqd.G)
#         edges = seqd.G['DOID:DOID:0050686']['DOID:193']
#         self.assertTrue('Ontology Lookup Service API' in get_apis(edges))
