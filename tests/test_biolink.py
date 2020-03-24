import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
reg = Registry()


class TestSingleHopQuery(unittest.TestCase):

    # def test_anatomy2gene(self):
    #     # test <chemical, interactswith, anatomy>
    #     seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
    #                                      input_id='uberon',
    #                                      output_cls='Gene',
    #                                      output_id='hgnc',
    #                                      pred='associatedWith',
    #                                      values='UBERON:0004720',
    #                                      registry=reg)
    #     seqd.query()
    #     self.assertTrue('15859' in seqd.G or '21165' in seqd.G)

    # def test_phenotype2pathway(self):
    #     seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
    #                                      input_id='hp',
    #                                      output_cls='Pathway',
    #                                      output_id='reactome',
    #                                      pred='associatedWith',
    #                                      values='HP:0004904',
    #                                      registry=reg)
    #     seqd.query()
    #     self.assertTrue('R-HSA-210745' in seqd.G)

    def test_disease2gene(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='mondo',
                                         output_cls='Gene',
                                         output_id='hgnc',
                                         pred='associatedWith',
                                         values='MONDO:0010997',
                                         registry=reg)
        seqd.query()
        self.assertTrue('6893' in seqd.G)

    def test_disease2pathway(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='mondo',
                                         output_cls='Pathway',
                                         output_id='reactome',
                                         pred='associatedWith',
                                         values='MONDO:0010997',
                                         registry=reg)
        seqd.query()
        self.assertTrue('R-HSA-264870' in seqd.G)

    def test_disease2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='DiseaseOrPhenotypicFeature',
                                         input_id='mondo',
                                         output_cls='PhenotypicFeature',
                                         output_id='mondo',
                                         pred='associatedWith',
                                         values='MONDO:0010997',
                                         registry=reg)
        seqd.query()
        self.assertTrue('HP:0002063' in seqd.G)

    def test_gene2anatomy(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='AnatomicalEntity',
                                         output_id='uberon',
                                         pred='associatedWith',
                                         values='13434',
                                         registry=reg)
        seqd.query()
        self.assertTrue('UBERON:0000988' in seqd.G)

    def test_gene2phenotype(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='PhenotypicFeature',
                                         output_id='hp',
                                         pred='associatedWith',
                                         values='13434',
                                         registry=reg)
        seqd.query()
        self.assertTrue('HP:0040218' in seqd.G)

    def test_geneinteraction(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='entrez',
                                         output_cls='Gene',
                                         output_id='hp',
                                         pred='molecularlyInteractsWith',
                                         values='1838',
                                         registry=reg)
        seqd.query()
        self.assertTrue('5001' in seqd.G)

    def test_pathway2disease(self):
        # test <chemical, interactswith, anatomy>
        seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
                                         input_id='reactome',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='mondo',
                                         pred='associatedWith',
                                         values='R-HSA-210745',
                                         registry=reg)
        seqd.query()
        self.assertTrue('MONDO:0018911' in seqd.G)

    # def test_pathway2phenotype(self):
    #     seqd = SingleEdgeQueryDispatcher(input_cls='Pathway',
    #                                      input_id='reactome',
    #                                      output_cls='PhenotypicFeature',
    #                                      output_id='hp',
    #                                      pred='associatedWith',
    #                                      values='R-HSA-210745',
    #                                      registry=reg)
    #     seqd.query()
    #     self.assertTrue('HP:0004904' in seqd.G)

    def test_phenotype2disease(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='hp',
                                         output_cls='DiseaseOrPhenotypicFeature',
                                         output_id='mondo',
                                         pred='associatedWith',
                                         values='HP:0004904',
                                         registry=reg)
        seqd.query()
        self.assertTrue('MONDO:0010894' in seqd.G)

    def test_phenotype2gene(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='hp',
                                         output_cls='Gene',
                                         output_id='hgnc',
                                         pred='associatedWith',
                                         values='HP:0004904',
                                         registry=reg)
        seqd.query()
        self.assertTrue('4195' in seqd.G)
