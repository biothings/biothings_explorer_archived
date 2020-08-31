import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_bp2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="CellularComponent",
            input_id="GO",
            pred="related_to",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("PR:000013099" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["PR:000013099"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_bp2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="CellularComponent",
            pred="related_to",
            input_id="GO",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("SO:0000199" in seqd.G)
        self.assertTrue("SO:0001853" in seqd.G)

    def test_bp2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="CHEBI",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("CHEBI:17984" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["CHEBI:17984"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_bp2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene",
            input_cls="CellularComponent",
            input_id="GO",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("RAB6A" in seqd.G)
        self.assertTrue("PPM1L" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["PPM1L"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_bp2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="UBERON",
            values="GO:0000776",
        )
        seqd.query()
        self.assertTrue("UBERON:0009856" in seqd.G)
        edges = seqd.G["GO:GO:0000776"]["UBERON:0009856"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_bp2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="CellularComponent",
            input_id="GO",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("MOP:0000479" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["MOP:0000479"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_cc2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="GO",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("GO:0016311" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["GO:0016311"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_cc2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="GO",
            values="GO:0000139",
        )
        seqd.query()
        self.assertTrue("GO:0005764" in seqd.G)
        edges = seqd.G["GO:GO:0000139"]["GO:0005764"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))

    def test_cc2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="CL",
            values="GO:0001891",
        )
        seqd.query()
        self.assertTrue("CL:0000234" in seqd.G)

    def test_bp2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="CellularComponent",
            input_id="GO",
            output_id="DOID",
            values="GO:0002102",
        )
        seqd.query()
        self.assertTrue("DOID:162" in seqd.G)
        edges = seqd.G["GO:GO:0002102"]["DOID:162"]
        self.assertTrue("CORD Cellular Component API" in get_apis(edges))
