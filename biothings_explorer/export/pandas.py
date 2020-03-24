# -*- coding: utf-8 -*-
"""
Export the output of BTE to pandas data frame.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

import pandas as pd


def networkx2pandas(current_graph, input_type):
    """Converting current graph into a pandas data frame

    :param: current_graph: a python dict containing all paths
    :param: input_type: the semantic type of the input
    """
    data = []
    for paths in current_graph.values():
        for path in paths:
            path_data = {}
            for i, edge in enumerate(path):
                if i == 0:
                    path_data['input'] = edge['input_name']
                    path_data['input_type'] = input_type
                path_data['pred' + str(i + 1)] = edge['info']['label']
                path_data['pred' + str(i + 1) +
                          '_source'] = retrieve_prop_from_edge(edge['info'],
                                                               'source')
                path_data['pred' + str(i + 1) +
                          '_api'] = retrieve_prop_from_edge(edge['info'],
                                                            'api')
                path_data['pred' + str(i + 1) +
                          '_pubmed'] = retrieve_prop_from_edge(edge['info'],
                                                               'pubmed')
                node = 'output' if i + 1 == len(path) else 'node' + str(i + 1)
                path_data[node + '_type'] = edge['info']['info']['@type']
                path_data[node + '_name'] = edge['output_name']
                path_data[node + '_id'] = edge['output_id']
            data.append(path_data)
    return pd.DataFrame(data).drop_duplicates()


def retrieve_prop_from_edge(edge_info, prop):
    """Retrieve property info from the edge data."""
    if prop == 'api':
        data = edge_info['info'].get('$api')
        if data:
            if not isinstance(data, list):
                data = [data]
            return ','.join(data)
    elif prop == 'source':
        data = edge_info['info'].get('$source')
        if data:
            if not isinstance(data, list):
                data = [data]
            return ','.join(data)
    elif prop == 'pubmed':
        data = edge_info['info'].get('pubmed')
        if data:
            if not isinstance(data, list):
                data = [data]
            else:
                data = [str(item) if not isinstance(item, str) else item
                        for item in data]
            return ','.join(data)
