"""
Function for simple filter that ranks items (edges of graph) by co-occurrence
 in literature using only average frequency per year

Parameters:
    G - A networkX graph
    count - number of nodes to return (default=50)

Returns:
    A networkX graph with the top count results

    * not yet functional *
"""

# simple filter that ranks items (edges of graph) by co-occurrence in literature using only average frequency per year

def filter_co_occurs_avg(G, count=50):

    def get_ids(node):
        ids = []
        try:
            ids.append(seqd.G.nodes[node]['equivalent_ids']['MESH'])
            ids.append(seqd.G.nodes[node]['equivalent_ids']['UMLS'])
        except:
            pass

        ids = [i for sub in ids for i in sub] # flatten and get rid of set()

        if len(ids) == 0:
            return 0
        else:
            return ids

    avgs = []
    for edge in G.edges.data():

        # get the ids
        ids = []
        ids.append(get_ids(edge[0]))
        ids.append(get_ids(edge[1]))


        if 0 in ids: # at least 1 doesn't have an ID
            edge[2]['rank'] = 0
            edge[2]['filteredBy'] = 'CoOccurrence'
            continue

        freq, numYears = 0,0

        linenum = 0
        # look for IDs in file
        with open('NIH_CoOccurs/summary_CoOccurs_2019.txt') as fp:
            for line in fp:
                line = line.strip().split('|')

                if (((line[0] in ids[0]) | (line[1] in ids[0])) & ((line[2] in ids[1]) | (line[3] in ids[1]))) | \
                (((line[0] in ids[1]) | (line[1] in ids[1])) & ((line[2] in ids[0]) | (line[3] in ids[0]))):
                    freq += int(line[4])
                    numYears += 1
                else:
                    if numYears > 0:
                        break # seems like all co-occs for a given pair are adjacent, don't need to go thru whole file
        fp.close()

        if numYears > 0:
            avgs.append([freq/numYears, edge[0], edge[1]]) #avg,node1,node2

    print('Exit loop')
    avgs.sort(reverse=True)

    print('Ranking nodes')
    # rank them
    for i in range(count):
        for edge in range(len(G[avgs[i][0]][avgs[i][1]])): # account for nodes w/ >1 edge
            G[avgs[i][0]][avgs[i][1]][edge]['rank'] = i+1
            G[avgs[i][0]][avgs[i][1]][edge]['filteredBy'] = 'CoOccurrence'
            G[avgs[i][0]][avgs[i][1]][edge]['avg'] = avgs[i][0]

    fp.close()
    return G
