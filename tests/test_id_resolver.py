import unittest
from biothings_explorer.id_resolver import IDResolver


class TestIDResolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idr = IDResolver()

    def test_input_genes(self):
        inputs = [(['CXCR4', 'CXCR3', 'CXCR2'], 'bts:symbol', 'Gene')]
        res = self.idr.resolve_ids(inputs)
        self.assertIn('symbol:CXCR4', res)
        self.assertEqual(res['symbol:CXCR4']['bts:ensembl'], ['ENSG00000121966'])
        self.assertEqual(res['symbol:CXCR4']['bts:entrez'], ['7852'])
        self.assertEqual(res['symbol:CXCR4']['bts:symbol'], ['CXCR4'])

    def test_wrong_gene_symbolss(self):
        inputs = [(['CXCR4', 'CXCR3', 'CXCR2', '123'], 'bts:symbol', 'Gene')]
        res = self.idr.resolve_ids(inputs)
        self.assertIn('symbol:123', res)
        self.assertDictEqual(res['symbol:123'], {'bts:symbol': ['123']})


if __name__ == '__main__':
    unittest.main()