# -*- coding: utf-8 -*-
"""
Export the output of BTE to vis.js accepted format.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""


def networkx_json_to_visjs(res):
    """Convert JSON output from networkx to visjs compatible version.

    :param: res: JSON output from networkx of the graph
    """
    colors = {1: 'green', 2: 'red', 3: 'rgba(255,168,7)'}
    if res:
        links = res['links']
        new_links = []
        for _link in links:
            _link['from'] = _link.pop('source')
            _link['to'] = _link.pop('target')
            _link['font'] = {'align': 'middle'}
            _link['arrows'] = 'to'
            new_links.append(_link)
        res['links'] = new_links
        new_nodes = []
        for _node in res['nodes']:
            _node['label'] = _node['identifier'] + ':' + str(_node['id'])
            _node['color'] = colors[_node['level']]
            if 'equivalent_ids' in _node:
                equ_ids = []
                for k, v in _node['equivalent_ids'].items():
                    if isinstance(v, list):
                        for _v in v:
                            equ_ids.append(k + ':' + str(_v))
                    else:
                        equ_ids.append(k + ":" + str(v))
                equ_ids = '<br>'.join(equ_ids)
                _node['equivalent_ids'] = equ_ids
            new_nodes.append(_node)
        res['nodes'] = new_nodes
    return res
