import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2chemical(self):
        """Test /gene/chemical_substance/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Gene',
                                         input_id='entrez',
                                         values='7852')
        seqd.query()
        self.assertTrue('ENFUVIRTIDE' in seqd.G)
        self.assertTrue('ENFUVIRTIDE' in seqd.G)

    def test_chemical2disease(self):
        """Test /chemical_substance/disease/{chemicalid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chebi',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         values='CHEBI:6601')
        seqd.query()
        self.assertTrue('non-small cell lung carcinoma (disease)' in seqd.G)
        self.assertTrue('poliomyelitis' in seqd.G)
        self.assertTrue('melanoma (disease)' in seqd.G)

    def test_chemical2gene(self):
        """Test /chemical_substance/gene/{chemicalid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chebi',
                                         output_cls='Gene',
                                         values='CHEBI:6601')
        seqd.query()
        self.assertTrue('HMGB1' in seqd.G)
        self.assertTrue('TP53' in seqd.G)
        self.assertTrue('TNF' in seqd.G)

    def test_gene2disease(self):
        """Test /gene/disease/{geneid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         values='7852')
        seqd.query()
        self.assertTrue('epidermodysplasia verruciformis' in seqd.G)
        self.assertTrue('Waldenstrom macroglobulinemia' in seqd.G)

    def test_disease2gene(self):
        """Test /disease/gene/{diseaseid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='mondo',
                                         output_cls='Gene',
                                         values='MONDO:0007926')
        seqd.query()
        self.assertTrue('FBF1' in seqd.G)
        self.assertTrue('UACA' in seqd.G)
        self.assertTrue('CXCR4' in seqd.G)

    def test_disease2chemical(self):
        """Test /disease/chemical_substance/{diseaseid} endpoint"""
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='mondo',
                                         output_cls='ChemicalSubstance',
                                         values='MONDO:0007926')
        seqd.query()
        self.assertTrue('CHLORAMBUCIL' in seqd.G)
        self.assertTrue('flunixin' in seqd.G)
        self.assertTrue('HETASTARCH' in seqd.G)
