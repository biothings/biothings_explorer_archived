import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_variant2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='dbsnp',
                                         output_cls='Gene',
                                         output_id='entrez',
                                         pred='variantAssociatedWithGene',
                                         values='rs539316232',
                                         registry=reg)
        seqd.query()
        self.assertTrue('8816' in seqd.G)

    def test_variant2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='dbsnp',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='omim',
                                         pred='variantAssociatedWithCondition',
                                         values='rs111364296',
                                         registry=reg)
        seqd.query()
        self.assertTrue('145600' in seqd.G)
        self.assertTrue('423' in seqd.G)
        