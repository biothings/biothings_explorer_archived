import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher


class TestSingleHopQuery(unittest.TestCase):
    def setUp(self):
        self.reg = Registry()

    def test_chemical2metabolizer(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:drugbank',
                                         output_cls='Gene',
                                         output_id='bts:symbol',
                                         pred='bts:metabolizedBy',
                                         values='DB00740',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('CYP1A2' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:chembl',
                                         output_cls='Gene',
                                         output_id='bts:symbol',
                                         pred='bts:metabolizedBy',
                                         values='CHEMBL744',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('CYP1A2' in seqd.G)

    def test_chemical2targets(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:drugbank',
                                         output_cls='Gene',
                                         output_id='bts:symbol',
                                         pred='bts:target',
                                         values='DB00740',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('SCN5A' in seqd.G)
        self.assertTrue('SLC7A11' in seqd.G)
        self.assertTrue('Kcnn2' in seqd.G)
        self.assertFalse('CYP1A2' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:chembl',
                                         output_cls='Gene',
                                         output_id='bts:symbol',
                                         pred='bts:target',
                                         values='CHEMBL744',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('SCN5A' in seqd.G)

    def test_chemical2treatment(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:drugbank',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:treats',
                                         values='DB00740',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0002736' in seqd.G)

    def test_chemical2contraindication(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:drugbank',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:contraindication',
                                         values='DB00740',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0001973' in seqd.G)
        self.assertTrue('C0206061' in seqd.G)


