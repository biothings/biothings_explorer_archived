import unittest
from biothings_explorer.hint import Hint


class TestHint(unittest.TestCase):
    def setUp(self):
        self.ht = Hint()

    def mygene_test(self, res):
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("Gene"))
        self.assertIsNotNone(res.get("Gene")[0])
        bioentity = res.get("Gene")[0]
        self.assertEqual(bioentity["NCBIGene"], "1017")
        self.assertEqual(bioentity["type"], "Gene")
        self.assertEqual(bioentity["primary"]["identifier"], "NCBIGene")
        self.assertEqual(bioentity["primary"]["value"], "1017")
        self.assertEqual(bioentity["SYMBOL"], "CDK2")

    def myvariant_test(self, res):
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("SequenceVariant"))
        self.assertIsNotNone(res.get("SequenceVariant")[0])
        bioentity = res.get("SequenceVariant")[0]
        self.assertEqual(bioentity["DBSNP"], "rs12190874")
        self.assertEqual(bioentity["type"], "SequenceVariant")
        self.assertEqual(bioentity["primary"]["identifier"], "DBSNP")
        self.assertEqual(bioentity["primary"]["value"], "rs12190874")

    def test_gene_NCBIGene_id_as_input(self):
        """Test the output of Hint query when providing gene NCBIGene id as input."""
        res = self.ht.query("1017")
        self.mygene_test(res)

    def test_gene_SYMBOL_as_input(self):
        """Test the output of Hint query when providing gene SYMBOL as input."""
        res = self.ht.query("CDK2")
        self.mygene_test(res)

    def test_gene_UMLS_id_as_input(self):
        """Test the output of Hint query when providing gene UMLS id as input."""
        res = self.ht.query("C1332823")
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("Gene"))
        self.assertIsNotNone(res.get("Gene")[0])
        bioentity = res.get("Gene")[0]
        self.assertEqual(bioentity["UMLS"], "C1332823")
        self.assertEqual(bioentity["type"], "Gene")
        self.assertEqual(bioentity["primary"]["identifier"], "NCBIGene")
        self.assertEqual(bioentity["primary"]["value"], "7852")
        self.assertEqual(bioentity["SYMBOL"], "CXCR4")

    def test_gene_hgnc_id_as_input(self):
        """Test the output of Hint query when providing gene hgnc id as input."""
        res = self.ht.query("1771")
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get("Gene"))
        self.assertIsNotNone(res.get("Gene")[0])
        bioentity = [item for item in res.get("Gene") if item.get("HGNC") == "1771"][0]
        self.assertEqual(bioentity["type"], "Gene")
        self.assertEqual(bioentity["primary"]["identifier"], "NCBIGene")
        self.assertEqual(bioentity["primary"]["value"], "1017")

    def test_gene_uniprot_id_as_input(self):
        """Test the output of Hint query when providing gene uniprot id as input."""
        res = self.ht.query("P24941")
        self.mygene_test(res)

    def test_variant_rsid_as_input(self):
        """Test the output of Hint query when providing variant dbsnp id as input."""
        res = self.ht.query("rs12190874")
        self.myvariant_test(res)

    def test_chemical(self):
        """Test the output of Hint query when providing chemical drugbank ID as input."""
        res = self.ht.query("DB01926")
        bioentity = res.get("ChemicalSubstance")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["name"], "Carboxymycobactin S")

    def test_chemical_with_cas_id(self):
        """Test the output of Hint query when providing chemical CAS ID as input."""
        res = self.ht.query("1744-22-5")
        bioentity = res.get("ChemicalSubstance")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["CHEMBL.COMPOUND"], "CHEMBL744")

    def test_chemical_with_iupac_id(self):
        """Test the output of Hint query when providing chemical IUPAC ID as input."""
        res = self.ht.query("[6-(trifluoromethoxy)-1,3-benzothiazol-2-yl]amine")
        bioentity = res.get("ChemicalSubstance")[0]
        self.assertIsNotNone(res)
        self.assertEqual(
            bioentity["IUPAC"], "[6-(trifluoromethoxy)-1,3-benzothiazol-2-yl]amine"
        )

    def test_chemical_with_formula(self):
        """Test the output of Hint query when providing chemical formula as input."""
        res = self.ht.query("H2O")
        bioentity = res.get("ChemicalSubstance")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["formula"], "H2O")

    def test_chemical_with_abbreviations(self):
        """Test the output of Hint query when providing chemical abbreviations as input."""
        res = self.ht.query("AZT")
        names = [item.get("name") for item in res.get("ChemicalSubstance")]
        self.assertIsNotNone(res)
        self.assertIn("ZIDOVUDINE", names)

    def test_chemical_with_international_brand_names(self):
        """Test the output of Hint query when providing drug international brand name as input."""
        res = self.ht.query("Dulane")
        names = [item.get("name") for item in res.get("ChemicalSubstance")]
        self.assertIsNotNone(res)
        self.assertIn("DULOXETINE", names)

    def test_mf_with_lowercase_go_term(self):
        """Test the output of Hint query when providing lower case go term as input."""
        res = self.ht.query("go:0001790")
        bioentity = res.get("MolecularActivity")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["GO"], "GO:0001790")

    def test_bp_with_lowercase_go_term(self):
        """Test the output of Hint query when providing lower case go term as input."""
        res = self.ht.query("go:0002354")
        bioentity = res.get("BiologicalProcess")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["GO"], "GO:0002354")

    def test_cc_with_lowercase_go_term(self):
        """Test the output of Hint query when providing lower case go term as input."""
        res = self.ht.query("go:1903503")
        bioentity = res.get("CellularComponent")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["GO"], "GO:1903503")

    def test_anatomy_with_uberon_id(self):
        """Test the output of Hint query when providing UBERON ID as input."""
        res = self.ht.query("UBERON:0035924")
        bioentity = res.get("AnatomicalEntity")[0]
        self.assertIsNotNone(res)
        self.assertEqual(bioentity["UBERON"], "UBERON:0035924")

    def test_resolving_by_synonyms(self):
        """Test the output of Hint query when providing disease synonyms"""
        res = self.ht.query("GIST")
        bioentity = res.get("Disease")
        ids = [item.get("MONDO") for item in bioentity]
        self.assertIsNotNone(res)
        self.assertIn("MONDO:0011719", ids)

    def test_if_response_is_empty_list(self):
        """Test if API response is a empty list"""
        res = self.ht.query("APP")
        self.assertIsNotNone(res)
