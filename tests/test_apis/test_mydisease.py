import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_disease2chemical(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='ChemicalSubstance',
                                         pred='related_to',
                                         values='MONDO:0016575')
        seqd.query()
        self.assertTrue('BW A509U' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0016575']['BW A509U']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_disease2variant(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='SequenceVariant',
                                         pred='related_to',
                                         values='MONDO:0016575')
        seqd.query()
        self.assertTrue('rs137853191' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0016575']['rs137853191']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_disease2gene(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='Gene',
                                         pred='related_to',
                                         values='MONDO:0016575')
        seqd.query()
        self.assertTrue('CCDC151' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0016575']['CCDC151']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_disease2phenotype(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='PhenotypicFeature',
                                         pred='related_to',
                                         values='MONDO:0007965')
        seqd.query()
        self.assertTrue('HP:0007716' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0007965']['HP:0007716']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_disease2bp(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='BiologicalProcess',
                                         pred='related_to',
                                         values='MONDO:0016575')
        seqd.query()
        self.assertTrue('BRAIN DEVELOPMENT' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0016575']['BRAIN DEVELOPMENT']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_chemical2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='MESH',
                                         output_id="MONDO",
                                         input_cls='ChemicalSubstance',
                                         pred='related_to',
                                         values='D015215')
        seqd.query()
        self.assertTrue('MONDO:0016575' in seqd.G)
        edges = seqd.G['MESH:D015215']['MONDO:0016575']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_variant2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='DBSNP',
                                         output_id="MONDO",
                                         input_cls='SequenceVariant',
                                         pred='related_to',
                                         values='rs137853191')
        seqd.query()
        self.assertTrue('MONDO:0016575' in seqd.G)
        edges = seqd.G['DBSNP:rs137853191']['MONDO:0016575']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_phenotype2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='HP',
                                         output_id="MONDO",
                                         input_cls='PhenotypicFeature',
                                         pred='related_to',
                                         values='HP:0002105')
        seqd.query()
        self.assertTrue('MONDO:0008346' in seqd.G)
        edges = seqd.G['HP:HP:0002105']['MONDO:0008346']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_gene2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='SYMBOL',
                                         output_id="MONDO",
                                         input_cls='Gene',
                                         pred='related_to',
                                         values='CCNO')
        seqd.query()
        self.assertTrue('MONDO:0016575' in seqd.G)
        edges = seqd.G['SYMBOL:CCNO']['MONDO:0016575']
        self.assertTrue('mydisease.info API' in get_apis(edges))

    def test_bp2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='GO',
                                         output_id="MONDO",
                                         input_cls='BiologicalProcess',
                                         pred='related_to',
                                         values='GO:0016038')
        seqd.query()
        self.assertTrue('MONDO:0010563' in seqd.G)
        edges = seqd.G['GO:GO:0016038']['MONDO:0010563']
        self.assertTrue('mydisease.info API' in get_apis(edges))