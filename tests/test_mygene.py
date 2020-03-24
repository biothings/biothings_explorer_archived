import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_gene2mf(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='MolecularActivity',
                                         output_id='go',
                                         pred='enablesMF',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('GO:0000287' in seqd.G)

    def test_gene2bp(self):
        # test <gene, involvedInBP, bp>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='BiologicalProcess',
                                         output_id='go',
                                         pred='involvedInBP',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('GO:0000082' in seqd.G)

    def test_gene2pathway(self):
        # test <gene, involvedInpathway, pathway>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='Pathway',
                                         output_id='reactome',
                                         pred='involvedInPathway',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('R-HSA-1266738' in seqd.G)
        self.assertTrue('WP1530' in seqd.G)

    def test_gene2transcript(self):
        # test <gene, hasTranscript, transcript>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='Transcript',
                                         output_id='ensembl',
                                         pred='hasTranscript',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('ENST00000266970' in seqd.G)
        self.assertTrue('ENST00000556276' in seqd.G)

    def test_gene2protein(self):
        # test <gene, hasGeneProduct, protein>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='Protein',
                                         output_id='ensembl',
                                         pred='hasGeneProduct',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('ENSP00000243067' in seqd.G)
        self.assertTrue('ENSP00000450983' in seqd.G)
        self.assertTrue('P24941' in seqd.G)

    def test_gene2homolog(self):
        # test <gene, hasTranscript, transcript>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='Gene',
                                         output_id='mgi',
                                         pred='hasHomolog',
                                         values='1017',
                                         registry=reg)
        seqd.query()
        self.assertTrue('104772' in seqd.G)
        self.assertTrue('FBgn0004107' in seqd.G)
        self.assertTrue('19338' in seqd.G)

