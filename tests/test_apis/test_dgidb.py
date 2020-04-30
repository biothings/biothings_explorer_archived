import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis


class TestSingleHopQuery(unittest.TestCase):

    def test_gene2chemical(self):
        """Test /gene/chemical_substance/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Gene',
                                         pred="physically_interacts_with",
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        self.assertTrue('CARBOPLATIN' in seqd.G)
        edges = seqd.G['NCBIGene:1017']['CARBOPLATIN']
        self.assertTrue('DGIdb API' in get_apis(edges))

    def test_chemical2gene(self):
        """Test /gene/chemical_substance/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         output_cls='Gene',
                                         pred="physically_interacts_with",
                                         input_id='CHEMBL.COMPOUND',
                                         values='CHEMBL744')
        seqd.query()
        self.assertTrue('SCN5A' in seqd.G)
        edges = seqd.G['CHEMBL.COMPOUND:CHEMBL744']['SCN5A']
        self.assertTrue('DGIdb API' in get_apis(edges))