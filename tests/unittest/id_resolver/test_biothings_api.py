import unittest
from biothings_explorer.resolve_ids.api import BioThingsAPI
from biothings_explorer.resolve_ids.bioentity import BioEntity


GENE_METADATA = {
    "id_ranks": [
        "NCBIGene",
        "ENSEMBL",
        "HGNC",
        "UMLS",
        "UNIPROTKB",
        "SYMBOL",
        "OMIM",
        "MGI",
    ],
    "semantic": "Gene",
    "api_name": "mygene.info",
    "url": "https://mygene.info/v3",
    "mapping": {
        "NCBIGene": ["entrezgene"],
        "name": ["name"],
        "SYMBOL": ["symbol"],
        "UMLS": ["umls.cui", "umls.protein_cui"],
        "HGNC": ["HGNC"],
        "UNIPROTKB": ["uniprot.Swiss-Prot"],
        "ENSEMBL": ["ensembl.gene"],
        "OMIM": ["OMIM"],
        "MGI": ["MGI"],
    },
}


class TestBioThingsAPIClass(unittest.TestCase):
    def test_get_init(self):
        api = BioThingsAPI(GENE_METADATA)
        self.assertEqual(api.url, GENE_METADATA.get("url"))
        self.assertEqual(api.mapping, GENE_METADATA.get("mapping"))
        self.assertEqual(api.rank, GENE_METADATA.get("id_ranks"))

    def test_get_all_fields(self):
        api = BioThingsAPI(GENE_METADATA)
        res = api._get_all_fields()
        self.assertIn("MGI", res)
        self.assertIn("ensembl.gene", res)

    def test_get_scope(self):
        api = BioThingsAPI(GENE_METADATA)
        res = api._get_scope("OMIM")
        self.assertEqual(res, GENE_METADATA["mapping"]["OMIM"])

    def test_build_query_with_less_than_1000_inputs(self):
        api = BioThingsAPI(GENE_METADATA)
        res = list(api.build_query("NCBIGene", [str(i) for i in range(1, 400)]))
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0].startswith("q=1,2,3,4"))
        self.assertEqual(len(res[0].split("&", 1)[0].split(",")), 399)

    def test_build_query_with_more_than_1000_inputs(self):
        api = BioThingsAPI(GENE_METADATA)
        res = list(api.build_query("NCBIGene", [str(i) for i in range(1, 2000)]))
        self.assertEqual(len(res), 2)
        self.assertTrue(res[0].startswith("q=1,2,3,4"))
        self.assertEqual(len(res[0].split("&", 1)[0].split(",")), 1000)
        self.assertTrue(res[1].startswith("q=1001,1002,1003,1004"))
        self.assertEqual(len(res[1].split("&", 1)[0].split(",")), 999)

    def test_get_db_ids(self):
        api = BioThingsAPI(GENE_METADATA)
        api_response = [
            {"query": "1017", "entrezgene": "1017", "symbol": "CDK2", "HGNC": "1771"},
            {"query": "1018", "entrezgene": "1018", "symbol": "CDK3", "HGNC": "1772"},
            {"query": "111", "notfound": True},
        ]
        res = api.get_db_ids("NCBIGene", "Gene", api_response)
        self.assertIn("NCBIGene:1017", res)
        self.assertNotIn("NCBIGene:111", res)
        self.assertNotIn("111", res)
        self.assertEqual(len(res.keys()), 2)
        self.assertIsInstance(res["NCBIGene:1017"], BioEntity)
        entity = res["NCBIGene:1017"]
        self.assertEqual(entity.get_primary_id(), "NCBIGene:1017")

