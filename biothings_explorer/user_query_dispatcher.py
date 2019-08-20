# -*- coding: utf-8 -*-

"""
biothings_explorer.user_query_dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert User Query Into Actual API Calls
"""
from collections import defaultdict

import networkx as nx

from .api_call_dispatcher import Dispatcher
from .id_converter import IDConverter
from .registry import Registry


class SingleEdgeQueryDispatcher():
    def __init__(self, input_cls, input_id, output_cls, output_id, label, values, registry=None):
        self.input_cls = input_cls
        self.input_id = input_id
        self.output_cls = output_cls
        self.output_id = output_id
        self.label = label
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.idc = IDConverter(values, input_id, input_cls, self.registry)
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def group_edges_by_input_id(self, edges):
        grouped_edges = defaultdict(list)
        for _edge in edges:
            grouped_edges[_edge['input_id']].append(_edge)
        return grouped_edges

    def query(self):
        edges = self.registry.filter_edges(self.input_cls, self.output_cls,
                                           self.label)
        print('edges', edges)
        grouped_edges = self.group_edges_by_input_id(edges)
        equivalent_ids = self.idc.convert_id()
        output_ids_dict = defaultdict(list)
        # k is the source id, v is the equivalent ids
        for k, v in equivalent_ids.items():
            # p is the input id, q is the edges from the source id
            for p, q in grouped_edges.items():
                # check if input id is in equivalent ids
                if p in v:
                    input_type = q[0]['input_type']
                    input_id = q[0]['input_id']
                    if type(v[p]) == str:
                        v[p] = [v[p]]
                    self.G.add_nodes_from(str(v[p]),
                                          type=input_type,
                                          identifier=input_id,
                                          level=1)
                    if type(v[p]) == list and len(v[p]) == 1:
                        v[p] = v[p][0]
                    output_ids = [_item['output_id'] for _item in q]
                    labels = [_item['mapping_key'] for _item in q]
                    #self.G.add_edge(k, v[p], label='equivalent')
                    self.dp.edges = q
                    self.dp.values = v[p]
                    if type(v[p]) == list:
                        self.dp.batch_mode = True
                    _res = self.dp.dispatch()
                    for m,n in _res.items():
                        if n:
                            for a, b in n.items():
                                if a in labels:
                                    for _b in b:
                                        if type(_b) != dict:
                                            self.G.add_node(str(_b), identifier=a,
                                                            type=n["@type"],
                                                            level=2)
                                            self.G.add_edge(str(v[p]), str(_b),
                                                            info=None,
                                                            label=a)
                                        else:
                                            print('_b', _b)
                                            for i,j in _b.items():
                                                if i in output_ids and j:
                                                    output_type = _b.get("@type")
                                                    source = _b.get("$source")
                                                    j = [str(jj) for jj in j]
                                                    self.G.add_nodes_from(j,
                                                                          identifier=i,
                                                                          type=output_type,
                                                                          level=2)
                                                    self.G.add_edge(str(v[p]),
                                                                    str(j[0]),
                                                                    info=_b,
                                                                    label=a,
                                                                    source=source)

        output_ids = [x for x,y in self.G.nodes(data=True) if y and y['level']==2]
        # group output ids based on identifier and type
        for _id in output_ids:
            output_ids_dict[self.G.node[_id]['type'] + ',' + self.G.node[_id]['identifier']].append(_id)
        for k, v in output_ids_dict.items():
            input_cls, input_id = k.split(',')
            self.idc = IDConverter(v, input_id, input_cls, self.registry)
            equivalent_ids = self.idc.convert_id()
            for m, n in equivalent_ids.items():
                self.G.node[m]['equivalent_ids'] = n
