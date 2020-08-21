import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_disease2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="Disease",
            input_id="DOID",
            pred="related_to",
            output_id="PR",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("PR:000007572" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["PR:000007572"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="Disease",
            pred="related_to",
            input_id="DOID",
            output_id="SO",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("SO:0000999" in seqd.G)
        self.assertTrue("SO:0001853" in seqd.G)

    def test_disease2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="Disease",
            input_id="DOID",
            values="DOID:12143",
            output_id="CHEBI",
        )
        seqd.query()
        self.assertTrue("CHEBI:65349" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["CHEBI:65349"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene", input_cls="Disease", input_id="DOID", values="DOID:12143"
        )
        seqd.query()
        self.assertTrue("DHDDS" in seqd.G)
        self.assertTrue("RPL3" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["DHDDS"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="Disease",
            input_id="DOID",
            output_id="UBERON",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("UBERON:0007023" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["UBERON:0007023"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="Disease",
            input_id="DOID",
            output_id="GO",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("GO:0004935" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["GO:0004935"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="Disease",
            input_id="DOID",
            values="DOID:12143",
            output_id="GO",
        )
        seqd.query()
        self.assertTrue("GO:0007605" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["GO:0007605"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="Disease",
            input_id="DOID",
            output_id="GO",
            values="DOID:0001816",
        )
        seqd.query()
        self.assertTrue("GO:0030017" in seqd.G)
        edges = seqd.G["DOID:DOID:0001816"]["GO:0030017"]
        self.assertTrue("CORD Disease API" in get_apis(edges))

    def test_disease2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="Disease",
            input_id="DOID",
            output_id="CL",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("CL:0000731" in seqd.G)

    def test_disease2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="Disease",
            input_id="DOID",
            output_id="DOID",
            values="DOID:12143",
        )
        seqd.query()
        self.assertTrue("DOID:225" in seqd.G)
        edges = seqd.G["DOID:DOID:12143"]["DOID:225"]
        self.assertTrue("CORD Disease API" in get_apis(edges))
