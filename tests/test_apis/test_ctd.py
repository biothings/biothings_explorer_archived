import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2disease(self):
        # test <gene, related_to, disease>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='NCBIGene',
                                         output_cls='Disease',
                                         pred='related_to',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('D000077195' in seqd.G)
        edges = seqd.G['NCBIGene:1017']['D000077195']
        apis = get_apis(edges)
        self.assertTrue('CTD API' in apis)

    def test_chemical2gene(self):
        # test <gene, involvedInBP, bp>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='MESH',
                                         output_cls='Gene',
                                         pred='related_to',
                                         values='D003634',
                                         registry=reg)
        seqd.query()
        self.assertTrue('ABCA1' in seqd.G)
        edges = seqd.G['MESH:D003634']['ABCA1']
        apis = get_apis(edges)
        self.assertTrue('CTD API' in apis)
