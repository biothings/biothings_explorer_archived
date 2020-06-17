"""
Function for filtering based on the number of edges connected to each node

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results
"""

def filter_num_edges(G, count=50): #takes input G as networkX graph

    degrees = []
    for i,node in enumerate(G.nodes):
        degrees.append(G.degree(node))

    data = {'node':G.nodes, 'degree':degrees}
    deg_count = pd.DataFrame(data=data)
    deg_count.sort_values(by='degree', inplace=True, ascending=False)

    filtered = list(deg_count.head(count)['node'])
    subG = G.subgraph(filtered)

    for i,node in enumerate(filtered):
        subG.nodes.data()[node]['filteredBy'] = 'edges'
        subG.nodes.data()[node]['rank'] = i+1

    return subG
