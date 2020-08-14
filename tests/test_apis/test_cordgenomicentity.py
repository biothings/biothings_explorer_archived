import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_genomicentity2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="GenomicEntity",
            input_id="SO",
            pred="related_to",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("PR:000022738" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["PR:000022738"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            input_cls="GenomicEntity",
            pred="related_to",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("SO:0000165" in seqd.G)
        self.assertTrue("SO:0000436" in seqd.G)

    def test_genomicentity2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("CHEBI:33284" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["CHEBI:33284"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("ARHGAP45" in seqd.G)
        self.assertTrue("LRP5" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["LRP5"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("UBERON:0000104" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["UBERON:0000104"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("MOP:0000569" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["MOP:0000569"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("GROWTH" in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["GROWTH"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("nucleolus organizer region".upper() in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["nucleolus organizer region".upper()]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))

    def test_genomicentity2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="GenomicEntity",
            input_id="SO",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("CL:0000037" in seqd.G)

    def test_genomicentity2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="GenomicEntity",
            input_id="SO",
            output_id="DOID",
            values="SO:0001860",
        )
        seqd.query()
        self.assertTrue("DOID:0050784".upper() in seqd.G)
        edges = seqd.G["SO:SO:0001860"]["DOID:0050784"]
        self.assertTrue("CORD Genomic Entity API" in get_apis(edges))
