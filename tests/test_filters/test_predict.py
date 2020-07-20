"""
Tests for integration of filter into Predict/FindConnection

**NOTE: filter length must equal len(self.paths), can have empty dicts for place holders**
"""

import unittest
from biothings_explorer.hint import Hint
from biothings_explorer.user_query_dispatcher import FindConnection

class TestPredict(unittest.TestCase):

    # test no filters given
    def test_no_filter(self):
        ht = Hint()
        input = ht.query('hyperphenylalaninemia')['Disease'][0]
        filt = []
        fc = FindConnection(input_obj=input,
                            output_obj='ChemicalSubstance',
                            intermediate_nodes=['Gene'],
                            filters=filt)
        fc.connect()
        for node,y in fc.fc.G.nodes(data=True):
            self.assertTrue('filteredBy' not in y.keys())

    # test 1 filter
    def test_one_filt(self):
        ht = Hint()
        input = ht.query('hyperphenylalaninemia')['Disease'][0]
        filt = [{}, {'name':'NodeDegree', 'count':25}]
        fc = FindConnection(input_obj=input,
                            output_obj='ChemicalSubstance',
                            intermediate_nodes=['Gene'],
                            filters=filt)
        fc.connect()
        self.assertEqual(27, len(fc.fc.G.nodes))

    # test w/ intermediate node
    def test_two_filt(self):
        ht = Hint()
        input = ht.query('hyperphenylalaninemia')['Disease'][0]
        filt = [{'name':'NodeDegree', 'count':20}, {'name':'EdgeLabel', 'label':'related_to'}]
        fc = FindConnection(input_obj=input,
                            output_obj='ChemicalSubstance',
                            intermediate_nodes=['Gene'],
                            filters=filt)
        fc.connect()
        self.assertEqual(52, len(fc.fc.G.nodes))
        for node,y in fc.fc.G.nodes(data=True):
            if node != 'mild hyperphenylalaninemia':
                if y['type'] == 'Gene':
                    self.assertEqual('NodeDegree', y['filteredBy'])
                elif y['type'] == 'ChemicalSubstance':
                    self.assertEqual('EdgeLabel', y['filteredBy'])
