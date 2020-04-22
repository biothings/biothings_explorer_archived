import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_bp2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Protein',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         pred="related_to",
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('PR:000004614' in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['PR:000004614']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(output_cls='GenomicEntity',
                                         input_cls='AnatomicalEntity',
                                         pred="related_to",
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('SO:0000140' in seqd.G)
        self.assertTrue('SO:0000999' in seqd.G)

    def test_bp2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('CHEBI:22563' in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['CHEBI:22563']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))
        

    def test_bp2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('HIF1A' in seqd.G)
        self.assertTrue('AR' in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['HIF1A']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(output_cls='AnatomicalEntity',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue("UBERON:0000057" in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['UBERON:0000057']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='MolecularActivity',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue("MOP:0000568" in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']["MOP:0000568"]
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(output_cls='BiologicalProcess',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue("lipid metabolic process".upper() in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']["lipid metabolic process".upper()]
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(output_cls='CellularComponent',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('MEMBRANE' in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['MEMBRANE']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))

    def test_bp2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Cell',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('CL:0007011' in seqd.G)

    def test_bp2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Disease',
                                         input_cls='AnatomicalEntity',
                                         input_id='UBERON',
                                         values='UBERON:0000013')
        seqd.query()
        self.assertTrue('NEURONITIS' in seqd.G)
        edges = seqd.G['UBERON:UBERON:0000013']['NEURONITIS']
        self.assertTrue('CORD Anatomy API' in get_apis(edges))
