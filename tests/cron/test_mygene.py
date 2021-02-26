import unittest
import requests


class MyGeneTestCase(unittest.TestCase):
    def setUp(self):
        self.res = requests.get("https://mygene.info/v3/query?q=symbol:CDK7&fields=all")
        self.data = self.res.json()

    def test_status_code_should_be_200(self):
        self.assertEqual(self.res.status_code, 200)

    def test_omim_id_should_be_601955(self):
        self.assertEqual(self.data["hits"][0]["MIM"], "601955")

    def test_hgnc_id_should_be_1778(self):
        self.assertEqual(self.data["hits"][0]["HGNC"], "1778")

    def test_ensembl_gene_id_should_be_ENSG00000277273(self):
        self.assertIn(
            "ENSG00000277273",
            [item["gene"] for item in self.data["hits"][0]["ensembl"]],
        )

    def test_entrezgene_id_should_be_1022(self):
        self.assertEqual(self.data["hits"][0]["entrezgene"], "1022")

    def test_uniprot_id_should_be_P50613(self):
        self.assertEqual(self.data["hits"][0]["uniprot"]["Swiss-Prot"], "P50613")
