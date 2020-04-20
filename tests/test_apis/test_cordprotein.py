import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()

class TestSingleHopQuery(unittest.TestCase):

    def test_protein2protein(self):
        """Test protein-protein"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Protein',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('PR:000017296' in seqd.G)
        self.assertTrue('PR:000007563' in seqd.G)

    def test_protein2genomicentity(self):
        """Test protein-genomic_entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='GenomicEntity',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('SO:0002004' in seqd.G)
        self.assertTrue('SO:0002045' in seqd.G)

    def test_protein2chemicalsubstance(self):
        """Test protein-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='ChemicalSubstance',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('APC' in seqd.G)
        self.assertTrue('CHEBI:33893' in seqd.G)

    def test_protein2gene(self):
        """Test protein-gene"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Gene',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('GAPDH' in seqd.G)
        self.assertTrue('ATM' in seqd.G)

    def test_protein2anatomy(self):
        """Test protein-anatomy"""
        seqd = SingleEdgeQueryDispatcher(output_cls='AnatomicalEntity',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue("UBERON:0000180" in seqd.G)
        self.assertTrue("UBERON:0000479" in seqd.G)

    def test_protein2ma(self):
        """Test protein-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(output_cls='MolecularActivity',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue("cytokine activity" in seqd.G)

    def test_protein2bp(self):
        """Test protein-biological_process"""
        seqd = SingleEdgeQueryDispatcher(output_cls='BiologicalProcess',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('gene expression' in seqd.G)

    def test_protein2cc(self):
        """Test protein-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(output_cls='CellularComponent',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('membrane attack complex' in seqd.G)

    def test_protein2cell(self):
        """Test protein-cell"""
        seqd = SingleEdgeQueryDispatcher(output_cls='Cell',
                                         input_cls='Protein',
                                         input_id='PR:000008999',
                                         values='3684')
        seqd.query()
        self.assertTrue('CL:0000094' in seqd.G)

    def test_protein2disease(self):
        """Test protein-disease"""
        seqd = SingleEdgeQueryDispatcher(output_cls='DiseaseOrPhenotypicFeature',
                                         input_cls='Protein',
                                         input_id='pr',
                                         values='PR:000008999')
        seqd.query()
        self.assertTrue('scalp-ear-nipple syndrome' in seqd.G)
