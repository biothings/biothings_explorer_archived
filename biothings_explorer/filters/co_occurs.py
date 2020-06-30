"""
Function for filter that ranks items (edges of graph) by co-occurrence
    by sending batch queries to the MRCOC co-occurrence API

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX subgraph with 'count' number of unique edges
    Number of edges between two nodes are preserved and have same rank
    Each edge in returned graph labeled with rank and ngd_overall

# error codes for NGD :
#      100 : ID (mesh or umls) not found for at least 1 of the nodes
#      200 : query not found for pair of nodes
"""

import requests

def filter_co_occur(G, count=50):
    unique_edges = []
    for edge in G.edges:
        if [edge[0], edge[1]] in unique_edges:
            continue
        else:
            unique_edges.append([edge[0], edge[1]])

    num_combs, combos = [], []
    for edge in unique_edges:
        id1 = get_ids(edge[0])
        id2 = get_ids(edge[1])

        if (id1 == 0) | (id2 == 0):
            edge.insert(0, 100)
        else:
            combo = make_combo(id1, id2)
            combos.append(combo)
            num_combs.append(len(combo))

    combos = [i for j in combos for i in j]
    chunks = [combos[x:x+1000] for x in range(0,len(combos),1000)]
    x = []
    for chunk in chunks:
        x += requests.post('https://biothings.ncats.io/mrcoc/query', json={'scopes':'combo', 'q': chunk}).json()

    end, i = 0, 0
    for edge in unique_edges:
        if isinstance(edge[0],int):
            continue
        start = end
        end += num_combs[i]
        for query in x[start:end]:
            if not 'notfound' in query:
                edge.insert(0, query['ngd_overall'])
                break
        if not isinstance(edge[0], float):
            edge.insert(0, 200)
        i+=1

    results = sorted(unique_edges)[:count]
    filtered = list(set([i[1] for i in results] + [i[2] for i in results]))
    subG = G.subgraph(filtered)

    for i,res in enumerate(results, start=1):
        for edge in subG[res[1]][res[2]]:
            subG[res[1]][res[2]][edge]['rank'] = i
            subG[res[1]][res[2]][edge]['filteredBy'] = 'CoOccurrence'
            subG[res[1]][res[2]][edge]['ngd_overall'] = res[0]

    return subG
