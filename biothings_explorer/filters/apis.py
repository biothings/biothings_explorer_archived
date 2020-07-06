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
    counts = []
    for node in G.nodes:
        if node == source:
            continue
        apis = set()
        for edge in G[source][node]:
            apis.add(G[source][node][edge]['info']['$api'])
        counts.append([len(apis), node])

    counts = sorted(counts, reverse=True)[:count]
    filtered = [i[1] for i in counts] + [source]
    subG = G.subgraph(filtered)

    for i,node in enumerate(filtered[:-1], start=1):
        subG.nodes.data()[node]['filteredBy'] = 'UniqueAPIs'
        subG.nodes.data()[node]['rank'] = i

    return subG
