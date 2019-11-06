import unittest
from biothings_explorer.hint import Hint


class TestHint(unittest.TestCase):
    def setUp(self):
        self.ht = Hint()

    def test_gene_entrez_id_as_input(self):
        """test the output of Hint query when providing gene entrez id as input"""
        res = self.ht.query('1017')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('Gene'))
        self.assertIsNotNone(res.get('Gene')[0])
        bioentity = res.get('Gene')[0]
        self.assertEqual(bioentity['entrez'], '1017')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '1017')
        self.assertEqual(bioentity['symbol'], 'CDK2')

    def test_gene_symbol_as_input(self):
        """test the output of Hint query when providing gene symbol as input"""
        res = self.ht.query('CDK2')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('Gene'))
        self.assertIsNotNone(res.get('Gene')[0])
        bioentity = res.get('Gene')[0]
        self.assertEqual(bioentity['entrez'], '1017')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '1017')
        self.assertEqual(bioentity['symbol'], 'CDK2')

    def test_gene_umls_id_as_input(self):
        """test the output of Hint query when providing gene umls id as input"""
        res = self.ht.query('C1332823')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('Gene'))
        self.assertIsNotNone(res.get('Gene')[0])
        bioentity = res.get('Gene')[0]
        self.assertEqual(bioentity['entrez'], '7852')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '7852')
        self.assertEqual(bioentity['symbol'], 'CXCR4')