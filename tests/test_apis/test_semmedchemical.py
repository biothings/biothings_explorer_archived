import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):


    def test_chemical2chemicalsubstance(self):
        """Test chemical-chemical"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='ChemicalSubstance',
                                         pred='physically_interacts_with',
                                         input_id='UMLS',
                                         values='C0043716')
        seqd.query()
        self.assertTrue('THYMIDINE' in seqd.G)
        edges = seqd.G['UMLS:C0043716']['THYMIDINE']
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2gene(self):
        """Test chemical-gene entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_cls='ChemicalSubstance',
                                         pred='negatively_regulates',
                                         input_id='UMLS',
                                         values='C0043716')
        seqd.query()
        self.assertTrue('C0035547' in seqd.G)
        edges = seqd.G['UMLS:C0043716']['C0035547']
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2disease(self):
        """Test chemical-disease entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_cls='ChemicalSubstance',
                                         pred='treats',
                                         input_id='UMLS',
                                         values='C0043716')
        seqd.query()
        self.assertTrue("Acquired Immunodeficiency".upper() in seqd.G)
        edges = seqd.G['UMLS:C0043716']["Acquired Immunodeficiency".upper()]
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2bp(self):
        """Test chemical-bp entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='BiologicalProcess',
                                         input_cls='ChemicalSubstance',
                                         pred='disrupts',
                                         input_id='UMLS',
                                         values='C0043716')
        seqd.query()
        self.assertTrue("Lymphocyte Activation".upper() in seqd.G)
        edges = seqd.G['UMLS:C0043716']["Lymphocyte Activation".upper()]
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2cc(self):
        """Test chemical-cc entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='CellularComponent',
                                         input_cls='ChemicalSubstance',
                                         pred='affects',
                                         input_id='UMLS',
                                         values="C1122805")
        seqd.query()
        self.assertTrue("Mitochondrial Membrane, Outer".upper() in seqd.G)
        edges = seqd.G['UMLS:C1122805']["Mitochondrial Membrane, Outer".upper()]
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2cell(self):
        """Test chemical-cell entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Cell',
                                         input_cls='ChemicalSubstance',
                                         pred='produced_by',
                                         input_id='UMLS',
                                         values='C1137885')
        seqd.query()
        self.assertTrue("C1519477" in seqd.G)
        edges = seqd.G['UMLS:C1137885']["C1519477"]
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))

    def test_chemical2anatomy(self):
        """Test chemical-anatomy entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='AnatomicalEntity',
                                         input_cls='ChemicalSubstance',
                                         pred='affects',
                                         input_id='UMLS',
                                         output_id='UMLS',
                                         values='C0057606')
        seqd.query()
        self.assertTrue("C0005767" in seqd.G)
        edges = seqd.G['UMLS:C0057606']["C0005767"]
        self.assertTrue('SEMMED Chemical API' in get_apis(edges))
