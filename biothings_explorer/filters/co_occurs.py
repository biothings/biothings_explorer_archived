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

    # helper funcs
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
    source = [x for x,y in G.nodes(data=True) if y['level']==1][0]
    for node in G.nodes:
        if node != source:
            unique_edges.append([source,node])

    num_combs, combos = [], []
    src_id = get_ids(source)
    for edge in unique_edges:
        tar_id = get_ids(edge[1])

        if (src_id == 0) | (tar_id == 0):
            edge.insert(0, 100)
        else:
            combo = make_combo(src_id, tar_id)
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
    filtered = [i[2] for i in results] + [source]
    subG = G.subgraph(filtered)

    for i,res in enumerate(results, start=1):
        subG.nodes[res[2]]['rank'] = i
        subG.nodes[res[2]]['filteredBy'] = 'CoOccurrence'
        subG.nodes[res[2]]['ngd_overall'] = res[0]

    return subG
