import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

class TestSingleHopQuery(unittest.TestCase):

    def test_chemical2disease(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='CHEMBL.COMPOUND',
                                         output_id="UMLS",
                                         input_cls='ChemicalSubstance',
                                         pred='treats',
                                         values='CHEMBL223228')
        seqd.query()
        self.assertTrue('C0019693' in seqd.G)
        edges = seqd.G['CHEMBL.COMPOUND:CHEMBL223228']['C0019693']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_chemical2contraindicatioin(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_id='CHEMBL.COMPOUND',
                                         output_id="UMLS",
                                         input_cls='ChemicalSubstance',
                                         pred='contraindication',
                                         values='CHEMBL223228')
        seqd.query()
        self.assertTrue('C0015624' in seqd.G)
        edges = seqd.G['CHEMBL.COMPOUND:CHEMBL223228']['C0015624']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_chemical2metabolites(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_id='CHEMBL.COMPOUND',
                                         output_id="SYMBOL",
                                         input_cls='ChemicalSubstance',
                                         pred='metabolic_processing_affected_by',
                                         values='CHEMBL223228')
        seqd.query()
        self.assertTrue('CYP2C19' in seqd.G)
        edges = seqd.G['CHEMBL.COMPOUND:CHEMBL223228']['CYP2C19']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_chemical2targets(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_id='CHEMBL.COMPOUND',
                                         output_id="SYMBOL",
                                         input_cls='ChemicalSubstance',
                                         pred='physically_interacts_with',
                                         values='CHEMBL223228')
        seqd.query()
        self.assertTrue('NR1I2' in seqd.G)
        self.assertTrue('pol' in seqd.G)
        edges = seqd.G['CHEMBL.COMPOUND:CHEMBL223228']['NR1I2']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_disease2chemical(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         output_id='CHEMBL.COMPOUND',
                                         input_id="UMLS",
                                         output_cls='ChemicalSubstance',
                                         pred='treated_by',
                                         values='C0019693')
        seqd.query()
        self.assertTrue('CHEMBL223228' in seqd.G)
        edges = seqd.G['UMLS:C0019693']['CHEMBL223228']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_contraindicatioin2chemical(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                         output_id='CHEMBL.COMPOUND',
                                         input_id="UMLS",
                                         output_cls='ChemicalSubstance',
                                         pred='contraindicated_by',
                                         values='C0015624')
        seqd.query()
        self.assertTrue('CHEMBL223228' in seqd.G)
        edges = seqd.G['UMLS:C0015624']['CHEMBL223228']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_metabolites2chemical(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_id='CHEMBL.COMPOUND',
                                         input_id="SYMBOL",
                                         output_cls='ChemicalSubstance',
                                         pred='metabolize',
                                         values='CYP2C19')
        seqd.query()
        self.assertTrue('CHEMBL223228' in seqd.G)
        edges = seqd.G['SYMBOL:CYP2C19']['CHEMBL223228']
        self.assertTrue('MyChem.info API' in get_apis(edges))

    def test_targets2chemical(self):
        # test <gene, enableMF, mf>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_id='CHEMBL.COMPOUND',
                                         input_id="SYMBOL",
                                         output_cls='ChemicalSubstance',
                                         pred='physically_interacts_with',
                                         values='NR1I2')
        seqd.query()
        self.assertTrue('CHEMBL223228' in seqd.G)
        edges = seqd.G['SYMBOL:NR1I2']['CHEMBL223228']
        self.assertTrue('MyChem.info API' in get_apis(edges))
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_id='CHEMBL.COMPOUND',
                                         input_id="SYMBOL",
                                         output_cls='ChemicalSubstance',
                                         pred='physically_interacts_with',
                                         values='pol')
        seqd.query()
        self.assertTrue('CHEMBL223228' in seqd.G)
        edges = seqd.G['SYMBOL:pol']['CHEMBL223228']
        self.assertTrue('MyChem.info API' in get_apis(edges))