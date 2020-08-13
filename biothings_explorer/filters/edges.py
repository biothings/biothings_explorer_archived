"""
Function for filtering based on the number of edges connected to each node/degree

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results
"""
# TO DO: fix other 2 filter functions to deal w/ intermediate nodes
#        add some key for each node so we know which ones are returned in which step of the query process
#               (ex. if NodeDegree is used for inter1 and the target type, then there will be two sets
#                of nodes which are labeled with filteredBy=NodeDegree, can't differentiate right now)
def filter_node_degree(G, count=50, filt='NodeDegree'):

    sources = [x for x,y in G.nodes(data=True) if y['level']==1]
    targets = [x for x,y in G.nodes(data=True) if y['level']==2]

    degrees = []
    for target in targets:
        degrees.append([G.degree(target), target])

    degrees = sorted(degrees, reverse=True)[:count]

    filtered = [i[1] for i in degrees] + sources
    subG = G.subgraph(filtered)

    for i,node in enumerate(filtered[:-len(sources)], start=1):
        subG.nodes.data()[node]['filteredBy'] = filt
        subG.nodes.data()[node]['rank'] = i

    return subG
