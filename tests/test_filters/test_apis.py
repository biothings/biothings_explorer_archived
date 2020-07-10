"""
Tests for apis.py
"""

import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from apis import filter_api

class TestFilterAPI(unittest.TestCase):

    # check correct number of results are returned (count + source(1))
    def test_count(self):
        counts = [15, 50, 100]
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        for count in counts:
            subG = filter_api(seqd.G, count)
            self.assertEqual(count+1, len(subG.nodes))


    # check that the filteredBy is UniqueAPIs
    def test_filteredBy(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                 output_cls='ChemicalSubstance',
                                 input_id='NCBIGene',
                                 values='1017')
        seqd.query()
        subG = filter_api(seqd.G)
        for node,y in subG.nodes(data=True):
            if node != 'NCBIGene:1017': #source node shouldn't have it
                self.assertEqual('UniqueAPIs', y['filteredBy'])


    # check that the source node isn't labeled w/ rank or filteredBy
    def test_source(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                    output_cls='Disease',
                                    input_id='MESH',
                                    values='D000755')
        seqd.query()
        source = 'MESH:D000755'
        subG = filter_api(seqd.G)
        for node,y in subG.nodes(data=True):
            if node == source:
                self.assertTrue('filteredBy' not in y.keys())
                self.assertTrue('rank' not in y.keys())

if __name__ == '__main__':
    unittest.main()
