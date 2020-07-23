"""
Tests for co-occurs.py
"""

import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher
from biothings_explorer.filters.co_occurs import filter_co_occur

class TestFilterCoOccur(unittest.TestCase):

    # test for counts
    def test_count(self):
        counts = [15, 50, 100]
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        for count in counts:
            subG = filter_co_occur(seqd.G, count)
            self.assertEqual(count+1, len(subG.nodes))

    # test for filteredBy
    def test_filteredBy(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        subG = filter_co_occur(seqd.G)
        for node,y in subG.nodes(data=True):
            if node != 'MESH:D000755':
                self.assertEqual('CoOccurrence', y['filteredBy'])

    # test that all 3 labels are present (ngd, rank, and filteredBy)
    def test_labels(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        subG = filter_co_occur(seqd.G)
        for node,y in subG.nodes(data=True):
            if node != 'MESH:D000755':
                self.assertTrue('filteredBy' in y.keys())
                self.assertTrue('rank' in y.keys())
                self.assertTrue('ngd_overall' in y.keys())

    # test if ranks are in the right order (use ngd_overall)
    def test_ranks(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        subG = filter_co_occur(seqd.G)
        rankngd = [0]*50
        for node,y in subG.nodes(data=True):
            if node != 'MESH:D000755':
                rankngd[y['rank']-1] = y['ngd_overall']
        for i in range(len(rankngd)-1):
            self.assertLess(rankngd[i], rankngd[i+1])

    # test that source node doesn't have any of the new labels
    def test_source(self):
        seqd = SingleEdgeQueryDispatcher(input_cls='Disease',
                                            output_cls='Disease',
                                            input_id='MESH',
                                            values='D000755')
        seqd.query()
        subG = filter_co_occur(seqd.G)
        for node,y in subG.nodes(data=True):
            if node == 'MESH:D000755':
                self.assertTrue('filteredBy' not in y.keys())
                self.assertTrue('rank' not in y.keys())
                self.assertTrue('ngd_overall' not in y.keys())


if __name__ == '__main__':
    unittest.main()
