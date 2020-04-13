# import unittest
# from biothings_explorer.registry import Registry
# from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

# reg = Registry()


# class TestSingleHopQuery(unittest.TestCase):

#     def test_interactswith(self):
#         # test <chemical, interactswith, anatomy>
#         seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
#                                          input_id='umls',
#                                          output_cls='AnatomicalEntity',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0076241',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C0233929' in seqd.G)
#         # test <chemical, interactswith, anatomy>
#         seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
#                                          input_id='umls',
#                                          output_cls='AnatomicalEntity',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0038467',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C0042018' in seqd.G)
#         seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
#                                          input_id='umls',
#                                          output_cls='ChemicalSubstance',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0042018',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C0038467' in seqd.G)
#         # test <chemical, interactswith, anatomy>
#         seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
#                                          input_id='umls',
#                                          output_cls='AnatomicalEntity',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0002151',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C0032105' in seqd.G)
#         seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
#                                          input_id='umls',
#                                          output_cls='ChemicalSubstance',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0032105',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C0002151' in seqd.G)
#         # test <chemical, interactswith, bp>
#         seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
#                                          input_id='umls',
#                                          output_cls='BiologicalProcess',
#                                          output_id='umls',
#                                          pred='associatedWith',
#                                          values='C0885444',
#                                          registry=reg)
#         seqd.query()
#         self.assertTrue('C1158226' in seqd.G)
