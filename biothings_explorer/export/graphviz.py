# -*- coding: utf-8 -*-
"""
Export the output of BTE to graphviz.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""
from graphviz import Digraph


def visualize(edges, size=None):
    """Export networkx graph into graphviz format for jupyter notebook visualization.

    :param: edges: the edge representation of the graph
    :param: size: the size of the output graph, e.g. (6, 8)
    """
    if size:
        d = Digraph(graph_attr=[('size', size)])    # pylint: disable=undefined-variable
    else:
        d = Digraph()                               # pylint: disable=undefined-variable
    for _item in edges:
        d.edge(_item[0], _item[1])
    return d

def networkx2graphvis(G):
    f = Digraph()
    for k, v, j in G.edges(data=True):
        f.edge(k, v, j['label'])
    return f