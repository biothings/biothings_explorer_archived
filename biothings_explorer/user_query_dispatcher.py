# -*- coding: utf-8 -*-

"""
biothings_explorer.user_query_dispatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Accept user query and return results as a graph
"""
from collections import defaultdict
import networkx as nx
import time

from .api_call_dispatcher import Dispatcher
from .id_converter import IDConverter
from .registry import Registry
from .networkx_helper import load_res_to_networkx, add_equivalent_ids_to_nodes, merge_two_networkx_graphs, networkx_to_graphvis, networkx_to_pandas_df, connect_networkx_to_pandas_df
from .utils import dict2tuple, tuple2dict
from .metadata import Metadata


ID_RANK = {'Gene': 'bts:symbol',
           'ChemicalSubstance': 'bts:name',
           'DiseaseOrPhenotypicFeature': 'bts:name'}


class SingleEdgeQueryDispatcher():
    """Query from one bio-entity to other type(s) of bio-entities

    params
    ------
    input_cls: str or list, the semantic type(s) of the input, e.g. Gene
    input_id: str, the identifier type of the input, e.g. bts:entrez
    values: str or list, the actual value of the input, e.g. CDK7
    output_cls: str or list or None, the semantic type(s) of the output, e.g. Gene. If None, search for all semantic type(s) which connect from the input
    output_id: str, optional, the identifier type in which output ids will be, e.g. bts:chembl
    pred: str or list or None, the relationship between input and output. If None, search for all relationships between input and output
    input_obj: optional, a representation of the input from Hint Module
    registry: optional, the Registry object in BioThings Explorer
    """
    def __init__(self, input_cls=None, input_id=None, values=None,
                 output_cls=None, output_id=None, pred=None,
                 equivalent_ids=None, input_obj=None, registry=None):
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.metadata = Metadata(reg=self.registry)
        self.idc = IDConverter(registry=self.registry)
        semantic_types = self.metadata.list_all_semantic_types()
        id_types = self.metadata.list_all_id_types()
        self.input_cls = input_cls
        self.input_id = input_id
        self.output_cls = output_cls
        self.output_id = output_id
        # if output id is not specified, use the default id for this type
        if not output_id:
            if self.output_cls and self.output_cls in ID_RANK:
                self.output_id = [ID_RANK.get(self.output_cls)]
            else:
                self.output_id = ["bts:symbol", "bts:name"]
        if type(self.output_id) != list:
            self.output_id = [self.output_id]
        self.pred = pred
        self.values = values
        self.equivalent_ids = equivalent_ids
        if input_obj:
            assert "primary" in input_obj
            self.input_cls = input_obj.get("primary").get("cls")
            self.input_id = "bts:" + input_obj.get("primary").get("identifier")
            self.values = input_obj.get("primary").get("value")
        # check if input_cls is valid
        if self.input_cls not in semantic_types:
            raise Exception("The input_cls is not valid. Valid input classes are {}".format(semantic_types))
        # check if input_id is valid
        if not self.equivalent_ids and self.input_id not in id_types:
            raise Exception("The input_id is not valid. Valid input id types are {}".format(id_types))
        # check if output_cls is valid
        if self.output_cls and self.output_cls not in semantic_types:
            raise Exception("The output_cls is not valid. Valid output classes are {}".format(semantic_types))
        if not self.equivalent_ids:
            # find equivalent ids for the input value
            equivalent_ids = self.idc.convert_ids([(self.values,
                                                   self.input_id,
                                                   self.input_cls)])
            self.equivalent_ids = equivalent_ids
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def group_edges_by_input_id(self, edges):
        """ group edges based on the input identifier

        Params
        ------
        edges: list of dicts, edges filtered based on input/output/pred
        """
        if not edges:
            return edges
        grouped_edges = defaultdict(list)
        for _edge in edges:
            # need to convert to tuple to make it immutable
            grouped_edges[_edge['input_id']].append(dict2tuple(_edge))
        return grouped_edges

    def merge_equivalent_nodes(self):
        """Merge equivalent nodes together

        nodes will be merged based on their equivalent ids
        edges will be added to the merged node
        """
        if self.G:
            nodes_to_remove = set()
            nodes_to_add = []
            edges_to_add = []
            identifiers = []
            # loop through all edges
            # n1 is the subject node, n2 is the object node
            for n1, n2, data in self.G.edges(data=True):
                # get the id type of the object node
                identifier = self.G.nodes[n2]['identifier']
                # check if the identifier matches the id type specified by the
                # user or the default id type
                if self.output_id and identifier not in self.output_id:
                    equivalent_ids = self.G.nodes[n2]['equivalent_ids']
                    # find the corresponding id from the equivalent id dict
                    new_vals = None
                    for _id in self.output_id:
                        if equivalent_ids.get(_id):
                            new_vals = equivalent_ids.get(_id)
                            break
                    if new_vals:
                        # get n2's node info
                        node_info = self.G.nodes[n2]
                        # change n2's identifier
                        for _val in new_vals:
                            # add new edge
                            edges_to_add.append((n1, _val, data))
                            # set the original node to be removed
                            nodes_to_remove.add(n2)
                            # if this node is not in graph, add this node
                            if _val not in self.G.nodes():
                                nodes_to_add.append((_val, node_info))
                                identifiers.append(_id)
            # remove duplicate nodes
            for n in nodes_to_remove:
                self.G.remove_node(n)
            # update identifier type
            for k, n in zip(identifiers, nodes_to_add):
                n[1]['identifier'] = k
            # add new nodes and edges
            self.G.add_nodes_from(nodes_to_add)
            self.G.add_edges_from(edges_to_add)

    def query(self):
        """Query APIs and organize outputs into networkx graph"""
        # filter edges based on subject, object, predicate
        edges = self.registry.filter_edges(self.input_cls, self.output_cls,
                                           self.pred)
        if not edges:
            # print("No edges found for the <input, pred, output> you specified")
            return
        grouped_edges = self.group_edges_by_input_id(edges)
        # t1 = time.time()
        # print("equivalent_ids", self.equivalent_ids)
        # t2 = time.time()
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
                        m = _edge
                        m = tuple2dict(m)
                        m['value'] = v[p]
                        mapping_keys.append(m['label'])
                        input_edges.append(m)
                        output_id_types.append(m['output_id'])
                    self.G.add_node(k.split(':', 1)[-1],
                                    type=self.input_cls,
                                    identifier="bts:" + k.split(':', 1)[0],
                                    level=1,
                                    equivalent_ids=self.equivalent_ids[k])
                    for _id in v[p]:
                        id_mapping[_id] = k.split(':', 1)[-1]
        if not input_edges:
            return
        # make API calls and restructure API outputs
        _res = self.dp.dispatch(input_edges)
        # t3 = time.time()
        # print('time to make API calls {}'.format(t3 - t2))
        # load API outputs into the MultiDiGraph
        self.G = load_res_to_networkx(_res, self.G, mapping_keys,
                                      id_mapping, output_id_types)
        # annotate nodes with its equivalent ids
        # print("about to add equivalent ids")
        self.G, out_equ_ids = add_equivalent_ids_to_nodes(self.G, self.idc)
        # print(self.G.nodes(data=True))
        # print("equivalent ids added")
        self.equivalent_ids.update(out_equ_ids)
        # t4 = time.time()
        # print("time to generate equivalent ids for output {}".format(t4-t3))
        # merge equivalent nodes
        self.merge_equivalent_nodes()

    def to_json(self):
        """convert the graph into JSON through networkx"""
        # first check if the graph is empty
        if self.G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(self.G)
            return res
        else:
            return {}

    @property
    def output_ids(self):
        """Retrieve output ids along with their equivalent ids"""
        result = {}
        if self.G.number_of_nodes() > 0:
            for x, y in self.G.nodes(data=True):
                if y['level'] and y['level'] == 2:
                    identifier = y['identifier']
                    semantic_type = y['type']
                    if semantic_type not in result:
                        result[semantic_type] = {}
                    if identifier.startswith('bts:'):
                        identifier = identifier[4:]
                    curie = identifier + ':' + x
                    result[semantic_type][curie] = y['equivalent_ids']
        return result

    def show_all_nodes(self):
        """show all nodes in the graph"""
        return list(self.G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.G.edges())

    def display_node_info(self, node):
        """show detailed node information

        Params
        ------
        node: str, node id
        """
        if node not in self.G:
            raise Exception("{} is not in the graph".format(node))
        return self.G.nodes[node]

    def display_edge_info(self, start_node, end_node):
        """display detailed edge info between start node and end node

        Params
        ------
        start_node: str, start node id
        end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        if not self.G.has_edge(start_node, end_node):
            raise Exception("No edge exists between {} and {}".format(start_node, end_node))
        return dict(self.G[start_node][end_node])

    def display_table_view(self):
        return networkx_to_pandas_df(self.G)


class Connect():
    def __init__(self, input_obj, output_obj, max_steps=2, registry=None):
        """
        params
        ------
        max_steps: maximum number of edges connecting input and output
        """
        self.input_obj = input_obj
        self.output_obj = output_obj
        if type(max_steps) != int:
            raise Exception("max_steps should be integer")
        if max_steps < 1:
            raise Exception("max_steps should be at least 2")
        if max_steps > 4:
            raise Exception("max_steps should be no more than 4")
        self.steps = max_steps
        if registry:
            self.registry = registry
        else:
            self.registry = Registry()
        self.G = nx.MultiDiGraph()

    def show_path(self):
        input_node = self.input_obj.get("primary").get("value")
        output_node = self.output_obj.get("primary").get("value")
        paths = []
        for path in nx.all_simple_paths(self.G,
                                        source=input_node,
                                        target=output_node):

            paths.append(path)
        return paths

    def sub_graph(self):
        paths = self.show_path()
        nodes = set()
        for _path in paths:
            if _path:
                nodes = nodes | set(_path)
        return self.G.subgraph(nodes)

    def check_output_in_graph(self):
        values = self.output_obj.get("primary").get("value")
        if values in self.G:
            return True
        else:
            return False

    def to_json(self):
        """convert the graph into JSON through networkx"""
        sub_G = self.sub_graph()
        if sub_G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(sub_G)
            return res
        else:
            return {}

    def connect(self):
        for i in range(self.steps):
            # if this is the last step, set output_cls to be the same
            # as user specified output class, otherwise, output_cls
            # should be none (which is try all classes)
            if i == self.steps - 1:
                output_cls = self.output_obj.get("primary").get("cls")
            else:
                output_cls = None
            print("processing step {} ...".format(i + 1))
            if i == 0:
                seqd = SingleEdgeQueryDispatcher(input_obj=self.input_obj,
                                                 output_cls=output_cls,
                                                 pred=None)
                seqd.query()
                self.G = merge_two_networkx_graphs(self.G, seqd.G)
            else:
                output_ids = seqd.output_ids
                if output_ids:
                    for semantic_type, ids in output_ids.items():
                        seqd = SingleEdgeQueryDispatcher(equivalent_ids=ids, input_cls=semantic_type, output_cls=output_cls, pred=None)
                        seqd.query()
                        self.G = merge_two_networkx_graphs(self.G, seqd.G)
        print("query completed")
        result = self.check_output_in_graph()
        if result:
            print("Find connection")
        else:
            print("Connction not found!")

    def show_all_nodes(self):
        """show all nodes in the graph"""
        return list(self.G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.G.edges())

    def display_node_info(self, node):
        """show detailed node information

        Params
        ------
        node: str, node id
        """
        if node not in self.G:
            raise Exception("{} is not in the graph".format(node))
        return self.G.nodes[node]

    def display_edge_info(self, start_node, end_node):
        """display detailed edge info between start node and end node

        Params
        ------
        start_node: str, start node id
        end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        if not self.G.has_edge(start_node, end_node):
            raise Exception("No edge exists between {} and {}".format(start_node, end_node))
        return dict(self.G[start_node][end_node])


