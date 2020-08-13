"""
Function for filtering based on the number of unique APIs supporting the
association between the source and target nodes

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results
"""

def filter_api(G, count=50):

    sources = [x for x,y in G.nodes(data=True) if y['level']==1]
    targets = [x for x,y in G.nodes(data=True) if y['level']==2]

    counts = []
    for target in targets:
        apis = set()
        for source in sources:
            try:
                for edge in G[source][target]:
                    apis.add(G[source][target][edge]['info']['$api'])
            except:
                pass
        counts.append([len(apis), target])
        
    counts = sorted(counts, reverse=True)[:count]
    filtered = [i[1] for i in counts] + sources
    subG = G.subgraph(filtered)

    for i,node in enumerate(filtered[:-len(sources)], start=1):
        subG.nodes.data()[node]['filteredBy'] = 'UniqueAPIs'
        subG.nodes.data()[node]['rank'] = i

    return subG
