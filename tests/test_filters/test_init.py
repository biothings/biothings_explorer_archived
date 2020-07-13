"""
Tests for __init__.py
"""

import unittest
from biothings_explorer.filters.__init__ import Filter
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher

class TestFilter(unittest.TestCase):

    # test node degrees
    def test_node_deg(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                                 output_cls='ChemicalSubstance',
                                                 input_id='NCBIGene',
                                                 values='1017')
        seqd.query()
        filt = {'name':'NodeDegree', 'count':30}
        newG = Filter(seqd.G, filt).filter_results()
        self.assertEqual(newG.number_of_nodes(), 31)
        for node,y in newG.nodes(data=True):
            if node != 'NCBIGene:1017':
                self.assertEqual('NodeDegree', y['filteredBy'])

    # test apis
    def test_api(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        filt = {'name':'UniqueAPIs'}
        newG = Filter(seqd.G, filt).filter_results()
        for node,y in newG.nodes(data=True):
            if node != 'NCBIGene:1017':
                self.assertEqual('UniqueAPIs', y['filteredBy'])

    # test co CoOccurrence
    def test_co_occur(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        filt = {'name':'CoOccurrence', 'count':60}
        newG = Filter(seqd.G, filt).filter_results()
        self.assertEqual(newG.number_of_nodes(), 61)
        for node,y in newG.nodes(data=True):
            if node != 'MESH:D000755':
                self.assertEqual('CoOccurrence', y['filteredBy'])

    # test with labels
    def test_label_T(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        filt = {'name':'EdgeLabel', 'count':60, 'label':'related_to'}
        newG = Filter(seqd.G, filt).filter_results()
        self.assertEqual(newG.number_of_nodes(), 61)
        for x in newG.edges.data():
            self.assertEqual(filt['label'], x[2]['label'])

     # with no label given
    def test_label_F(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017')
        seqd.query()
        filt = {'name':'EdgeLabel', 'count':60}
        newG = Filter(seqd.G, filt).filter_results()
        self.assertEqual(seqd.G, newG)
        self.assertEqual(seqd.G.number_of_nodes(), newG.number_of_nodes())

    # test no filter given
    def test_no_filter(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                          output_cls='ChemicalSubstance',
                                          input_id='NCBIGene',
                                          values='1017')
        seqd.query()
        newG = Filter(seqd.G).filter_results()
        self.assertEqual(seqd.G, newG)
        self.assertEqual(seqd.G.number_of_nodes(), newG.number_of_nodes())


if __name__ == '__main__':
    unittest.main()
