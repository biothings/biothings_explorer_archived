import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher


class TestSingleHopQuery(unittest.TestCase):
    def setUp(self):
        self.reg = Registry()

    def test_anatomy2gene(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
                                         input_id='bts:uberon',
                                         output_cls='Gene',
                                         output_id='bts:hgnc',
                                         pred='bts:associatedWith',
                                         values='UBERON:0004720',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('15859' in seqd.G or '21165' in seqd.G)

    def test_disease2gene(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='Gene',
                                         output_id='bts:hgnc',
                                         pred='bts:associatedWith',
                                         values='MONDO:0010997',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('6893' in seqd.G)

    def test_disease2pathway(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='Pathway',
                                         output_id='bts:reactome',
                                         pred='bts:associatedWith',
                                         values='MONDO:0010997',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('R-HSA-264870' in seqd.G)

    def test_disease2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='bts:mondo',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:mondo',
                                         pred='bts:associatedWith',
                                         values='MONDO:0010997',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('HP:0002063' in seqd.G)

    def test_gene2anatomy(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:entrez',
                                         output_cls='AnatomicalEntity',
                                         output_id='bts:uberon',
                                         pred='bts:associatedWith',
                                         values='13434',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('UBERON:0000988' in seqd.G)

    def test_gene2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:entrez',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:hp',
                                         pred='bts:associatedWith',
                                         values='13434',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('HP:0040218' in seqd.G)

    def test_geneinteraction(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:entrez',
                                         output_cls='Gene',
                                         output_id='bts:hp',
                                         pred='bts:molecularlyInteractsWith',
                                         values='1838',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('5001' in seqd.G)

    def test_pathway2disease(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
                                         input_id='bts:reactome',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='bts:mondo',
                                         pred='bts:associatedWith',
                                         values='R-HSA-210745',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('MONDO:0018911' in seqd.G)
    """
    def test_pathway2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
                                         input_id='bts:reactome',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:hp',
                                         pred='bts:associatedWith',
                                         values='R-HSA-210745',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('HP:0004904' in seqd.G)
    """

    def test_phenotype2disease(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:hp',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='bts:mondo',
                                         pred='bts:associatedWith',
                                         values='HP:0004904',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('MONDO:0010894' in seqd.G)

    def test_phenotype2gene(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:hp',
                                         output_cls='Gene',
                                         output_id='bts:hgnc',
                                         pred='bts:associatedWith',
                                         values='HP:0004904',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('4195' in seqd.G)

"""
    def test_phenotype2pathway(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:hp',
                                         output_cls='Pathway',
                                         output_id='bts:reactome',
                                         pred='bts:associatedWith',
                                         values='HP:0004904',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('R-HSA-210745' in seqd.G)
"""
