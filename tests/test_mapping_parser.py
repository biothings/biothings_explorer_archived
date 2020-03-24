import unittest
from biothings_explorer.mapping_parser import MappingParser

class TestMappingParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mp  = MappingParser()

    def test_remove_prefix_flat_dict(self):
        json_doc = {'type': 'gene', "@context": "http://schema.org"}
        json_doc_prefix_removed = self.mp.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': 'gene', "@context": "http://schema.org"})
    
    def test_remove_prefix_lst_of_dicts(self):
        json_doc = {'type': [{'name': 'gene'}, {'drug': 'carol'}]}
        json_doc_prefix_removed = self.mp.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': [{'name': 'gene'},{'drug': 'carol'}]})

    def test_remove_prefix_int(self):
        json_doc = {'type': 1}
        json_doc_prefix_removed = self.mp.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': 1})


if __name__ == '__main__':
    unittest.main()