"""
Function for filtering based on the label of an edges (ie. related_to, positively_regulates, etc)

Parameters:
    G - A networkX graph
    label - label to look for or a list of labels
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results that fit the label
"""
from edges import filter_node_degree

def filter_label(G, label, count=50):

    val_edges = []
    for edge in G.edges:
        if G[edge[0]][edge[1]][edge[2]]['label'] in label:
            val_edges.append(edge)

    subG = G.edge_subgraph(val_edges)
    subG = filter_node_degree(subG, count, 'EdgeLabel')

    return subG
