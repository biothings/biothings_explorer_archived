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

    # helper methods
    def get_ids(node):
        ids = []
        try:
            ids.append(G.nodes[node]['equivalent_ids']['MESH'])
            ids.append(G.nodes[node]['equivalent_ids']['UMLS'])
        except:
            pass
        ids = [i for sub in ids for i in sub] # flatten and get rid of set()
        return 0 if len(ids) == 0 else ids

    def make_combo(id1, id2):
        combos = ['-'.join([i,j]) for i in id1 for j in id2]
        combos += ['-'.join([j,i]) for i in id1 for j in id2]
        return combos

    # begin code
    unique_edges = []
    for edge in G.edges:
        if [edge[0], edge[1]] in unique_edges:
            continue
        else:
            unique_edges.append([edge[0], edge[1]])

    for edge in unique_edges:
        id1 = get_ids(edge[0])
        id2 = get_ids(edge[1])

        if (id1 == 0) | (id2 == 0):
            edge.insert(0, 100)
        else:
            combo = make_combo(id1, id2)
            x = requests.post('https://biothings.ncats.io/mrcoc/query', json={'scopes':'combo', 'q': combo}).json()
            for query in x:
                if not 'notfound' in query:
                    edge.insert(0, query['ngd_overall'])
                    break
            if not isinstance(edge[0], float):
                edge.insert(0, 200)

    results = sorted(unique_edges)[:count]
    filtered = list(set([i[1] for i in results] + [i[2] for i in results]))
    subG = G.subgraph(filtered)

    for i,res in enumerate(results, start=1):
        for edge in subG[res[1]][res[2]]:
            subG[res[1]][res[2]][edge]['rank'] = i
            subG[res[1]][res[2]][edge]['filteredBy'] = 'CoOccurrence'
            subG[res[1]][res[2]][edge]['ngd_overall'] = res[0]

    return subG
