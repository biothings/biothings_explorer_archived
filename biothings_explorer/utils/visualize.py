from data_tools import plotting as dtp
import warnings

def visualize(df):
    warnings.filterwarnings('ignore')
    if len(df) == 0:
        return
    if len(df) > 10:
        df = df.sample(10)
    records = df.to_dict('records')
    nodes = []
    links = []
    for item in records:
        tmp_node = [item['input']]
        tmp_link = []
        for i in range(1, 4):
            node_id = 'node' + str(i) + '_name'
            if node_id in item:
                tmp_node.append(item[node_id])
            else:
                break
            tmp_node.append(item['output_name'])
        nodes.append(tmp_node)
        for i in range(0, 3):
            edge_id = 'pred' + str(i)
            if edge_id in item:
                tmp_link.append(item[edge_id])
        links.append(tmp_link)
    G = dtp.build_explanitory_graph(nodes, links)
    return dtp.draw_explanitory_graph(G)