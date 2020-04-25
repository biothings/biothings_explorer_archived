import unittest
from biothings_explorer.id_resolver import IDResolver


class TestIDResolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.idr = IDResolver()

    def test_genes_as_input(self):
        inputs = [(['CXCR4', 'CXCR3', 'CXCR2'], 'SYMBOL', 'Gene')]
        res = self.idr.resolve_ids(inputs)
        self.assertIn('SYMBOL:CXCR4', res)
        self.assertEqual(res['SYMBOL:CXCR4']['ENSEMBL'], ['ENSG00000121966'])
        self.assertEqual(res['SYMBOL:CXCR4']['NCBIGene'], ['7852'])
        self.assertEqual(res['SYMBOL:CXCR4']['SYMBOL'], ['CXCR4'])

    def test_wrong_gene_SYMBOLss(self):
        inputs = [(['CXCR4', 'CXCR3', 'CXCR2', '123'], 'SYMBOL', 'Gene')]
        res = self.idr.resolve_ids(inputs)
        self.assertIn('SYMBOL:123', res)
        self.assertDictEqual(res['SYMBOL:123'], {'SYMBOL': ['123']})


if __name__ == '__main__':
    unittest.main()