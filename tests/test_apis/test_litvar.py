import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_variant2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='DBSNP',
                                         output_cls='Gene',
                                         output_id='SYMBOL',
                                         pred='located_in',
                                         values='rs137852559')
        seqd.query()
        self.assertTrue('SHOX' in seqd.G)
        edges = seqd.G['DBSNP:rs137852559']['SHOX']
        self.assertTrue('LitVar API' in get_apis(edges))