import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_bp2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Protein',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         pred="related_to",
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('PR:000003959' in seqd.G)
        edges = seqd.G['GO:GO:0019369']['PR:000003959']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(output_cls='GenomicEntity',
                                         input_cls='BiologicalProcess',
                                         pred="related_to",
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('SO:0000999' in seqd.G)
        self.assertTrue('SO:0001853' in seqd.G)

    def test_bp2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('CHEBI:25212' in seqd.G)
        edges = seqd.G['GO:GO:0019369']['CHEBI:25212']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('RPS4X' in seqd.G)
        self.assertTrue('RPS4Y1' in seqd.G)
        edges = seqd.G['GO:GO:0019369']['RPS4X']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(output_cls='AnatomicalEntity',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue("UBERON:0002048" in seqd.G)
        edges = seqd.G['GO:GO:0019369']['UBERON:0002048']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='MolecularActivity',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue("MOP:0000010" in seqd.G)
        edges = seqd.G['GO:GO:0019369']["MOP:0000010"]
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(output_cls='BiologicalProcess',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue("glycerophospholipid metabolic process".upper() in seqd.G)
        edges = seqd.G['GO:GO:0019369']["glycerophospholipid metabolic process".upper()]
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(output_cls='CellularComponent',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('INTRACELLULAR' in seqd.G)
        edges = seqd.G['GO:GO:0019369']['INTRACELLULAR']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))

    def test_bp2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Cell',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('CL:0000097' in seqd.G)

    def test_bp2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_cls='BiologicalProcess',
                                         input_id='GO',
                                         values='GO:0019369')
        seqd.query()
        self.assertTrue('ASTHMA' in seqd.G)
        edges = seqd.G['GO:GO:0019369']['ASTHMA']
        self.assertTrue('CORD Biological Process API' in get_apis(edges))
