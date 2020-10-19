# -*- coding: utf-8 -*-

"""Accept user query and return results as a graph.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>

"""
from collections import defaultdict
import networkx as nx
import copy

from .api_call_dispatcher import Dispatcher
from .id_resolver import IDResolver
from .registry import Registry
from .utils.networkx import (
    load_res_to_networkx,
    add_equivalent_ids_to_nodes,
    merge_two_networkx_graphs,
)
from .utils.common import dict2listoftuples, listoftuples2dict
from .utils.common import (
    get_name_from_equivalent_ids,
    get_primary_id_from_equivalent_ids,
)
from .metadata import Metadata
from .export.reasoner import ReasonerConverter
from .export.graphml import GraphmlConverter
from .export.pandas import networkx2pandas
from .export.graphviz import networkx2graphvis

# TODO: remove ID_RANK
ID_RANK = {
    "Gene": "SYMBOL",
    "ChemicalSubstance": "name",
    "DiseaseOrPhenotypicFeature": "name",
}


class SingleEdgeQueryDispatcher:
    """Query from one bio-entity to other type(s) of bio-entities.

    params
    ------
    input_cls: str or list, the semantic type(s) of the input, e.g. Gene
    input_id: str, the identifier type of the input, e.g. entrez
    values: str or list, the actual value of the input, e.g. CDK7
    output_cls: str or list or None, the semantic type(s) of the output, e.g. Gene. If None, search for all semantic type(s) which connect from the input
    output_id: str, optional, the identifier type in which output ids will be, e.g. chembl
    pred: str or list or None, the relationship between input and output. If None, search for all relationships between input and output
    input_obj: optional, a representation of the input from Hint Module
    prev_graph: the graph object coming from last query
    registry: optional, the Registry object in BioThings Explorer
    """

    def __init__(
        self,
        input_cls=None,
        input_id=None,
        values=None,
        output_cls=None,
        output_id=None,
        pred=None,
        equivalent_ids=None,
        input_obj=None,
        prev_graph={},
        query_id=1,
        reverse=False,
        registry=None,
        loop=None,
    ):
        self.loop = loop
        # load bte registry
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.prev_graph = prev_graph
        self.query_id = query_id
        self.metadata = Metadata(reg=self.registry)
        # load id conversion module
        self.idr = IDResolver()
        semantic_types = self.metadata.list_all_semantic_types()
        id_types = self.metadata.list_all_id_types()
        self.input_cls = input_cls
        self.input_id = input_id
        if output_cls in (["BiologicalEntity"], "BiologicalEntity"):
            self.output_cls = None
        else:
            self.output_cls = output_cls
        if isinstance(self.output_cls, str):
            self.output_cls = [self.output_cls]
        self.output_id = output_id
        # if output id is not specified, use the default id for this type
        if not output_id:
            if (
                self.output_cls
                and not isinstance(self.output_cls, list)
                and self.output_cls in ID_RANK
            ):
                self.output_id = [ID_RANK.get(self.output_cls)]
            else:
                self.output_id = ["SYMBOL", "name"]
        if not isinstance(self.output_id, list):
            self.output_id = [self.output_id]
        self.pred = pred
        self.values = values
        self.equivalent_ids = equivalent_ids
        self.input_identifier = None
        self.reverse = reverse
        if input_obj:
            self.input_cls = input_obj.get("primary").get("cls")
            self.input_id = input_obj.get("primary").get("identifier")
            self.values = input_obj.get("primary").get("value")
            if "SYMBOL" in input_obj:
                self.input_label = input_obj.get("SYMBOL")
                self.input_identifier = "SYMBOL"
            elif "name" in input_obj:
                self.input_label = input_obj.get("name")
                self.input_identifier = "name"
            else:
                self.input_label = (
                    input_obj.get("primary").get("identifier")
                    + ":"
                    + input_obj.get("primary").get("value")
                )
                self.input_identifier = input_obj.get("primary").get("identifier")
        else:
            self.input_label = None
        # check if input_cls is valid
        if self.input_cls not in semantic_types:
            raise Exception(
                "The input_cls is not valid. Valid input classes are {}".format(
                    semantic_types
                )
            )
        if not self.equivalent_ids:
            # find equivalent ids for the input value
            equivalent_ids = self.idr.resolve_ids(
                [(self.values, self.input_id, self.input_cls)], loop=self.loop
            )
            if not self.input_label:
                self.input_label = self.input_id + ":" + values
            self.equivalent_ids = equivalent_ids
        self.dp = Dispatcher(registry=self.registry)
        self.G = nx.MultiDiGraph()
        self.log = []
        self.summary = []

    def to_reasoner_std(self):
        """Convert the output to reasoner api standard.
        """
        rc = ReasonerConverter()
        rc.load_bte_query_path(
            start={
                "type": self.input_cls,
                "primary": {"identifier": self.input_id, "value": self.values},
            },
            intermediate=None,
            end={"type": self.output_cls[0]},
        )
        rc.load_bte_output(self.G)
        return rc.generate_reasoner_response()

    @staticmethod
    def group_edges_by_input_id(edges):
        """Group edges based on the input identifier.

        :param: edges: list of dicts, edges filtered based on input/output/pred.
        """
        if not edges:
            return edges
        grouped_edges = defaultdict(list)
        for _edge in edges:
            # need to convert to tuple to make it immutable
            grouped_edges[_edge["operation"]["input_id"]].append(
                dict2listoftuples(_edge)
            )
        return grouped_edges

    def merge_equivalent_nodes(self):
        """Merge equivalent nodes together.

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
                identifier = self.G.nodes[n2]["identifier"]
                # check if the identifier matches the id type specified by the
                # user or the default id type
                if self.output_id and identifier not in self.output_id:
                    # if equivalent_ids doesn't exist then print error message
                    if "equivalent_ids" not in self.G.nodes[n2]:
                        print("ID resolution steps failed:")
                    equivalent_ids = self.G.nodes[n2]["equivalent_ids"]
                    # find the corresponding id from the equivalent id dict
                    new_vals = None
                    for _id in self.output_id:
                        if equivalent_ids.get(_id):
                            if _id == "name":
                                new_vals = [equivalent_ids.get(_id)[0]]
                            else:
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
                            nodes_to_add.append((_val, node_info))
                            identifiers.append(_id)
            # remove duplicate nodes
            for n in nodes_to_remove:
                self.G.remove_node(n)
            # update identifier type
            for k, n in zip(identifiers, nodes_to_add):
                n[1]["identifier"] = k
            # add new nodes and edges
            self.G.add_nodes_from(nodes_to_add)
            self.G.add_edges_from(edges_to_add)

    def construct_internal_graph(self, reverse=False):
        graph = defaultdict(list)
        if reverse:
            g = self.G.reverse(copy=True)
        else:
            g = self.G
        for sbj, obj, info in g.edges(data=True):
            sbj_name = get_name_from_equivalent_ids(
                g.nodes[sbj]["equivalent_ids"], None
            )
            sbj_id = get_primary_id_from_equivalent_ids(
                g.nodes[sbj]["equivalent_ids"], g.nodes[sbj]["type"]
            )
            obj_name = get_name_from_equivalent_ids(
                g.nodes[obj]["equivalent_ids"], None
            )
            obj_id = get_primary_id_from_equivalent_ids(
                g.nodes[obj]["equivalent_ids"], g.nodes[obj]["type"]
            )
            sbj_label = (
                str(self.query_id - 1)
                + "-"
                + g.nodes[sbj]["identifier"]
                + ":"
                + str(sbj).upper()
            )
            obj_label = (
                str(self.query_id)
                + "-"
                + g.nodes[obj]["identifier"]
                + ":"
                + str(obj).upper()
            )
            tmp = []
            if sbj_label in self.prev_graph:
                prev_graph = copy.deepcopy(self.prev_graph[sbj_label])
                for prec_rec in prev_graph:
                    prec_rec.append(
                        {
                            "input": sbj_label,
                            "output": obj_label,
                            "info": info,
                            "input_name": sbj_name,
                            "input_id": sbj_id,
                            "output_name": obj_name,
                            "output_id": obj_id,
                        }
                    )
                    tmp.append(prec_rec)
            else:
                if not reverse:
                    tmp = [
                        [
                            {
                                "input": sbj_label,
                                "output": obj_label,
                                "info": info,
                                "input_name": sbj_name,
                                "input_id": sbj_id,
                                "output_name": obj_name,
                                "output_id": obj_id,
                            }
                        ]
                    ]
            graph[obj_label] += tmp
        self.current_graph = graph

    def query(self, verbose=False):
        """Query APIs and organize outputs into networkx graph."""
        self.current_graph = {}
        output_cls_name = " AND ".join(self.output_cls) if self.output_cls else "None"
        if verbose:
            print("==== Step #1: Query path planning ====")
            print(
                "\nBecause {} is of type '{}', BTE will query our meta-KG for APIs that can take '{}' as input and '{}' as output".format(
                    self.input_label, self.input_cls, self.input_cls, output_cls_name
                )
            )
        self.log.append("==== Step #1: Query path planning ====")
        self.log.append(
            "\nBecause {} is of type '{}', BTE will query our meta-KG for APIs that can take '{}' as input and '{}' as output".format(
                self.input_label, self.input_cls, self.input_cls, output_cls_name
            )
        )
        # filter edges based on subject, object, predicate
        edges = self.registry.filter_edges(self.input_cls, self.output_cls, self.pred)
        if not edges:
            # print("No edges found for the <input, pred, output> you specified")
            if verbose:
                print(
                    "We are sorry! We couln't find any APIs which can do the type of query for you!"
                )
            self.log.append(
                "We are sorry! We couln't find any APIs which can do the type of query for you!"
            )
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
                        m = listoftuples2dict(m)
                        m["value"] = v[p]
                        mapping_keys.append(m["label"])
                        input_edges.append(m)
                        output_id_types.append(m["operation"]["output_id"])
                    input_identifier = (
                        self.input_identifier
                        if self.input_identifier
                        else k.split(":", 1)[0]
                    )
                    self.G.add_node(
                        get_name_from_equivalent_ids(v, self.input_label),
                        type=self.input_cls,
                        identifier=input_identifier,
                        level=1,
                        equivalent_ids=self.equivalent_ids[k],
                    )
                    for _id in v[p]:
                        id_mapping[_id] = get_name_from_equivalent_ids(
                            v, self.input_label
                        )
        if not input_edges:
            if verbose:
                print(
                    "We are sorry! We couln't find any APIs which can do the type of query for you!"
                )
            self.log.append(
                "We are sorry! We couln't find any APIs which can do the type of query for you!"
            )
            return
        source_nodes_cnt = len(self.G)
        # make API calls and restructure API outputs
        (_res, log) = self.dp.dispatch(input_edges, verbose=verbose, loop=self.loop)
        self.log += log
        # load API outputs into the MultiDiGraph
        self.G = load_res_to_networkx(
            _res, self.G, mapping_keys, id_mapping, output_id_types
        )
        # annotate nodes with its equivalent ids
        self.G, out_equ_ids = add_equivalent_ids_to_nodes(self.G, self.idr)
        self.equivalent_ids.update(out_equ_ids)
        # merge equivalent nodes
        self.merge_equivalent_nodes()
        self.construct_internal_graph(reverse=self.reverse)
        if verbose:
            print(
                "\nAfter id-to-object translation, BTE retrieved {} unique objects.".format(
                    len(self.G) - source_nodes_cnt
                )
            )
        self.log.append(
            "\nAfter id-to-object translation, BTE retrieved {} unique objects.".format(
                len(self.G) - source_nodes_cnt
            )
        )

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
        """Retrieve output ids along with their equivalent ids."""
        result = {}
        if self.G.number_of_nodes() > 0:
            for x, y in self.G.nodes(data=True):
                if y["level"] and y["level"] == 2:
                    identifier = y["identifier"]
                    semantic_type = y["type"]
                    if semantic_type not in result:
                        result[semantic_type] = {}
                    curie = identifier + ":" + x
                    result[semantic_type][curie] = y["equivalent_ids"]
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
            raise Exception(
                "No edge exists between {} and {}".format(start_node, end_node)
            )
        return dict(self.G[start_node][end_node])

    def display_table_view(self):
        return networkx2pandas(self.G, self.input_cls)


class Explain:
    """Find intermediate node(s) that connect input and output
    
    There might not be direct evidence showing connection between A and B. \
        The "FindConnection" class aims at finding intermediate node(s) which both A and B are connected to.

    Parameters:
        input_obj: dict
            the input object returned from Hint, required
        output_obj: dict
            the output object returned from Hint, required
        intermediate_nodes: dict
            the semantic type(s) of the intermediate node
            could be None, which represents any semantic type, or a list of semantic types
        
    Examples
        >>> fc = FindConnection(input_obj=asthma, output_obj=imatinib, intermediate_nodes=[None])
        >>> fc.connect()

        >>> fc = FindConnection(input_obj=asthma, output_obj=imatinib, intermediate_nodes=['Gene'])
        >>> fc.connect()

        >>> fc = FindConnection(input_obj=asthma, output_obj=imatinib, intermediate_nodes=['Gene', 'ChemicalSubstance'])
        >>> fc.connect()

    """

    def __init__(self, input_obj, output_obj, intermediate_nodes=None, registry=None):
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        # convert intermediate_cls into a list if not
        if not intermediate_nodes:
            self.intermediate_cls = output_obj["type"]
            self.intermediate_cls_cnt = 0
        elif isinstance(intermediate_nodes, list):
            self.intermediate_cls = intermediate_nodes
            self.intermediate_cls_cnt = len(self.intermediate_cls)
        else:
            self.intermediate_cls = [intermediate_nodes]
            self.intermediate_cls_cnt = len(self.intermediate_cls)
        self.input_obj = input_obj
        # self.starts represents the display label of the input
        if "SYMBOL" in input_obj:
            self.starts = input_obj["SYMBOL"]
        elif "name" in input_obj:
            self.starts = input_obj["name"]
        else:
            self.starts = self.input_obj.get("primary").get(
                "identifier"
            ) + self.input_obj.get("primary").get("value")
        self.output_obj = output_obj
        # self.ends represents the display label of the output
        if "SYMBOL" in output_obj:
            self.ends = output_obj["SYMBOL"]
        elif "name" in output_obj:
            self.ends = output_obj["name"]
        else:
            self.ends = self.output_obj.get("primary").get(
                "identifier"
            ) + self.output_obj.get("primary").get("value")
        self.G = nx.MultiDiGraph()
        self.seqd = {}
        self.current_graph = {}
        self.log = []

    def connect(self, verbose=False):
        if verbose:
            print("==========")
            print("========== QUERY PARAMETER SUMMARY ==========")
            print("==========\n")
            print(
                "BTE will find paths that join '{}' and '{}'. Paths will have {} intermediate node.\n".format(
                    self.starts, self.ends, self.intermediate_cls_cnt
                )
            )
            if self.intermediate_cls_cnt > 0:
                for i, item in enumerate(self.intermediate_cls):
                    print(
                        "Intermediate node #{} will have these type constraints: {}\n\n".format(
                            i + 1, ",".join([str(j) for j in self.intermediate_cls])
                        )
                    )
            print("==========")
        self.log.append("==========")
        self.log.append("========== QUERY PARAMETER SUMMARY ==========")
        self.log.append("==========\n")
        self.log.append(
            "BTE will find paths that join '{}' and '{}'. Paths will have {} intermediate node.\n".format(
                self.starts, self.ends, self.intermediate_cls_cnt
            )
        )
        if self.intermediate_cls_cnt > 0:
            for i, item in enumerate(self.intermediate_cls):
                self.log.append(
                    "Intermediate node #{} will have these type constraints: {}\n\n".format(
                        i + 1, ",".join([str(j) for j in self.intermediate_cls])
                    )
                )
        self.log.append("==========")
        if self.intermediate_cls_cnt == 0:
            output_cls = self.intermediate_cls
        elif self.intermediate_cls == ["BiologicalEntity"]:
            output_cls = "Biological Entities"
        else:
            output_cls = " AND ".join(self.intermediate_cls) + " entities"
        if verbose:
            print(
                "========== QUERY #1 -- fetch all {} linked to '{}' ==========".format(
                    output_cls, self.starts
                )
            )
            print("==========\n")
        self.log.append(
            "========== QUERY #1 -- fetch all {} linked to '{}' ==========".format(
                output_cls, self.starts
            )
        )
        self.log.append("==========\n")
        self.seqd[1] = SingleEdgeQueryDispatcher(
            input_obj=self.input_obj,
            output_cls=self.intermediate_cls,
            query_id=1,
            registry=self.registry,
        )
        self.seqd[1].query(verbose=verbose)
        self.log += self.seqd[1].log
        if len(self.seqd[1].G) < 2:
            print(
                "The first query doesn't return any result. So BTE does not find any connection between your input and output"
            )
            return
        self.G = copy.deepcopy(self.seqd[1].G)
        if self.intermediate_cls_cnt == 0:
            if self.ends in self.G:
                found = ""
            else:
                found = "did not "
            if verbose:
                print("\n==========")
                print("========== Final assembly of results ==========")
                print("==========\n\n")
                print(
                    "BTE {}found direct connection between '{}' and '{}'".format(
                        found, self.starts, self.ends
                    )
                )
            self.log.append("\n==========")
            self.log.append("========== Final assembly of results ==========")
            self.log.append("==========\n\n")
            self.log.append(
                "BTE {}found direct connection between '{}' and '{}'".format(
                    found, self.starts, self.ends
                )
            )
        else:
            if verbose:
                print("\n\n==========")
                print(
                    "========== QUERY #2 -- fetch all {} linked to '{}' ==========".format(
                        output_cls, self.ends
                    )
                )
                print("==========\n")
            self.log.append("\n\n==========")
            self.log.append(
                "========== QUERY #2 -- fetch all {} linked to '{}' ==========".format(
                    output_cls, self.ends
                )
            )
            self.log.append("==========\n")
            self.seqd[2] = SingleEdgeQueryDispatcher(
                input_obj=self.output_obj,
                output_cls=self.intermediate_cls,
                prev_graph=self.seqd[1].current_graph,
                query_id=2,
                reverse=True,
                registry=self.registry,
            )
            self.seqd[2].query(verbose=verbose)
            if len(self.seqd[2].G) < 2:
                print(
                    "The second query doesn't return any result. So BTE does not find any connection between your input and output"
                )
                return
            self.log += self.seqd[2].log
            self.seqd[2].G = self.seqd[2].G.reverse()
            self.G = merge_two_networkx_graphs(self.G, self.seqd[2].G)
            self.sub_G = self.sub_graph()
            self.current_graph = self.seqd[2].current_graph
            if len(self.sub_G) <= 2:
                intermediate_cnt = 0
            else:
                intermediate_cnt = len(self.sub_G) - 2
            if verbose:
                print("\n==========")
                print("========== Final assembly of results ==========")
                print("==========\n\n")
                print(
                    "BTE found {} unique intermediate nodes connecting '{}' and '{}'".format(
                        intermediate_cnt, self.starts, self.ends
                    )
                )
            self.log.append("\n==========")
            self.log.append("========== Final assembly of results ==========")
            self.log.append("==========\n\n")
            self.log.append(
                "BTE found {} unique intermediate nodes connecting '{}' and '{}'".format(
                    intermediate_cnt, self.starts, self.ends
                )
            )

    def summary(self, attr):
        """"""

    def show_path(self, remove_duplicate=True):
        if remove_duplicate:
            paths = set()
            for path in nx.all_simple_paths(
                self.G, source=self.starts, target=self.ends
            ):

                path = "||".join(path)
                paths.add(path)
            new_paths = []
            for _path in paths:
                new_paths.append(_path.split("||"))
            return new_paths
        else:
            paths = []
            for path in nx.all_simple_paths(
                self.G, source=self.starts, target=self.ends
            ):
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
        """Convert the graph to visjs JSON format."""
        return networkx2graphvis(self.sub_G)

    def to_json(self):
        """Convert the graph into JSON through networkx."""
        if self.sub_G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(self.sub_G)
            return res
        return {}

    def show_all_nodes(self):
        """Show all nodes in the graph."""
        return list(self.sub_G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.sub_G.edges())

    def display_node_info(self, node):
        """Show detailed node information.

        :param: node: node id
        """
        if node not in self.G:
            raise Exception("{} is not in the graph".format(node))
        return self.G.nodes[node]

    def display_edge_info(self, start_node, end_node):
        """Display detailed edge info between start node and end node.

        :param: start_node: str, start node id
        :param: end_node: str, end node id
        """
        if start_node not in self.G:
            raise Exception("{} is not in the graph".format(start_node))
        if end_node not in self.G:
            raise Exception("{} is not in the graph".format(end_node))
        if not self.G.has_edge(start_node, end_node):
            raise Exception(
                "No edge exists between {} and {}".format(start_node, end_node)
            )
        return dict(self.G[start_node][end_node])

    def display_table_view(self):
        """Display the query results as a pandas table.
        
        Examples
        --------
        >>> df = fc.display_table_view()
        >>> df

        """
        return networkx2pandas(self.current_graph, self.input_obj["type"])


class Predict:
    """Find relationships between one specific entity and a class of entity types.
    
    params
    ------
    input_obj: the input object returned from Hint, required
    output_obj: the class of entities as output, required
        could be None, str, or a list of entity classes
    intermediate_nodes: the semantic type(s) of the intermediate node
        could be None, which represents any semantic type, or a list of semantic types
    
    """

    def __init__(self, input_obj, output_obj, intermediate_nodes, registry=None):
        """Initialize.
        params
        ------
        input_obj: the input object returned from Hint, required
        output_obj: the class of entities as output, required
            could be None, str, or a list of entity classes
        intermediate_nodes: the semantic type(s) of the intermediate node
            could be None, which represents any semantic type, or a list of semantic types
        
        """
        if not intermediate_nodes:
            intermediate_nodes = []
        elif not isinstance(intermediate_nodes, list):
            intermediate_nodes = [intermediate_nodes]
        self.intermediate_nodes = copy.deepcopy(intermediate_nodes)
        self.paths = copy.deepcopy(intermediate_nodes)
        # append output_obj to the path
        self.paths.append(output_obj)
        self.input_obj = input_obj
        if "SYMBOL" in input_obj:
            self.starts = input_obj["SYMBOL"]
        elif "name" in input_obj:
            self.starts = input_obj["name"]
        else:
            self.starts = self.input_obj.get("primary").get(
                "identifier"
            ) + self.input_obj.get("primary").get("value")
        self.ends = output_obj
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry
        self.G = nx.MultiDiGraph()
        self.seqd = {}
        # aggregate output_ids from different queries
        self.output_ids = {}
        self.current_graph = {}
        self.prev_graph = {}
        self.log = []

    def merge_output_ids(self, query_id, output_ids):
        level = query_id.split(".")[0]
        for _type, _ids in output_ids.items():
            if _type in self.output_ids[level]:
                self.output_ids[level][_type].update(_ids)
            else:
                self.output_ids[level][_type] = _ids

    def connect(self, verbose=False):
        """Make the query.
        
        params
        ------
        verbose: boolean, if True, print the progress and the summary
        """
        if verbose:
            print("==========")
            print("========== QUERY PARAMETER SUMMARY ==========")
            print("==========\n")
            print(
                "BTE will find paths that join '{}' and '{}'. Paths will have {} intermediate node.\n".format(
                    self.starts, self.ends, len(self.intermediate_nodes)
                )
            )
            for i, item in enumerate(self.intermediate_nodes):
                print(
                    "Intermediate node #{} will have these type constraints: {}\n".format(
                        i + 1, item
                    )
                )
        self.log.append("==========")
        self.log.append("========== QUERY PARAMETER SUMMARY ==========")
        self.log.append("==========\n")
        self.log.append(
            "BTE will find paths that join '{}' and '{}'. Paths will have {} intermediate node.\n".format(
                self.starts, self.ends, len(self.intermediate_nodes)
            )
        )
        for i, item in enumerate(self.intermediate_nodes):
            self.log.append(
                "Intermediate node #{} will have these type constraints: {}\n".format(
                    i + 1, item
                )
            )
        for i, output_cls in enumerate(self.paths):
            if i == 0:
                # if it's the first element in the path
                # the input should be the user provided input
                equivalent_ids = None
                input_obj = self.input_obj
                input_cls = input_obj["type"]
            else:
                # if it's not the first element in the path
                # the input should be the results from the previous query
                input_cls = self.paths[i - 1]
                equivalent_ids = copy.deepcopy(self.output_ids[str(i)])
                input_obj = None
            if (i > 0 and equivalent_ids != {}) or i == 0:
                if input_obj:
                    _input = copy.copy(self.starts)
                if output_cls == "BiologicalEntity":
                    _output = "Biological Entities"
                else:
                    if not isinstance(output_cls, list) or not isinstance(
                        output_cls, tuple
                    ):
                        output_cls = [output_cls]
                    _output = " AND ".join(output_cls) + " entities"
                self.output_ids[str(i + 1)] = {}
                if equivalent_ids:
                    for j, input_cls in enumerate(equivalent_ids.keys()):
                        query_id = str(i + 1) + "." + str(j + 1)
                        if verbose:
                            print(
                                "\n\n========== QUERY #{} -- fetch all {} linked to {} entites ==========".format(
                                    query_id, _output, input_cls
                                )
                            )
                            print("==========\n")
                        self.log.append(
                            "\n\n========== QUERY #{} -- fetch all {} linked to {} entites ==========".format(
                                query_id, _output, input_cls
                            )
                        )
                        self.log.append("==========\n")
                        self.seqd[query_id] = SingleEdgeQueryDispatcher(
                            input_obj=input_obj,
                            equivalent_ids=equivalent_ids[input_cls],
                            input_cls=input_cls,
                            output_cls=output_cls,
                            query_id=i + 1,
                            prev_graph=self.prev_graph,
                            pred=None,
                        )
                        self.seqd[query_id].query(verbose=verbose)
                        if len(self.seqd[query_id].G) < 2:
                            break
                        self.log += self.seqd[query_id].log
                        # print(seqd.G.nodes())
                        self.G = merge_two_networkx_graphs(
                            self.G, self.seqd[query_id].G
                        )
                        self.merge_output_ids(query_id, self.seqd[query_id].output_ids)
                        self.prev_graph.update(self.seqd[query_id].current_graph)
                        if i + 1 == len(self.paths):
                            self.current_graph.update(self.seqd[query_id].current_graph)
                    else:
                        continue
                    break
                else:
                    if verbose:
                        print(
                            "\n\n========== QUERY #{} -- fetch all {} linked to {} ==========".format(
                                i + 1, _output, _input
                            )
                        )
                        print("==========\n")
                    self.log.append(
                        "\n\n========== QUERY #{} -- fetch all {} linked to {} ==========".format(
                            i + 1, _output, _input
                        )
                    )
                    self.log.append("==========\n")
                    self.seqd[i + 1] = SingleEdgeQueryDispatcher(
                        input_obj=input_obj,
                        input_cls=input_cls,
                        output_cls=output_cls,
                        query_id=i + 1,
                        prev_graph=self.prev_graph,
                        pred=None,
                    )
                    self.seqd[i + 1].query(verbose=verbose)
                    if len(self.seqd[i + 1].G) < 2:
                        break
                    self.log += self.seqd[i + 1].log
                    self.G = merge_two_networkx_graphs(self.G, self.seqd[i + 1].G)
                    self.output_ids[str(i + 1)] = self.seqd[i + 1].output_ids
                    self.prev_graph.update(self.seqd[i + 1].current_graph)
                    if i + 1 == len(self.paths):
                        self.current_graph.update(self.seqd[i + 1].current_graph)

        if verbose:
            print("\n==========")
            print("========== Final assembly of results ==========")
            print("==========\n\n")
            for i in range(len(self.paths)):
                if self.output_ids.get(str(i + 1)):
                    for output_cls, _ids in self.output_ids[str(i + 1)].items():
                        print(
                            "In the #{} query, BTE found {} unique {} nodes".format(
                                i + 1, len(_ids), output_cls
                            )
                        )
        self.log.append("\n==========")
        self.log.append("========== Final assembly of results ==========")
        self.log.append("==========\n\n")
        for i in range(len(self.paths)):
            if self.output_ids.get(str(i + 1)):
                for output_cls, _ids in self.output_ids[str(i + 1)].items():
                    self.log.append(
                        "In the #{} query, BTE found {} unique {} nodes".format(
                            i + 1, len(_ids), output_cls
                        )
                    )

    def to_json(self):
        """convert the graph into JSON through networkx"""
        if self.G.number_of_nodes() > 0:
            res = nx.json_graph.node_link_data(self.G)
            return res
        return {}

    def show_path(self, remove_duplicate=True):
        # if the last query was not performed, return
        if not self.output_ids.get(str(len(self.paths))):
            return
        # gather all outputs from the last query
        final_outputs = set()
        for output_ids in self.output_ids.get(str(len(self.paths))).values():
            for k, item in output_ids.items():
                if item.get("SYMBOL"):
                    final_outputs.add(item["SYMBOL"][0])
                elif item.get("name"):
                    final_outputs.add(item["name"][0])
                else:
                    splitted = k.split(":")
                    if len(splitted) == 2:
                        final_outputs.add(splitted[-1])
                    elif len(splitted) == 3:
                        final_outputs.add(":".join(splitted[1:]))
        # if the last query returns no results, return
        if len(final_outputs) == 0:
            return
        if len(self.paths) == 1:
            paths = []
            for _node in final_outputs:
                paths.append([self.starts, _node])
            return paths
        if remove_duplicate:
            paths = set()
            for _node in final_outputs:
                for path in nx.all_simple_paths(
                    self.G, source=self.starts, target=_node
                ):

                    path = "||".join(path)
                    paths.add(path)
                new_paths = []
                for _path in paths:
                    new_paths.append(_path.split("||"))
            return new_paths
        paths = []
        for _node in final_outputs:
            for path in nx.all_simple_paths(
                self.G, source=self.starts, target=self.ends
            ):
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
            raise Exception(
                "No edge exists between {} and {}".format(start_node, end_node)
            )
        return dict(self.G[start_node][end_node])

    def show_all_nodes(self):
        """show all nodes in the graph"""
        return list(self.G.nodes())

    def show_all_edges(self):
        """show all edges in the graph"""
        return list(self.G.edges())

    def display_table_view(self):
        """Display the query results as a pandas table
        
        Examples
        --------
        >>> df = fc.display_table_view()
        >>> df
        """
        # paths = self.show_path()
        # return connect_networkx_to_pandas_df(self.G, paths)
        self.paths.insert(0, self.input_obj["type"])
        return networkx2pandas(self.current_graph, self.input_obj["type"])


class FindConnection:
    """Find relationships between one specific entity and another specific entity or other classes of entity types.

        Args:
            input_obj (required): must be an object returned from Hint corresponding to a specific biomedical entity.
                                Examples: 
                    Hint().query("Fanconi anemia")['DiseaseOrPhenotypicFeature'][0]
                    Hint().query("acetaminophen")['ChemicalSubstance'][0]

            output_obj (required): must EITHER be an object returned from Hint corresponding to a specific biomedical
                                entity, OR be a string or list of strings corresponding to Biolink Entity classes.
                                Examples:
                    Hint().query("acetaminophen")['ChemicalSubstance'][0]
                    'Gene'
                    ['Gene','ChemicalSubstance']

            intermediate_nodes (required): the semantic type(s) of the intermediate node(s).  Examples:
                    None                         : no intermediate node, find direct connections only
                    []                           : no intermediate node, find direct connections only
                    ['BiologicalEntity']         : one intermediate node of any semantic type
                    ['Gene']                     : one intermediate node that must be a Gene
                    [('Gene','Pathway')]         : one intermediate node that must be a Gene or a Pathway
                    ['Gene','Pathway']           : two intermediate nodes, first must be a Gene, second must be a Pathway.
                    ['Gene',('Pathway','Gene')]  : two intermediate nodes, first must be a Gene, second must be a Pathway or Gene.
                                                    **NOTE**: queries with more than one intermediate node are currently not supported
    
    **NOTE**: queries with more than one intermediate node are currently not supported
    """

    def __init__(self, input_obj, output_obj, intermediate_nodes, registry=None):
        """Find relationships in the Knowledge Graph between an Input Object and an Output Object.
        
        Args:
            input_obj (required): must be an object returned from Hint corresponding to a specific biomedical entity.
                                Examples:
                    Hint().query("Fanconi anemia")['DiseaseOrPhenotypicFeature'][0]
                    Hint().query("acetaminophen")['ChemicalSubstance'][0]

            output_obj (required): must EITHER be an object returned from Hint corresponding to a specific biomedical
                                entity, OR be a string or list of strings corresponding to Biolink Entity classes.
                                Examples:
                    Hint().query("acetaminophen")['ChemicalSubstance'][0]
                    'Gene'
                    ['Gene','ChemicalSubstance']

            intermediate_nodes (required): the semantic type(s) of the intermediate node(s).  Examples:
                    None                         : no intermediate node, find direct connections only
                    []                           : no intermediate node, find direct connections only
                    ['BiologicalEntity']         : one intermediate node of any semantic type
                    ['Gene']                     : one intermediate node that must be a Gene
                    [('Gene','Pathway')]         : one intermediate node that must be a Gene or a Pathway
                    ['Gene','Pathway']           : two intermediate nodes, first must be a Gene, second must be a Pathway.
                    ['Gene',('Pathway','Gene')]  : two intermediate nodes, first must be a Gene, second must be a Pathway or Gene.
                                                    **NOTE**: queries with more than one intermediate node are currently not supported
        """
        self.input_obj = input_obj
        self.output_obj = output_obj
        self.intermediate_nodes = intermediate_nodes
        if isinstance(output_obj, dict):
            self.fc = Explain(
                input_obj, output_obj, intermediate_nodes, registry=registry
            )
        else:
            self.fc = Predict(
                input_obj, output_obj, intermediate_nodes, registry=registry
            )

    def connect(self, verbose=False):
        self.fc.connect(verbose=verbose)

    def to_json(self):
        """Convert the graph into JSON through networkx."""
        return self.fc.to_json()

    def show_path(self, remove_duplicate=True):
        return self.fc.show_path(remove_duplicate=remove_duplicate)

    def display_node_info(self, node):
        """Show detailed node information.

        Parameters
            * node (str): node id
        """
        return self.fc.display_node_info(node)

    def display_edge_info(self, start_node, end_node):
        """Display detailed edge info between start node and end node.

        Parameters
            * start_node (str): start node id
            * end_node (str): end node id
        """
        return self.fc.display_edge_info(start_node, end_node)

    def show_all_nodes(self):
        """Show all nodes in the graph."""
        return self.fc.show_all_nodes()

    def show_all_edges(self):
        """Show all edges in the graph."""
        return self.fc.show_all_edges()

    def display_table_view(self):
        """Display the query results as a pandas table.
        
        **Examples**

        >>> df = fc.display_table_view()
        >>> df
        """
        return self.fc.display_table_view()

    def to_reasoner_std(self):
        """Convert the output to reasoner api standard.
        """
        rc = ReasonerConverter()
        rc.load_bte_query_path(
            start=self.input_obj,
            intermediate=self.intermediate_nodes,
            end=self.output_obj,
        )
        rc.load_bte_output(self.fc.G)
        return rc.generate_reasoner_response()

    def to_graphml(self, path):
        """Convert the output to graphml format.

        parameters
            * path (str): the file path to store the graphml file
        """
        rc = GraphmlConverter()
        rc.load_bte_output(self.fc.G)
        rc.generate_graphml_output(path)
        print("graphml file has been saved at {}".format(path))
