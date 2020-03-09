from itertools import groupby

def restructure_reasoner_response(json_doc):
    """Restructure the API output from reasoner API.
    
    parameters
    ----------
    json_doc: json output from reasoner API
    """
    edges = json_doc['knowledge_graph']['edges']
    if not edges:
        return {}
    res = {}
    edges = sorted(edges, key=lambda x: x['type'])
    for k, g in groupby(edges, lambda x: x['type']):
        res[k] = []
        for _item in g:
            if _item['target_id'].startswith("PANTHER.FAMILY"):
                _item['panther'] = _item['target_id'][15:]
            res[k].append(_item)
    return res