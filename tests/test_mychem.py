import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_chemical2metabolizer(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='drugbank',
                                         output_cls='Gene',
                                         output_id='symbol',
                                         pred='metabolizedBy',
                                         values='DB00740',
                                         registry=reg)
        seqd.query()
        self.assertTrue('CYP1A2' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chembl',
                                         output_cls='Gene',
                                         output_id='symbol',
                                         pred='metabolizedBy',
                                         values='CHEMBL744',
                                         registry=reg)
        seqd.query()
        self.assertTrue('CYP1A2' in seqd.G)

    def test_chemical2targets(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='drugbank',
                                         output_cls='Gene',
                                         output_id='symbol',
                                         pred='target',
                                         values='DB00740',
                                         registry=reg)
        seqd.query()
        self.assertTrue('SCN5A' in seqd.G)
        self.assertTrue('SLC7A11' in seqd.G)
        self.assertTrue('Kcnn2' in seqd.G)
        self.assertFalse('CYP1A2' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='chembl',
                                         output_cls='Gene',
                                         output_id='symbol',
                                         pred='target',
                                         values='CHEMBL744',
                                         registry=reg)
        seqd.query()
        self.assertTrue('SCN5A' in seqd.G)

    def test_chemical2treatment(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='drugbank',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='umls',
                                         pred='treats',
                                         values='DB00740',
                                         registry=reg)
        seqd.query()
        self.assertTrue('C0002736' in seqd.G)

    def test_chemical2contraindication(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='drugbank',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='umls',
                                         pred='contraindication',
                                         values='DB00740',
                                         registry=reg)
        seqd.query()
        self.assertTrue('C0001973' in seqd.G)
        self.assertTrue('C0206061' in seqd.G)


