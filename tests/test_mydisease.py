import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):

    def test_disease2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:entrez',
                                         pred='bts:associatedWith',
                                         values='C0008780',
                                         registry=reg)
        seqd.query()
        self.assertTrue('10309' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='Gene',
                                         output_id='bts:entrez',
                                         pred='bts:associatedWith',
                                         values='MONDO:0016575',
                                         registry=reg)
        seqd.query()
        self.assertTrue('10309' in seqd.G)

    def test_disease2variant(self):
        # test <disease, associatedwith, variant>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='SequenceVariant',
                                         output_id='bts:rsid',
                                         pred='bts:associatedWith',
                                         values='C0011860',
                                         registry=reg)
        seqd.query()
        self.assertTrue('rs10010131' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='SequenceVariant',
                                         output_id='bts:rsid',
                                         pred='bts:associatedWith',
                                         values='MONDO:0015122',
                                         registry=reg)
        seqd.query()
        self.assertTrue('rs10010131' in seqd.G)

    def test_disease2phenotype(self):
        # test <disease, associatedwith, phenotype>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:hp',
                                         pred='bts:associatedWith',
                                         values='MONDO:0009079',
                                         registry=reg)
        seqd.query()
        self.assertTrue('HP:0000007' in seqd.G)

    def test_disease2chemical(self):
        # test <disease, associatedwith, chemical>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:mesh',
                                         pred='bts:associatedWith',
                                         values='MONDO:0002258',
                                         registry=reg)
        seqd.query()
        self.assertTrue('D014874' in seqd.G)

    def test_disease2bp(self):
        # test <disease, associatedwith, bp>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:go',
                                         pred='bts:associatedWith',
                                         values='MONDO:0015229',
                                         registry=reg)
        seqd.query()
        self.assertTrue('GO:0035082' in seqd.G)