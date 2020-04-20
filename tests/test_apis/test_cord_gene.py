import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2chemical(self):
        # test <chemical, target, gene>
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Gene',
                                         input_id='entrez',
                                         values='7852')
        seqd.query()
        self.assertTrue('ENFUVIRTIDE' in seqd.G)
        self.assertTrue('ENFUVIRTIDE' in seqd.G)

    def test_chemical2disease(self):
        # test <gene, targetedBy, chemical>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chebi',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         values='CHEBI:6601')
        seqd.query()
        self.assertTrue('non-small cell lung carcinoma (disease)' in seqd.G)
        self.assertTrue('poliomyelitis' in seqd.G)
        self.assertTrue('melanoma (disease)' in seqd.G)

    def test_chemical2gene(self):
        # test <gene, targetedBy, chemical>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chebi',
                                         output_cls='Gene',
                                         values='CHEBI:6601')
        seqd.query()
        self.assertTrue('HMGB1' in seqd.G)
        self.assertTrue('TP53' in seqd.G)
        self.assertTrue('TNF' in seqd.G)
