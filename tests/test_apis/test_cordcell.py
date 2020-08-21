import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_cell2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="Cell",
            input_id="CL",
            pred="related_to",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("PR:000013192" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["PR:000013192"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="Cell",
            pred="related_to",
            input_id="CL",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("SO:0000194" in seqd.G)
        self.assertTrue("SO:0000167" in seqd.G)

    def test_cell2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="Cell",
            input_id="CL",
            output_id="CHEBI",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("CHEBI:80551" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["CHEBI:80551"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene", input_cls="Cell", input_id="CL", values="CL:0000060"
        )
        seqd.query()
        self.assertTrue("DMTF1" in seqd.G)
        self.assertTrue("MIR27A" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["MIR27A"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="Cell",
            input_id="CL",
            output_id="UBERON",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("UBERON:0001754" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["UBERON:0001754"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="Cell",
            input_id="CL",
            values="CL:0000062",
        )
        seqd.query()
        self.assertTrue("receptor activator activity".upper() in seqd.G)
        edges = seqd.G["CL:CL:0000062"]["receptor activator activity".upper()]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="Cell",
            input_id="CL",
            output_id="GO",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("GO:0035882" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["GO:0035882"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="Cell",
            input_id="CL",
            output_id="GO",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("GO:0005634" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["GO:0005634"]
        self.assertTrue("CORD Cell API" in get_apis(edges))

    def test_cell2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="Cell",
            input_id="CL",
            values="CL:0000040",
            output_id="CL",
        )
        seqd.query()
        self.assertTrue("CL:0000988" in seqd.G)

    def test_cell2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="Cell",
            input_id="CL",
            output_id="DOID",
            values="CL:0000060",
        )
        seqd.query()
        self.assertTrue("DOID:2600" in seqd.G)
        edges = seqd.G["CL:CL:0000060"]["DOID:2600"]
        self.assertTrue("CORD Cell API" in get_apis(edges))
