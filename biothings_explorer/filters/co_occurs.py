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

    # helper functions

    # function to get all MESH/UMLS ids of a node
    def get_ids(node):
        ids = []
        if 'MESH' in G.nodes[node]['equivalent_ids'].keys():
            ids.append(G.nodes[node]['equivalent_ids']['MESH'])
        if 'UMLS' in G.nodes[node]['equivalent_ids'].keys():
            ids.append(G.nodes[node]['equivalent_ids']['UMLS'])

        ids = [i for sub in ids for i in sub] # flatten and get rid of set()
        return 0 if len(ids) == 0 else ids

    # function to make combos of source/targets used to query the API
    def make_combo(id1, id2):
        combos = ['-'.join([i,j]) for i in id1 for j in id2]
        combos += ['-'.join([j,i]) for i in id1 for j in id2]
        return combos

    # begin code
    unique_edges = []
    # get sources and targets
    sources = [x for x,y in G.nodes(data=True) if y['level']==1]
    targets = [x for x,y in G.nodes(data=True) if y['level']==2]

    # get all source/target combos
    for source in sources:
        for target in targets:
            if G.has_edge(source,target):
                unique_edges.append([source,target])

    num_combs, combos = [], []
    # loop through each unique edge
    for edge in unique_edges:
        # get source and target IDs
        src_id = get_ids(edge[0])
        tar_id = get_ids(edge[1])

        # error code 100 if one of the source or target didn't have any ids
        if (src_id == 0) | (tar_id == 0):
            edge.insert(0, 100)
        else:
            # both IDs present, make combos and add to list
            combo = make_combo(src_id, tar_id)
            combos.append(combo)
            num_combs.append(len(combo))

    # flatten the list
    combos = [i for j in combos for i in j]
    # break into chunks -- can only query 1000 at a time
    chunks = [combos[x:x+1000] for x in range(0,len(combos),1000)]

    # make post request
    x = []
    for chunk in chunks:
        x += requests.post('https://biothings.ncats.io/mrcoc/query', json={'scopes':'combo', 'q': chunk}).json()

    end, i = 0, 0
    for edge in unique_edges:
        if isinstance(edge[0],int): # skip if 100 error code
            continue
        # start/end signify length of results for that edge, since each edge has different number of combos
        start = end
        end += num_combs[i]
        # loop through each result for that edge
        for query in x[start:end]:
            # break out of loop when a result is valid
            if not 'notfound' in query:
                edge.insert(0, query['ngd_overall'])
                break
        # if no result was found, error code 200
        if not isinstance(edge[0], float):
            edge.insert(0, 200)
        i+=1

    # sort results and get top 'count'
    results = sorted(unique_edges)[:count]
    # add sources to create subgraph of 'count' targets and all sources
    filtered = [i[2] for i in results] + sources
    subG = G.subgraph(filtered)

    # annotate with rank, filteredBy and which source that target co-occurred with
    for i,res in enumerate(results, start=1):
        # some targets can have multiple hits, see bottom of demo notebook when using this filter with intermediate nodes
        if 'rank' not in subG.nodes[res[2]].keys():
            subG.nodes[res[2]]['rank'] = i
            subG.nodes[res[2]]['filteredBy'] = 'CoOccurrence'
            subG.nodes[res[2]]['ngd_overall'] = res[0]
            subG.nodes[res[2]]['co_occur_with'] = res[1]
        elif isinstance(subG.nodes[res[2]]['rank'],list):
            subG.nodes[res[2]]['rank'].append(i)
            subG.nodes[res[2]]['ngd_overall'].append(res[0])
            subG.nodes[res[2]]['co_occur_with'].append(res[1])
        else: # create list for duplicate node
            subG.nodes[res[2]]['rank'] = [subG.nodes[res[2]]['rank'],i]
            subG.nodes[res[2]]['ngd_overall'] = [subG.nodes[res[2]]['ngd_overall'],res[0]]
            subG.nodes[res[2]]['co_occur_with'] = [subG.nodes[res[2]]['co_occur_with'],res[1]]

    return subG
