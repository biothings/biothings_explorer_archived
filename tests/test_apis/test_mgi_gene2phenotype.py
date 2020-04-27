import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2phenotype(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='MGI',
                                         output_cls='PhenotypicFeature',
                                         output_id='MP',
                                         pred='related_to',
                                         values='MGI:3588207')
        seqd.query()
        self.assertTrue('MP:0000598' in seqd.G)
        edges = seqd.G['MGI:MGI:3588207']['MP:0000598']
        self.assertTrue('MGIgene2phenotype API' in get_apis(edges))

    def test_gene2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         output_id='DOID',
                                         input_cls='Gene',
                                         input_id='MGI',
                                         pred='related_to',
                                         values='MGI:3588207')
        seqd.query()
        self.assertTrue('DOID:0050545' in seqd.G)
        edges = seqd.G['MGI:MGI:3588207']['DOID:0050545']
        self.assertTrue('MGIgene2phenotype API' in get_apis(edges))

    def test_disease2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='DOID',
                                         output_cls='Gene',
                                         output_id='MGI',
                                         pred='related_to',
                                         values='DOID:0050545')
        seqd.query()
        self.assertTrue('MGI:3588207' in seqd.G)
        edges = seqd.G['DOID:DOID:0050545']['MGI:3588207']
        self.assertTrue('MGIgene2phenotype API' in get_apis(edges))

    def test_phenotype2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='MP',
                                         output_cls='Gene',
                                         output_id='MGI',
                                         pred='related_to',
                                         values='MP:0000598')
        seqd.query()
        self.assertTrue('MGI:3588207' in seqd.G)
        edges = seqd.G['MP:MP:0000598']['MGI:3588207']
        self.assertTrue('MGIgene2phenotype API' in get_apis(edges))
