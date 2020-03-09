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
        self.assertEqual(bioentity['umls'], 'C1332823')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '7852')
        self.assertEqual(bioentity['symbol'], 'CXCR4')

    def test_gene_hgnc_id_as_input(self):
        """test the output of Hint query when providing gene hgnc id as input"""
        res = self.ht.query('1771')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('Gene'))
        self.assertIsNotNone(res.get('Gene')[0])
        bioentity = res.get('Gene')[0]
        self.assertEqual(bioentity['hgnc'], '1771')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '1017')
        self.assertEqual(bioentity['symbol'], 'CXCR4')

    def test_gene_uniprot_id_as_input(self):
        """test the output of Hint query when providing gene uniprot id as input"""
        res = self.ht.query('P24941')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('Gene'))
        self.assertIsNotNone(res.get('Gene')[0])
        bioentity = res.get('Gene')[0]
        self.assertEqual(bioentity['uniprot'], 'P24941')
        self.assertEqual(bioentity['type'], 'Gene')
        self.assertEqual(bioentity['primary']['identifier'], 'entrez')
        self.assertEqual(bioentity['primary']['value'], '1017')
        self.assertEqual(bioentity['symbol'], 'CDK2')

    def test_variant_rsid_as_input(self):
        """test the output of Hint query when providing variant dbsnp id as input"""
        res = self.ht.query('rs12190874')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('SequenceVariant'))
        self.assertIsNotNone(res.get('SequenceVariant')[0])
        bioentity = res.get('SequenceVariant')[0]
        self.assertEqual(bioentity['dbsnp'], 'rs12190874')
        self.assertEqual(bioentity['type'], 'SequenceVariant')
        self.assertEqual(bioentity['primary']['identifier'], 'dbsnp')
        self.assertEqual(bioentity['primary']['value'], 'rs12190874')
        self.assertEqual(bioentity['hgvs'], 'chr6:g.42454850G>A')

    def test_variant_hgvs_as_input(self):
        """test the output of Hint query when providing variant hgvs id as input"""
        res = self.ht.query('chr6:g.42454850G>A')
        self.assertIsNotNone(res)
        self.assertIsNotNone(res.get('SequenceVariant'))
        self.assertIsNotNone(res.get('SequenceVariant')[0])
        bioentity = res.get('SequenceVariant')[0]
        self.assertEqual(bioentity['hgvs'], 'chr6:g.42454850G>A')
        self.assertEqual(bioentity['type'], 'SequenceVariant')
        self.assertEqual(bioentity['primary']['identifier'], 'dbsnp')
        self.assertEqual(bioentity['primary']['value'], 'rs12190874')

