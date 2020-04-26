import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_disease2gene(self):
        # test disease-gene
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='Gene',
                                         pred='related_to',
                                         values='MONDO:0010997')
        seqd.query()
        self.assertTrue('MAPT' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0010997']['MAPT']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_disease2pathway(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='Pathway',
                                         pred='related_to',
                                         values='MONDO:0010997')
        seqd.query()
        self.assertTrue('CASPASE-MEDIATED CLEAVAGE OF CYTOSKELETAL PROTEINS' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0010997']['CASPASE-MEDIATED CLEAVAGE OF CYTOSKELETAL PROTEINS']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_disease2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         input_id='MONDO',
                                         output_cls='PhenotypicFeature',
                                         pred='related_to',
                                         values='MONDO:0010997')
        seqd.query()
        self.assertTrue('HP:0002063' in seqd.G)
        edges = seqd.G['MONDO:MONDO:0010997']['HP:0002063']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_gene2anatomy(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='NCBIGene',
                                         output_cls='AnatomicalEntity',
                                         output_id='UBERON',
                                         pred='related_to',
                                         values='13434')
        seqd.query()
        self.assertTrue('UBERON:0000988' in seqd.G)
        edges = seqd.G['NCBIGene:13434']['UBERON:0000988']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_gene2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='NCBIGene',
                                         output_cls='PhenotypicFeature',
                                         pred='related_to',
                                         values='13434')
        seqd.query()
        self.assertTrue('HP:0040218' in seqd.G)
        edges = seqd.G['NCBIGene:13434']['HP:0040218']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_geneinteraction(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='NCBIGene',
                                         output_cls='Gene',
                                         pred='physically_interacts_with',
                                         values='1838')
        seqd.query()
        self.assertTrue('HMG20A' in seqd.G)
        edges = seqd.G['NCBIGene:1838']['HMG20A']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_pathway2disease(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
                                         input_id='Reactome',
                                         output_cls='Disease',
                                         pred='related_to',
                                         values='R-HSA-210745')
        seqd.query()
        self.assertTrue('MATURITY ONSET DIABETES MELLITUS IN YOUNG' in seqd.G)
        edges = seqd.G['Reactome:R-HSA-210745']['MATURITY ONSET DIABETES MELLITUS IN YOUNG']
        self.assertTrue('BioLink API' in get_apis(edges))

    # def test_pathway2phenotype(self):
    #     seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
    #                                      input_id='reactome',
    #                                      output_cls='PhenotypicFeature',
    #                                      output_id='hp',
    #                                      pred='related_to',
    #                                      values='R-HSA-210745',
    #                                      registry=reg)
    #     seqd.query()
    #     self.assertTrue('HP:0004904' in seqd.G)

    def test_phenotype2disease(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='HP',
                                         output_cls='Disease',
                                         output_id='MONDO',
                                         pred='related_to',
                                         values='HP:0004904')
        seqd.query()
        self.assertTrue('MONDO:0010894' in seqd.G)
        edges = seqd.G['HP:HP:0004904']['MONDO:0010894']
        self.assertTrue('BioLink API' in get_apis(edges))

    def test_phenotype2gene(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='HP',
                                         output_cls='Gene',
                                         output_id='HGNC',
                                         pred='related_to',
                                         values='HP:0004904')
        seqd.query()
        self.assertTrue('4195' in seqd.G)
        edges = seqd.G['HP:HP:0004904']['4195']
        self.assertTrue('BioLink API' in get_apis(edges))
