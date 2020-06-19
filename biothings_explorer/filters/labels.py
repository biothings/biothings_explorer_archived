"""
Function for filtering based on the label of an edges (ie. related_to, positively_regulates, etc)

Parameters:
    G - A networkX graph
    label - label to look for
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results that fit the label
"""

def filter_label(G, label, count=50):

    val_edges = []
    for edge in G.edges:
        if G[edge[0]][edge[1]][0]['label'] == label:
            val_edges.append(edge)

    subG = G.edge_subgraph(val_edges)
    subG = filter_node_degree(subG, count)

    for node in subG.nodes:
        subG.nodes.data()[node]['filteredBy'] = 'EdgeLabel'

    return subG
