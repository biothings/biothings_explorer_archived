from collections import defaultdict


def restructure_scibite_response(json_doc):
    """restructure the JSON output from AUTOMAT SCIBITE API

    parameters
        * json_doc: the API response from AUTOMAT SCIBITE API
    """
    # convert from list to dict
    if json_doc['data'] == []:
        return {}
    res = defaultdict(set)
    for rec in json_doc['data']:
        obj = rec[-1]
        obj_id_prefix = obj['id'].split(':')[0]
        if obj_id_prefix in ['MONDO', 'CHEBI', 'DOID']:
            res[obj_id_prefix.lower()].add(obj['id'])
        elif obj_id_prefix in ['NCBIGene', 'ENSEMBL']:
            res[obj_id_prefix.lower()].add(obj['id'].split(':', 1)[-1])
        elif obj_id_prefix == 'CHEMBL.COMPOUND':
            res['chembl'].add(obj['id'].split(':', 1)[-1])
        obj = rec[0]
        obj_id_prefix = obj['id'].split(':')[0]
        if obj_id_prefix in ['MONDO', 'CHEBI', 'DOID']:
            res[obj_id_prefix.lower()].add(obj['id'])
        elif obj_id_prefix in ['NCBIGene', 'ENSEMBL']:
            res[obj_id_prefix.lower()].add(obj['id'].split(':', 1)[-1])
        elif obj_id_prefix == 'CHEMBL.COMPOUND':
            res['chembl'].add(obj['id'].split(':', 1)[-1])
    new_res = {}
    for k, v in res.items():
        new_res[k] = list(v)
    return {'associated_with': new_res}