class FindConnection():
    def __init__(self, input_obj, output_obj,
                 intermediate_cls=None, registry=None):
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.intermediate_cls = intermediate_cls
        self.input_obj = input_obj
        self.starts = input_obj['primary']['value']
        self.output_obj = output_obj
        self.ends = output_obj['primary']['value']
        self.G = nx.MultiDiGraph()

    def connect(self):
        print("start to query from {}:{}".format(self.input_obj.get("primary").get("identifier"), self.input_obj.get("primary").get("value")))
        seqd1 = SingleEdgeQueryDispatcher(input_obj=self.input_obj,
                                          output_cls=self.intermediate_cls,
                                          registry=self.registry)
        seqd1.query()
        self.G = seqd1.G
        print("1st query completed")
        print("start to query from {}:{}".format(self.output_obj.get("primary").get("identifier"), self.output_obj.get("primary").get("value")))
        seqd2 = SingleEdgeQueryDispatcher(input_obj=self.output_obj,
                                          output_cls=self.intermediate_cls,
                                          registry=self.registry)
        seqd2.query()
        seqd2.G = seqd2.G.reverse()
        print("2nd query completed")
        self.G = merge_two_networkx_graphs(self.G, seqd2.G)
        print("completed!")

    def show_path(self, remove_duplicate=True):
        input_node = self.input_obj.get("primary").get("value")
        output_node = self.output_obj.get("primary").get("value")
        if remove_duplicate:
            paths = set()
            for path in nx.all_simple_paths(self.G,
                                            source=input_node,
                                            target=output_node):

                path = "||".join(path)
                paths.add(path)
            new_paths = []
            for _path in paths:
                new_paths.append(_path.split('||'))
            return new_paths
        else:
            paths = []
            for path in nx.all_simple_paths(self.G,
                                            source=input_node,
                                            target=output_node):
                paths.append(path)
        return paths

    def sub_graph(self):
        paths = self.show_path()
        nodes = set()
        for _path in paths:
            if _path:
                nodes = nodes | set(_path)
        return self.G.subgraph(nodes)

    def visualize(self):
        H = self.sub_graph()
        return networkx_to_graphvis(H)

    def check_output_in_graph(self):
        values = self.output_obj.get("primary").get("value")
        if values in self.G:
            return True
        else:
            return False

    def to_json(self):
        """convert the graph into JSON through networkx"""
        sub_G = self.sub_graph()
        if sub_G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(sub_G)
            return res
        else:
            return {}

    def show_all_nodes(self):
        """show all nodes in the graph"""
        return list(self.G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.G.edges())

    def display_node_info(self, node):
        """show detailed node information

        Params
        ------
        node: str, node id
        """
        if node not in self.G:
            raise Exception("{} is not in the graph".format(node))
        return self.G.nodes[node]

    def display_edge_info(self, start_node, end_node):
        """display detailed edge info between start node and end node

        Params
        ------
        start_node: str, start node id
        end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        if not self.G.has_edge(start_node, end_node):
            raise Exception("No edge exists between {} and {}".format(start_node, end_node))
        return dict(self.G[start_node][end_node])

    def display_table_view(self):
        paths = self.show_path()
        return connect_networkx_to_pandas_df(self.G, paths)


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
    def __init__(self, input_obj, edges, registry=None):
        """
        edges: [(sub_cls, pred, obj_cls), (sub_cls, pred, obj_cls)
        """
        self.edges = edges
        self.input_obj = input_obj
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.idc = IDConverter(registry=self.registry)
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()

    def query(self):
        for i, edge in enumerate(self.edges):
            input_cls, pred, output_cls = edge
            print("start to query for associations between {} and {}...".format(input_cls, output_cls))
            if i == 0:
                equivalent_ids = None
            else:
                if input_cls != self.edges[i - 1][-1]:
                    raise Exception('The subject of edge {} does not match the object of edge {}'.format(i, i-1))
                equivalent_ids = seqd.output_ids[input_cls]
                self.input_obj = None
            if (i > 0 and equivalent_ids != {}) or i == 0:
                seqd = SingleEdgeQueryDispatcher(input_obj=self.input_obj,
                                                 equivalent_ids=equivalent_ids,
                                                 input_cls=input_cls,
                                                 output_cls=output_cls,
                                                 pred=pred)
                seqd.query()
                print("finished! Find {} hits.".format(seqd.G.number_of_nodes()))
                # print(seqd.G.nodes())
                self.G = merge_two_networkx_graphs(self.G, seqd.G)

    def to_json(self):
        """convert the graph into JSON through networkx"""
        if self.G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(self.G)
            return res
        else:
            return {}

    def show_path(self, start_node, end_node):
        """show paths which can connect from the start node to end node

        Params
        ------
        start_node: str, start node id
        end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        paths = []
        for path in nx.all_simple_paths(self.G,
                                        source=start_node,
                                        target=end_node):

            paths.append(path)
        return paths

    def display_node_info(self, node):
        """show detailed node information

        Params
        ------
        node: str, node id
        """
        if node not in self.G:
            raise Exception("{} is not in the graph".format(node))
        return self.G.nodes[node]

    def display_edge_info(self, start_node, end_node):
        """display detailed edge info between start node and end node

        Params
        ------
        start_node: str, start node id
        end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        if not self.G.has_edge(start_node, end_node):
            raise Exception("No edge exists between {} and {}".format(start_node, end_node))
        return dict(self.G[start_node][end_node])

    def show_all_nodes(self):
        """show all nodes in the graph"""
        return list(self.G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.G.edges())
