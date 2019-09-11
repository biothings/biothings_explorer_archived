# -*- coding: utf-8 -*-

"""
biothings_explorer.user_query_dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Convert User Query Into Actual API Calls
"""
from collections import defaultdict
import networkx as nx
import time

from .api_call_dispatcher import Dispatcher
from .id_converter import IDConverter
from .registry import Registry
from .networkx_helper import load_res_to_networkx, add_equivalent_ids_to_nodes


class SingleEdgeQueryDispatcher():
    def __init__(self, input_cls=None, input_id=None, values=None,
                 output_cls=None, output_id=None, pred=None,
                 equivalent_ids=None, input_obj=None, registry=None):
        self.input_cls = input_cls
        self.input_id = input_id
        self.output_cls = output_cls
        self.output_id = output_id
        self.pred = pred
        self.values = values
        self.equivalent_ids = equivalent_ids
        if input_obj:
            assert "primary" in input_obj
            self.input_cls = input_obj.get("primary").get("cls")
            self.input_id = input_obj.get("primary").get("identifier")
            self.values = input_obj.get("primary").get("value")
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.idc = IDConverter(registry=self.registry)
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def group_edges_by_input_id(self, edges):
        grouped_edges = defaultdict(list)
        for _edge in edges:
            grouped_edges[_edge['input_id']].append(_edge)
        return grouped_edges

    def merge_equivalent_nodes(self):
        if self.G:
            nodes_to_remove = set()
            nodes_to_add = []
            edges_to_add = []
            for n1, n2, data in self.G.edges(data=True):
                identifier = self.G.nodes[n2]['identifier']
                if self.output_id and self.output_id != identifier:
                    equivalent_ids = self.G.nodes[n2]['equivalent_ids']
                    new_vals = equivalent_ids.get(self.output_id)
                    if new_vals:
                        # get n2's node info
                        node_info = self.G.nodes[n2]
                        # change n2's identifier
                        node_info['identifier'] = self.output_id
                        for _val in new_vals:
                            # add new edge
                            edges_to_add.append((n1, _val, data))
                            # add new node
                            if _val not in self.G.nodes():
                                nodes_to_add.append((_val, node_info))
                                nodes_to_remove.add(n2)
            for n in nodes_to_remove:  # remove the merged nodes
                self.G.remove_node(n)
            self.G.add_nodes_from(nodes_to_add)
            self.G.add_edges_from(edges_to_add)

    def query(self):
        # filter edges based on subject, object, predicate
        edges = self.registry.filter_edges(self.input_cls, self.output_cls,
                                           self.pred)
        grouped_edges = self.group_edges_by_input_id(edges)
        t1 = time.time()
        if not self.equivalent_ids:
            # find equivalent ids for the input value
            equivalent_ids = self.idc.convert_ids([(self.values,
                                                   self.input_id,
                                                   self.input_cls)])
            self.equivalent_ids = equivalent_ids
        # print("equivalent_ids", self.equivalent_ids)
        t2 = time.time()
        # print('time to find equivalent ids {}'.format(t2-t1))
        input_edges = []
        mapping_keys = []
        output_id_types = []
        id_mapping = {}
        # populate edge with corresponding input value
        # k is the source id, v is the equivalent ids
        for k, v in self.equivalent_ids.items():
            # p is the input id, q is the edges from the source id
            for p, q in grouped_edges.items():
                # check if input id is in equivalent ids
                if p in v and v[p]:
                    for _edge in q:
                        _edge['value'] = v[p]
                        mapping_keys.append(_edge['mapping_key'])
                        input_edges.append(_edge)
                        output_id_types.append(_edge['output_id'])
                    self.G.add_node(k.split(':', 1)[-1],
                                    type=self.input_cls,
                                    identifier=k.split(':', 1)[0],
                                    level=1,
                                    equivalent_ids=self.equivalent_ids[k])
                    for _id in v[p]:
                        id_mapping[_id] = k.split(':', 1)[-1]
        # print('input_edges', input_edges)
        if not input_edges:
            self.G = None
            return
        # make API calls and restructure API outputs
        _res = self.dp.dispatch(input_edges)
        t3 = time.time()
        # print('time to make API calls {}'.format(t3 - t2))
        # print('_res', _res)
        # load API outputs into the MultiDiGraph
        self.G = load_res_to_networkx(_res, self.G, mapping_keys,
                                      id_mapping, output_id_types)
        # annotate nodes with its equivalent ids
        self.G, out_equ_ids = add_equivalent_ids_to_nodes(self.G, self.idc)
        self.equivalent_ids.update(out_equ_ids)
        t4 = time.time()
        # print("time to generate equivalent ids for output {}".format(t4-t3))
        # merge equivalent nodes
        self.merge_equivalent_nodes()


