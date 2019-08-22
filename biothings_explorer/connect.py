from itertools import groupby
from operator import itemgetter

from .user_query_dispatcher import SingleEdgeQueryDispatcher as seqd
from .utils import common_member, visualize
from .registry import Registry
import networkx as nx


class ConnectTwoConcepts():
    def __init__(self, start_point, end_point, edge1, edge2, registry=None):
        self.input_id = start_point['identifier']
        self.input_type = start_point['type']
        self.input_values = start_point['values']
        self.output_id = end_point['identifier']
        self.output_type = end_point['type']
        self.output_values = end_point['values']
        self.edge1 = edge1
        self.edge2 = edge2
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry

    def connect(self):
        q1 = seqd(self.input_type, self.input_id,
                  None, None, self.edge1, self.input_values,
                  registry=self.registry)
        q1.query()
        q2 = seqd(self.output_type, self.output_id,
                  None, None, self.edge2, self.output_values,
                  registry=self.registry)
        q2.query()
        q1_outputs = [(x, y['equivalent_ids']) for x,y in q1.G.nodes(data=True) if y and y['level']==2 and 'equivalent_ids' in y]
        q2_outputs = [(x, y['equivalent_ids']) for x,y in q2.G.nodes(data=True) if y and y['level']==2 and 'equivalent_ids' in y]
        common = common_member(q1_outputs, q2_outputs)
        if common:
            q1_common = [_item[0] for _item in common]
            q2_common = [_item[1] for _item in common]
            q1_subset = q1.G.subgraph(q1_common + [self.input_values])
            
            q2.G = nx.relabel_nodes(q2.G, {v: k for (k, v) in common})
            q2_subset = q2.G.subgraph(q1_common + [self.output_values]).reverse()
            q2_subset.nodes[self.output_values]['level'] = 3
            self.G = nx.compose(q2_subset, q1_subset)

    def visualize(self):
        return visualize(self.G.edges())
