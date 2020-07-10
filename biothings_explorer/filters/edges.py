"""
Function for filtering based on the number of edges connected to each node/degree

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results
"""
import pandas as pd

def filter_node_degree(G, count=50, filt='NodeDegree'):

    source = [x for x,y in G.nodes(data=True) if y['level']==1][0]
    degrees = [[],[]]
    for node in G.nodes:
        if node != source:
            degrees[0].append(node)
            degrees[1].append(G.degree(node))

    data = {'node':degrees[0], 'degree':degrees[1]}
    deg_count = pd.DataFrame(data=data)
    deg_count.sort_values(by='degree', inplace=True, ascending=False)

    filtered = list(deg_count.head(count)['node']) + [source]
    subG = G.subgraph(filtered)

    for i,node in enumerate(filtered[:-1], start=1):
        subG.nodes.data()[node]['filteredBy'] = filt
        subG.nodes.data()[node]['rank'] = i

    return subG
