# -*- coding: utf-8 -*-
"""A collection of util functions related to networkx

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

from collections import defaultdict


def load_res_to_networkx(_res, G, labels, id_mapping, output_id_types):
    """Load restructured API response into a networkx MultiDiGraph.

    Parameters
        * G: networkx MultiDiGraph
        * _res: restructured API response
        * labels: list of schema properties to extract from API response
        * id_mapping: dict containing mapping between equivalent ids and original ids
        * output_id_types: list of output identifiers
    """
    # check if API response is empty
    if not _res:
        return G
    # m represent input id, n represent parsed API output
    for input_id, parsed_api_output in _res.items():
        if not parsed_api_output:
            continue
        # a represent schema property, b represent value
        for prop, prop_vals in parsed_api_output.items():
            if prop not in labels:
                continue
            for _val in prop_vals:
                if not isinstance(_val, dict):
                    G.add_node(
                        str(_val),
                        identifier=prop,
                        type=parsed_api_output["@type"],
                        level=2,
                    )
                    G.add_edge(id_mapping[input_id], str(_val), info=None, label=prop)
                else:
                    for i, j in _val.items():
                        if i in output_id_types and j:
                            output_type = _val.get("@type")
                            source = _val.get("$source")
                            if not isinstance(j, list):
                                j = [j]
                            j = [str(jj) for jj in j]
                            G.add_nodes_from(j, identifier=i, type=output_type, level=2)
                            for _j in j:
                                G.add_edge(
                                    id_mapping[input_id],
                                    _j,
                                    info=_val,
                                    label=prop,
                                    source=source,
                                )
    return G


def add_equivalent_ids_to_nodes(G, IDResolver):
    """Add equivalent ids to each node.

    Parameters
        * G: Networkx Graph
        * IDConverter: Python Class in BTE to convert IDs

    TODO: This is weird, shouldn't include IDConverter in this.
    """
    # check if G is empty
    if not G:
        return (G, {})
    # get all nodes which are level 2 (output nodes)
    output_ids = [x for x, y in G.nodes(data=True) if y and y["level"] == 2]
    # check if there is no output nodes
    if not output_ids:
        return (G, {})
    # group output ids based on identifier and type
    idc_inputs = []
    output_ids_dict = defaultdict(list)
    for _id in output_ids:
        type_identifier = G.nodes[_id]["type"] + "," + G.nodes[_id]["identifier"]
        output_ids_dict[type_identifier].append(_id)
    # construct inputs for IDConverter
    for k, v in output_ids_dict.items():
        input_cls, input_id = k.split(",")
        idc_inputs.append((v, input_id, input_cls))
    # find equivalent ids
    equivalent_ids = IDResolver.resolve_ids(idc_inputs)
    # populate nodes with equivalent ids
    for m, n in equivalent_ids.items():
        G.nodes[m.split(":", 1)[-1]]["equivalent_ids"] = n
    return (G, equivalent_ids)


def merge_two_networkx_graphs(G1, G2):
    """Merge two networkx MultiDiGraphs.

    :param: G1: networkx graph as the source graph
    :param: G2: networkx graph added to G1

    TODO: line G1.add_edges_from(G2.edges(data=True)) will introduce duplicate edges
    """
    nodes_to_add = []
    for k, v in G2.nodes(data=True):
        if k not in G1:
            nodes_to_add.append((k, v))
    G1.add_nodes_from(nodes_to_add)
    G1.add_edges_from(G2.edges(data=True))
    return G1
