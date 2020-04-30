import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_disease2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='DOID',
                                         output_cls='Gene',
                                         output_id='SYMBOL',
                                         pred='related_to',
                                         values='DOID:0111486')
        seqd.query()
        self.assertTrue('UQCRC2' in seqd.G)
        edges = seqd.G['DOID:DOID:0111486']['UQCRC2']
        self.assertTrue('DISEASES API' in get_apis(edges))

    def test_gene2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         output_id='DOID',
                                         input_cls='Gene',
                                         input_id='SYMBOL',
                                         pred='related_to',
                                         values='UQCRC2')
        seqd.query()
        self.assertTrue('DOID:0111486' in seqd.G)
        edges = seqd.G['SYMBOL:UQCRC2']['DOID:0111486']
        self.assertTrue('DISEASES API' in get_apis(edges))
