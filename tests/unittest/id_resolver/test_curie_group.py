import unittest
from biothings_explorer.resolve_ids.curie_group import CurieGroup


class TestCurieGroupClass(unittest.TestCase):
    def test_find_api(self):
        res = CurieGroup._findAPI("Gene")
        self.assertIn("mapping", res)
        self.assertEqual(res["semantic"], "Gene")

    def test_group_curies_by_prefix(self):
        cg = CurieGroup("Gene", ["NCBIGene:1017", "SYMBOL:CDK7"])
        res = cg.groupCuriesByPrefix(["NCBIGene:1017", "SYMBOL:CDK7"])
        self.assertIn("NCBIGene", res)
        self.assertIn("1017", res["NCBIGene"])

