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
                path_data['pred' + str(i + 1)] = retrieve_prop_from_edge(edge['info'], 
                                                                         'relation')
                path_data['pred' + str(i + 1) +
                          '_source'] = retrieve_prop_from_edge(edge['info'],
                                                               'source')
                path_data['pred' + str(i + 1) +
                          '_api'] = retrieve_prop_from_edge(edge['info'],
                                                            'api')
                path_data['pred' + str(i + 1) +
                          '_pubmed'] = retrieve_prop_from_edge(edge['info'],
                                                               'pubmed')
                path_data['pred' + str(i + 1) +
                          '_method'] = retrieve_prop_from_edge(edge['info'],
                                                               'category')                
                node = 'output' if i + 1 == len(path) else 'node' + str(i + 1)
                path_data[node + '_type'] = edge['info']['info']['@type']
                path_data[node + '_name'] = edge['output_name']
                path_data[node + '_id'] = edge['output_id']
            data.append(path_data)
    return pd.DataFrame(data).drop_duplicates()


def retrieve_prop_from_edge(edge_info, prop):
    """
    Retrieve property info from the edge data.

    :param: edge_info: dictionary of edge information
    :param: prop: string, specific information you want from this dictionary

    Output:
         string, the specific information for that edge
    
    The edge_info is a dictionary with the following keys: 
        * info: a dictionary with the following possible keys: 
            * 'category': a list of strings, the method (how the info was generated)
            * 'SYMBOL', 'name', 'ULMS', 'MGI' keys: value is a string identifier
            * 'pubmed': list of strings, pubmed IDs
            * 'taxid': list of strings (NCBITaxon curies)
            * 'source': list of strings (resource the API drew from to get this info)
            * 'relation': list of strings (relationship)
            * always there: '$api' string, the API this info came from   
            * always there: '$source': like source, but annotated by SmartAPI rather than the API itself
            * always there: '@type': string, BioThings type of output  
        * label: like relation, but annotated by SmartAPI rather than the API itself 
    """
    if prop == 'api':
        data = edge_info['info'].get('$api')
        if data:
            if not isinstance(data, list):
                data = [data]
            return ','.join(data)
    elif prop == 'source':
        ## try getting source from inner dictionary, from api
        data = edge_info['info'].get('source')
        ## if that didn't work, get source from SmartAPI
        if not data:
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
    elif prop == 'relation':  
        ## try getting source from inner dictionary, from api        
        data = edge_info['info'].get('relation')
        ## if that didn't work, get source from SmartAPI
        if not data:
            data = edge_info.get('label')  
        if data:  
            if not isinstance(data, list):
                data = [data]
            data = [item.replace(" ", "_") for item in data]
            return ','.join(data)    
    elif prop == 'category':  
        data = edge_info['info'].get('category')
        if data:  
            if not isinstance(data, list):
                data = [data]
            data = [item.replace(" ", "_") for item in data]
            return ','.join(data)           