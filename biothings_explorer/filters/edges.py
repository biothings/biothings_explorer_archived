"""
Function for filtering based on the number of edges connected to each node/degree

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results
"""

def filter_node_degree(G, count=50, filt='NodeDegree'):

    # get sources and targets
    sources = [x for x,y in G.nodes(data=True) if y['level']==1]
    targets = [x for x,y in G.nodes(data=True) if y['level']==2]

    # get degrees for each target node
    degrees = []
    for target in targets:
        degrees.append([G.degree(target), target])

    # sort degrees highest to lowest, get 'count' number
    degrees = sorted(degrees, reverse=True)[:count]

    # include sources in subgraph
    filtered = [i[1] for i in degrees] + sources
    subG = G.subgraph(filtered)

    # annotate nodes with rank and filter used
    for i,node in enumerate(filtered[:-len(sources)], start=1):
        subG.nodes.data()[node]['filteredBy'] = filt
        subG.nodes.data()[node]['rank'] = i

    return subG
