import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2phenotype(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='HGNC',
                                         output_cls='PhenotypicFeature',
                                         output_id='HP',
                                         pred='related_to',
                                         values='851')
        seqd.query()
        self.assertTrue('HP:0001671' in seqd.G)
        edges = seqd.G['HGNC:851']['HP:0001671']
        self.assertTrue('EBIgene2phenotype API' in get_apis(edges))

    def test_phenotype2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='HP',
                                         output_cls='Gene',
                                         output_id='HGNC',
                                         pred='related_to',
                                         values='HP:0001671')
        seqd.query()
        self.assertTrue('851' in seqd.G)
        edges = seqd.G['HP:HP:0001671']['851']
        self.assertTrue('EBIgene2phenotype API' in get_apis(edges))
