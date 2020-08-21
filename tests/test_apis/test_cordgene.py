import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_gene2protein(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Protein",
            input_cls="Gene",
            output_id="PR",
            input_id="HGNC",
            values="7890",
        )
        seqd.query()
        self.assertTrue("PR:000016253" in seqd.G)
        self.assertTrue("PR:000001825" in seqd.G)

    def test_gene2genomicentity(self):
        """Test gene-protein"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="GenomicEntity",
            output_id="SO",
            input_cls="Gene",
            input_id="HGNC",
            values="7890",
        )
        seqd.query()
        self.assertTrue("SO:0000704" in seqd.G)
        self.assertTrue("SO:0001853" in seqd.G)

    def test_gene2chemicalsubstance(self):
        """Test gene-genomic entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="Gene",
            input_id="HGNC",
            values="7890",
            output_id="CHEBI",
        )
        seqd.query()
        self.assertTrue("CHEBI:27899" in seqd.G)

    def test_gene2gene(self):
        """Test gene-gene"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene", input_cls="Gene", input_id="HGNC", values="7890"
        )
        seqd.query()
        self.assertTrue("CALB1" in seqd.G)
        self.assertTrue("ADORA1" in seqd.G)

    def test_gene2anatomy(self):
        """Test gene-anatomy"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="Gene",
            input_id="HGNC",
            output_id="UBERON",
            values="7890",
        )
        seqd.query()
        self.assertTrue("UBERON:0001844" in seqd.G)

    def test_gene2ma(self):
        """Test gene-molecular_activity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="MolecularActivity",
            input_cls="Gene",
            input_id="HGNC",
            output_id="GO",
            values="10115",
        )
        seqd.query()
        self.assertTrue("GO:0008083" in seqd.G)

    def test_gene2bp(self):
        """Test gene-biological_process"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="Gene",
            input_id="HGNC",
            output_id="GO",
            values="1139",
        )
        seqd.query()
        self.assertTrue("GO:0002250" in seqd.G)

    def test_gene2cc(self):
        """Test gene-cellular_component"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="Gene",
            input_id="HGNC",
            output_id="GO",
            values="1139",
        )
        seqd.query()
        self.assertTrue("GO:0000785" in seqd.G)

    def test_gene2cell(self):
        """Test gene-cell"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="Gene",
            output_id="CL",
            input_id="HGNC",
            values="3684",
        )
        seqd.query()
        self.assertTrue("CL:0000057" in seqd.G)

    def test_gene2disease(self):
        """Test gene-disease"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="Gene",
            input_id="HGNC",
            output_id="DOID",
            values="10115",
        )
        seqd.query()
        self.assertTrue("DOID:0060731" in seqd.G)
