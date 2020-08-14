import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_ma2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="MolecularActivity",
            input_id="GO",
            pred="related_to",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("PR:000015198" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["PR:000015198"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="MolecularActivity",
            pred="related_to",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("SO:0000121" in seqd.G)
        self.assertTrue("SO:0000167" in seqd.G)

    def test_ma2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("PHENOLS" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["PHENOLS"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("CD55" in seqd.G)
        self.assertTrue("AKT1" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["CD55"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("UBERON:0000062" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["UBERON:0000062"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("MOP:0000797" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["MOP:0000797"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("AGING" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["AGING"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("VIRION" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["VIRION"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="MolecularActivity",
            input_id="GO",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("CL:0000097" in seqd.G)

    def test_ma2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="MolecularActivity",
            input_id="GO",
            output_id="DOID",
            values="GO:0050626",
        )
        seqd.query()
        self.assertTrue("DOID:1883" in seqd.G)
        edges = seqd.G["GO:GO:0050626"]["DOID:1883"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))
