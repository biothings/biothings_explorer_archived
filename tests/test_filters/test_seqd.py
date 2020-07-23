"""
Tests for initial changes to SEQD.query Function
"""

from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
import unittest

class TestSEQD(unittest.TestCase):

    # test filter by node degrees
    def test_node_deg(self):
        filter = {'name':'NodeDegree', 'count':30}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                                 output_cls='ChemicalSubstance',
                                                 input_id='NCBIGene',
                                                 values='1017',
                                                 filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 31)
        for node,y in seqd.G.nodes(data=True):
            if node != 'NCBIGene:1017':
                self.assertEqual('NodeDegree', y['filteredBy'])

    # test filter by apis
    def test_api(self):
        filter = {'name':'UniqueAPIs'}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017',
                                         filter=filter)
        seqd.query()
        for node,y in seqd.G.nodes(data=True):
            if node != 'NCBIGene:1017':
                self.assertEqual('UniqueAPIs', y['filteredBy'])

    # test filter by CoOccurrence
    def test_co_occur(self):
        filter = {'name':'CoOccurrence', 'count':60}
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755',
                                            filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 61)
        for node,y in seqd.G.nodes(data=True):
            if node != 'MESH:D000755':
                self.assertEqual('CoOccurrence', y['filteredBy'])

    # test with labels
    def test_label_T(self):
        filter = {'name':'EdgeLabel', 'count':60, 'label':'related_to'}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017',
                                         filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 61)
        for x in seqd.G.edges.data():
            self.assertEqual(filter['label'], x[2]['label'])

     # with no label given
    def test_label_F(self):
        filter = {'name':'EdgeLabel', 'count':60}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017',
                                         filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 859)

    # test no filter given
    def test_no_filter(self):
        filter = {}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                          output_cls='ChemicalSubstance',
                                          input_id='NCBIGene',
                                          values='1017',
                                          filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 859)

    # test with no count given (default to 50)
    def test_no_count(self):
        filter = {'name':'NodeDegree'}
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         output_cls='ChemicalSubstance',
                                         input_id='NCBIGene',
                                         values='1017',
                                         filter=filter)
        seqd.query()
        self.assertEqual(seqd.G.number_of_nodes(), 51)


if __name__ == '__main__':
    unittest.main()
