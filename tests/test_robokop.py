import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2genefamily(self):
        # test <Gene, partOf, GeneFamily>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:symbol',
                                         output_cls='GeneFamily',
                                         output_id='bts:panther',
                                         pred='bts:partOf',
                                         values='CXCR4',
                                         registry=reg)
        seqd.query()
        self.assertTrue('PTHR10489' in seqd.G)
