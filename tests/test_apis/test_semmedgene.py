import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):


    def test_gene2chemicalsubstance(self):
        """Test gene-chemical"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Gene',
                                         pred='negatively_regulated_by',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue('ADENOSINE' in seqd.G)
        edges = seqd.G['UMLS:C0248868']['ADENOSINE']
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2gene(self):
        """Test gene-gene entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_cls='Gene',
                                         pred='negatively_regulates',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue('TAF8' in seqd.G)
        edges = seqd.G['UMLS:C0248868']['TAF8']
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2disease(self):
        """Test gene-disease entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_cls='Gene',
                                         pred='prevents',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue("CARDIAC ARRHYTHMIA" in seqd.G)
        edges = seqd.G['UMLS:C0248868']["CARDIAC ARRHYTHMIA"]
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2bp(self):
        """Test gene-bp entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='BiologicalProcess',
                                         input_cls='Gene',
                                         pred='affected_by',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue("Phosphorylation".upper() in seqd.G)
        edges = seqd.G['UMLS:C0248868']["Phosphorylation".upper()]
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2cc(self):
        """Test gene-cc entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='CellularComponent',
                                         input_cls='Gene',
                                         pred='affects',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue("CYTOSKELETON" in seqd.G)
        edges = seqd.G['UMLS:C0248868']["CYTOSKELETON".upper()]
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2cell(self):
        """Test gene-cell entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Cell',
                                         input_cls='Gene',
                                         pred='affects',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue("C0007634" in seqd.G)
        edges = seqd.G['UMLS:C0248868']["C0007634".upper()]
        self.assertTrue('SEMMED Gene API' in get_apis(edges))

    def test_gene2anatomy(self):
        """Test gene-anatomy entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='AnatomicalEntity',
                                         input_cls='Gene',
                                         pred='affects',
                                         input_id='UMLS',
                                         values='C0248868')
        seqd.query()
        self.assertTrue("C0233929" in seqd.G)
        edges = seqd.G['UMLS:C0248868']["C0233929"]
        self.assertTrue('SEMMED Gene API' in get_apis(edges))
