import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_variant2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='DBSNP',
                                         output_cls='Gene',
                                         output_id='SYMBOL',
                                         pred='located_in',
                                         values='rs1373610867')
        seqd.query()
        self.assertTrue('TTN' in seqd.G)
        edges = seqd.G['DBSNP:rs1373610867']['TTN']
        self.assertTrue('MyVariant.info API' in get_apis(edges))

    def test_variant2disease(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='SequenceVariant',
                                         input_id='DBSNP',
                                         output_cls='Disease',
                                         output_id='OMIM',
                                         pred='related_to',
                                         values='rs137852559')
        seqd.query()
        self.assertTrue('127300' in seqd.G)
        edges = seqd.G['DBSNP:rs137852559']['127300']
        self.assertTrue('MyVariant.info API' in get_apis(edges))

    def test_disease2variant(self):
        seqd = SingleEdgeQueryDispatcher(output_cls='SequenceVariant',
                                         output_id='DBSNP',
                                         input_cls='Disease',
                                         input_id='OMIM',
                                         pred='related_to',
                                         values='127300')
        seqd.query()
        self.assertTrue('rs137852559' in seqd.G)
        edges = seqd.G['OMIM:127300']['rs137852559']
        self.assertTrue('MyVariant.info API' in get_apis(edges))