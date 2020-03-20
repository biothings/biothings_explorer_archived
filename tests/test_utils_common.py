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
        equivalent_ids = {'bts:entrez': ['1017'],
                          'bts:ensembl': ['ENSG1234'],
                          'bts:symbol': ['CDK7'],
                          'bts:umls': ['C001234']}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertEqual(res, 'entrez:1017')
        equivalent_ids = {'bts:kk': ['123']}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertEqual(res, 'kk:123')
        equivalent_ids = {}
        res = util.get_primary_id_from_equivalent_ids(equivalent_ids, 'Gene')
        self.assertIsNone(res)

    def test_get_name_from_equivalent_ids(self):
        equivalent_ids = {'bts:entrez': ['1017'],
                          'bts:ensembl': ['ENSG1234'],
                          'bts:symbol': ['CDK7'],
                          'bts:umls': ['C001234']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'CDK7')
        equivalent_ids = {'bts:name': ['Lung Cancer'], 'bts:mondo': ['MONDO:00023']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'Lung Cancer')
        equivalent_ids = {'bts:mondo': ['MONDO:000123']}
        res = util.get_name_from_equivalent_ids(equivalent_ids)
        self.assertEqual(res, 'MONDO:000123')
        res = util.get_name_from_equivalent_ids({})
        self.assertEqual(res, 'unknown')
        res = util.get_name_from_equivalent_ids({}, 'kevin')
        self.assertEqual(res, 'kevin')


if __name__ == '__main__':
    unittest.main()
