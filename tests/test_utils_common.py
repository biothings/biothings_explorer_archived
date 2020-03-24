import unittest
import biothings_explorer.utils.common as util


class TestUtilsCommon(unittest.TestCase):

    def test_add_s_when_input_is_non_integer(self):
        res = util.add_s('kevin')
        self.assertEqual(res, '')
    
    def test_add_s_when_input_is_greater_than_one(self):
        res = util.add_s(2)
        self.assertEqual(res, 's')

    def test_add_s_when_input_is_less_than_or_equal_to_one(self):
        res = util.add_s(1)
        self.assertEqual(res, '')
        res = util.add_s(0)
        self.assertEqual(res, '')
    
    def test_dict2listoftuples(self):
        py_dict = {'k': 'j', 'm': 'n'}
        res = util.dict2listoftuples(py_dict)
        # self.assertListEqual([('k', 'j'), ('m', 'n')], res)
        py_dict = {}
        res = util.dict2listoftuples(py_dict)
        self.assertListEqual([], res)

    def test_listoftuples2dict(self):
        lst = [('k', 'j'), ('m', 'n')]
        res = util.listoftuples2dict(lst)
        self.assertDictEqual(res, {'k': 'j', 'm': 'n'})
        lst = []
        res = util.listoftuples2dict(lst)
        self.assertDictEqual(res, {})

    def test_unlist(self):
        py_dict = {'k': ['n'], 'm': 'q'}
        res = util.unlist(py_dict)
        self.assertDictEqual(res, {'k': 'n', 'm': 'q'})
        py_dict = {'k': ['n', 'm'], 'm': 'q'}
        res = util.unlist(py_dict)
        self.assertDictEqual(res, py_dict)
        py_dict = {'k': {'m': ['n']}, 'm': 'q'}
        res = util.unlist(py_dict)
        self.assertDictEqual(res, {'k': {'m': 'n'}, 'm': 'q'})
        py_dict = ['m']
        res = util.unlist(py_dict)
        self.assertEqual(res, 'm')
        py_dict = ['m', 'n']
        res = util.unlist(py_dict)
        self.assertEqual(res, ['m', 'n'])
        py_dict = 'm'
        res = util.unlist(py_dict)
        self.assertEqual(res, 'm')
    
    def test_find_longest_common_path(self):
        paths = ['ensembl.gene', 'ensembl.transcript']
        res = util.find_longest_common_path(paths)
        self.assertEqual(res, 'ensembl')
        paths = ['ensembl.gene', 'protein']
        res = util.find_longest_common_path(paths)
        self.assertEqual(res, '')
        paths = ['ensembl.gene', 'ensembl.transcript', 'ensembl.protein.id']
        res = util.find_longest_common_path(paths)
        self.assertEqual(res, 'ensembl')
        paths = ['ensembl.gene', 'ensembl.gid']
        res = util.find_longest_common_path(paths)
        self.assertEqual(res, 'ensembl')

    def test_get_dict_values(self):
        py_dict = {'m': 'n', 'k': 'm', '@type': 'k', '@input': 'q'}
        res = util.get_dict_values(py_dict)
        self.assertSetEqual(set(res), set(['n', 'm']))
        res = util.get_dict_values(py_dict, excluded_keys=[])
        self.assertSetEqual(set(res), set(['n', 'm', 'k', 'q']))

    def test_get_primary_id_from_equivalent_ids(self):
        equivalent_ids = {'entrez': ['1017'],
                          'ensembl': ['ENSG1234'],
                          'symbol': ['CDK7'],
                          'umls': ['C001234']}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertEqual(res, 'entrez:1017')
        equivalent_ids = {'kk': ['123']}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertEqual(res, 'kk:123')
        equivalent_ids = {}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertEqual(res, '')

    def test_get_name_from_equivalent_ids(self):
        equivalent_ids = {'entrez': ['1017'],
                          'ensembl': ['ENSG1234'],
                          'symbol': ['CDK7'],
                          'umls': ['C001234']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'CDK7')
        equivalent_ids = {'name': ['Lung Cancer'], 'mondo': ['MONDO:00023']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'Lung Cancer')
        equivalent_ids = {'mondo': ['MONDO:000123']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'MONDO:000123')
        res = util.get_name_from_equivalent_ids({})
        self.assertEqual(res, 'unknown')
        res = util.get_name_from_equivalent_ids({}, 'kevin')
        self.assertEqual(res, 'kevin')

    def test_remove_prefix_flat_dict(self):
        json_doc = {'type': 'gene', "@context": "http://schema.org"}
        json_doc_prefix_removed = util.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': 'gene', "@context": "http://schema.org"})
    
    def test_remove_prefix_lst_of_dicts(self):
        json_doc = {'type': [{'name': 'gene'}, {'drug': 'carol'}]}
        json_doc_prefix_removed = util.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': [{'name': 'gene'},{'drug': 'carol'}]})

    def test_remove_prefix_int(self):
        json_doc = {'type': 1}
        json_doc_prefix_removed = util.remove_prefix(json_doc, 'bts')
        self.assertDictEqual(json_doc_prefix_removed, {'type': 1})
    
    def test_remove_prefix_non_json(self):
        _input = 'gene'
        self.assertEqual(util.remove_prefix(_input, 'bts'), 'gene')
        _input = 12
        self.assertEqual(util.remove_prefix(_input, 'bts'), _input)


if __name__ == '__main__':
    unittest.main()
