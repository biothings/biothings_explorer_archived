import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_chemical2gene(self):
        # test <chemical, target, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:chembl',
                                         output_cls='Gene',
                                         output_id='bts:entrez',
                                         pred='bts:target',
                                         values='CHEMBL744',
                                         registry=reg)
        seqd.query()
        self.assertTrue('6331' in seqd.G)

    def test_gene2chemical(self):
        # test <gene, targetedBy, chemical>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:symbol',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:chembl',
                                         pred='bts:targetedBy',
                                         values='CXCR4',
                                         registry=reg)
        seqd.query()
        self.assertTrue('CHEMBL518924' in seqd.G)
        self.assertTrue('CHEMBL2104426' in seqd.G)
        self.assertTrue('CHEMBL3545348' in seqd.G)
        self.assertTrue('CHEMBL52333' in seqd.G)
