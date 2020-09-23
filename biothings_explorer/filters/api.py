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

    # get sources and targets
    sources = [x for x,y in G.nodes(data=True) if y['level']==1]
    targets = [x for x,y in G.nodes(data=True) if y['level']==2]

    # get number of unique APIs supporting each target/source combo
    counts = []
    for target in targets:
        apis = set()
        for source in sources:
            try: # some target/source combos don't exist
                for edge in G[source][target]:
                    apis.add(G[source][target][edge]['info']['$api'])
            except:
                pass
        counts.append([len(apis), target])

    # sort and get 'count' number of targett nodes
    counts = sorted(counts, reverse=True)[:count]
    # add in sources to make subgraph
    filtered = [i[1] for i in counts] + sources
    subG = G.subgraph(filtered)

    # annotate target nodes with rank and filter used
    for i,node in enumerate(filtered[:-len(sources)], start=1):
        subG.nodes.data()[node]['filteredBy'] = 'UniqueAPIs'
        subG.nodes.data()[node]['rank'] = i

    return subG
