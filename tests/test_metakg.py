import unittest
from biothings_explorer.smartapi_kg import MetaKG


class TestMetaKGClass(unittest.TestCase):
    def test_filter_function(self):
        kg = MetaKG()
        res = kg.filter({"input_type": "Gene"})
        self.assertGreater(len(res), 10)
