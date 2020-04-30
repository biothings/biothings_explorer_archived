import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis


class TestSingleHopQuery(unittest.TestCase):

    def test_gene2chemical(self):
        """Test /gene/chemical_substance/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Gene',
                                         pred="related_to",
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        self.assertTrue('AZD-5438' in seqd.G)
        edges = seqd.G['NCBIGene:1017']['AZD-5438']
        self.assertTrue('OpenTarget API' in get_apis(edges))