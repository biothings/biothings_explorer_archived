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
            input_id="MOP",
            output_id="PR",
            pred="related_to",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("PR:000007883" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["PR:000007883"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="MolecularActivity",
            pred="related_to",
            input_id="MOP",
            output_id="SO",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("SO:0000014" in seqd.G)
        self.assertTrue("SO:0000141" in seqd.G)

    def test_ma2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="CHEBI",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("CHEBI:29309" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["CHEBI:29309"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene",
            input_cls="MolecularActivity",
            input_id="MOP",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("HSD17B4" in seqd.G)
        self.assertTrue("CSH1" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["HSD17B4"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="UBERON",
            values="MOP:0000142",
        )
        seqd.query()
        self.assertTrue("UBERON:0004187" in seqd.G)
        edges = seqd.G["MOP:MOP:0000142"]["UBERON:0004187"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="MolecularActivity",
            input_id="MOP",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("MOP:0000787" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["MOP:0000787"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="GO",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("GO:0000746" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["GO:0000746"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="GO",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("GO:0046930" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["GO:0046930"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))

    def test_ma2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="CL",
            values="MOP:0000142",
        )
        seqd.query()
        self.assertTrue("CL:0000034" in seqd.G)

    def test_ma2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="MolecularActivity",
            input_id="MOP",
            output_id="DOID",
            values="MOP:0000631",
        )
        seqd.query()
        self.assertTrue("DOID:2935" in seqd.G)
        edges = seqd.G["MOP:MOP:0000631"]["DOID:2935"]
        self.assertTrue("CORD Molecular Activity API" in get_apis(edges))
