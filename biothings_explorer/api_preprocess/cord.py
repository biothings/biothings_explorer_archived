from copy import deepcopy

def restructure_cord_response(json_doc, output_types):
    """Restructure the JSON output from cord API.

    :param: json_doc: the API response from cord API
    """
    if not isinstance(json_doc, list):
        return json_doc
    new_res = []
    for _res in json_doc:
        if not isinstance(_res, dict):
            continue
        # handle case where the queried item is not found
        if _res.get('notfound'):
            continue
        tmp_res = {'query': _res['query']}
        for k, v in _res.items():
            if k == "associated_with":
                k = "related_to"
            tmp_v = []
            if isinstance(v, list):
                for item in v:
                    if item["@type"] in output_types or (item["@type"] == 'DiseaseOrPhenotypicFeature' and output_types == ['Disease']):
                        item_copy = deepcopy(item)
                        for m in item.keys():
                            if m in ['pr', 'go', 'mop', 'hgnc', 'uberon', 'so', 'cl', 'doid', 'chebi']:
                                item_copy[m.upper()] = item_copy.pop(m)
                        tmp_v.append(item_copy)
            if tmp_v != []:
                tmp_res[k] = tmp_v
        new_res.append(tmp_res)
    return new_res