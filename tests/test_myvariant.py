import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher


class TestSingleHopQuery(unittest.TestCase):
    def setUp(self):
        self.reg = Registry()

    def test_variant2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='bts:dbsnp',
                                         output_cls='Gene',
                                         output_id='bts:entrez',
                                         pred='bts:variantAssociatedWithGene',
                                         values='rs539316232',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('8816' in seqd.G)

    def test_variant2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='bts:dbsnp',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='bts:omim',
                                         pred='bts:variantAssociatedWithCondition',
                                         values='rs111364296',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('145600' in seqd.G)
        self.assertTrue('423' in seqd.G)
        