class ConnectTwoConcepts():
    def __init__(self, start_point, end_point, edge1, edge2, registry=None):
        self.input_id = start_point['identifier']
        self.input_cls = start_point['type']
        self.input_values = start_point['values']
        self.output_id = end_point['identifier']
        self.output_cls = end_point['type']
        self.output_values = end_point['values']
        self.edge1 = edge1
        self.edge2 = edge2
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.idc = IDConverter(registry=self.registry)
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def group_edges_by_input_id(self, edges):
        grouped_edges = defaultdict(list)
        for _edge in edges:
            grouped_edges[_edge['input_id']].append(_edge)
        return grouped_edges

    def connect(self):
        idc_inputs = []
        # filter input edges based on subject, object, predicate
        input_edges = self.registry.filter_edges(self.input_cls,
                                                 None,
                                                 self.edge1)
        # group input edges based on identifier
        grouped_input_edges = self.group_edges_by_input_id(input_edges)
        # populate to id converter input list
        idc_inputs.append((self.input_values,
                           self.input_id,
                           self.input_cls))
        # filter output edges based on subject, object, predicate
        output_edges = self.registry.filter_edges(self.output_cls,
                                                  None,
                                                  self.edge2)
        # group output edges based on identifier
        grouped_output_edges = self.group_edges_by_input_id(output_edges)
        # populate to id converter input list
        idc_inputs.append((self.output_values,
                           self.output_id,
                           self.output_cls))
        # find equivalent ids for inputs and outputs
        equivalent_ids = self.idc.convert_ids(idc_inputs)
        input_edges = []
        mapping_keys = []
        output_id_types = []
        id_mapping = {}
        # populate edge with corresponding input value
        # k is the source id, v is the equivalent ids
        for k, v in equivalent_ids.items():
            id_type, _id = k.split(':', 1)
            if not id_type.startswith("bts:"):
                id_type = "bts:" + id_type
            if id_type == self.input_id and _id == self.input_values:
                # p is the input id, q is the edges from the source id
                for p, q in grouped_input_edges.items():
                    # check if input id is in equivalent ids
                    if p in v and v[p]:
                        for _edge in q:
                            _edge['value'] = v[p]
                            mapping_keys.append(_edge['mapping_key'])
                            input_edges.append(_edge)
                            output_id_types.append(_edge['output_id'])
                        self.G.add_node(k.split(':', 1)[-1],
                                        type=q[0]['input_type'],
                                        identifier=q[0]['input_id'],
                                        level=1,
                                        equivalent_ids=equivalent_ids[k])
                        for _id in v[p]:
                            id_mapping[_id] = k.split(':', 1)[-1]
            if id_type == self.output_id and _id == self.output_values:
                for m, n in grouped_output_edges.items():
                    # check if input id is in equivalent ids
                    if m in v and v[m]:
                        for _edge in n:
                            _edge['value'] = v[m]
                            mapping_keys.append(_edge['mapping_key'])
                            input_edges.append(_edge)
                            output_id_types.append(_edge['output_id'])
                        self.G.add_node(k.split(':', 1)[-1],
                                        type=n[0]['input_type'],
                                        identifier=n[0]['input_id'],
                                        level=1,
                                        equivalent_ids=equivalent_ids[k])
                        for _id in v[m]:
                            id_mapping[_id] = k.split(':', 1)[-1]
        # make API calls and restructure API outputs
        _res = self.dp.dispatch(input_edges)
        # load API outputs into the MultiDiGraph
        self.G = load_res_to_networkx(_res, self.G, mapping_keys,
                                      id_mapping, output_id_types)
        # annotate nodes with its equivalent ids
        self.G, _ = add_equivalent_ids_to_nodes(self.G, self.idc)


class MultiEdgeQueryDispatcher():
    def __init__(self, input_node, edges, registry=None):
        """
        edges: [(sub_cls, pred, obj_cls), (sub_cls, pred, obj_cls)
        """
        self.edges = edges
        self.input_node = input_node
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.idc = IDConverter(registry=self.registry)
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def get_equivalent_ids(self, G):
        result = {}
        for x, y in G.nodes(data=True):
            if y['level'] and y['level'] == 2:
                identifier = y['identifier']
                if identifier.startswith('bts:'):
                    identifier = identifier[4:]
                curie = identifier + ':' + x
                result[curie] = y['equivalent_ids']
        return result

    def query(self):
        for i, edge in enumerate(self.edges):
            input_cls, pred, output_cls = edge
            if i == 0:
                input_id = self.input_node['id']
                input_values = self.input_node['values']
                _, pred, output_cls = edge
                equivalent_ids = None
            else:
                equivalent_ids = self.get_equivalent_ids(seqd.G)
                input_id = None
                input_values = None
            seqd = SingleEdgeQueryDispatcher(input_cls, input_id,
                                             input_values, output_cls,
                                             None, pred,
                                             equivalent_ids=equivalent_ids,
                                             registry=self.registry)
            seqd.query()
            self.G = nx.compose(self.G, seqd.G)
