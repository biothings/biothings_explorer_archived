import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from .utils import get_apis

reg = Registry()


class TestSingleHopQuery(unittest.TestCase):
    def test_disease2chemicalsubstance(self):
        """Test disease-chemical"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="ChemicalSubstance",
            input_cls="Disease",
            pred="affected_by",
            input_id="UMLS",
            values="C0027430",
        )
        seqd.query()
        self.assertTrue("Adrenal Cortex Hormones".upper() in seqd.G)
        edges = seqd.G["UMLS:C0027430"]["Adrenal Cortex Hormones".upper()]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2gene(self):
        """Test disease-gene entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Gene",
            input_cls="Disease",
            pred="affected_by",
            input_id="UMLS",
            values="C0027430",
        )
        seqd.query()
        self.assertTrue("CAMP" in seqd.G)
        edges = seqd.G["UMLS:C0027430"]["CAMP"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2disease(self):
        """Test disease-disease entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Disease",
            input_cls="Disease",
            pred="causes",
            input_id="UMLS",
            values="C0027430",
        )
        seqd.query()
        self.assertTrue("EDEMA" in seqd.G)
        edges = seqd.G["UMLS:C0027430"]["EDEMA"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2bp(self):
        """Test disease-bp entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="BiologicalProcess",
            input_cls="Disease",
            pred="causes",
            output_id="UMLS",
            input_id="UMLS",
            values="C0027430",
        )
        seqd.query()
        self.assertTrue("C0037361".upper() in seqd.G)
        edges = seqd.G["UMLS:C0027430"]["C0037361"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2cc(self):
        """Test disease-cc entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="CellularComponent",
            input_cls="Disease",
            pred="affected_by",
            output_id="UMLS",
            input_id="UMLS",
            values="C0431506",
        )
        seqd.query()
        self.assertTrue("C1521104" in seqd.G)
        edges = seqd.G["UMLS:C0431506"]["C1521104"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2cell(self):
        """Test disease-cell entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="Cell",
            input_cls="Disease",
            pred="affected_by",
            input_id="UMLS",
            values="C0028778",
        )
        seqd.query()
        self.assertTrue("C0443611" in seqd.G)
        edges = seqd.G["UMLS:C0028778"]["C0443611"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))

    def test_disease2anatomy(self):
        """Test disease-anatomy entity"""
        seqd = SingleEdgeQueryDispatcher(
            output_cls="AnatomicalEntity",
            input_cls="Disease",
            pred="affected_by",
            input_id="UMLS",
            values="C0031557",
        )
        seqd.query()
        self.assertTrue("BLOOD" in seqd.G)
        edges = seqd.G["UMLS:C0031557"]["BLOOD"]
        self.assertTrue("SEMMED Disease API" in get_apis(edges))
