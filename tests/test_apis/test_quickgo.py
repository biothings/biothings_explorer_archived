import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_ma2ma(self):
        """Test /gene/chemical_substance/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(output_cls='MolecularActivity',
                                         input_cls='MolecularActivity',
                                         output_id="GO",
                                         pred="has_subclass",
                                         input_id='GO',
                                         values='GO:0000082')
        seqd.query()
        self.assertTrue('GO:0031571' in seqd.G)
        edges = seqd.G['GO:GO:0000082']['GO:0031571']
        self.assertTrue('QuickGO API' in get_apis(edges))