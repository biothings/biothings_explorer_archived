from copy import deepcopy


def restructure_semmed_response(json_doc, output_types):
    """Restructure the JSON output from semmed API.

    :param: json_doc: the API response from semmed API
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
        else:
            tmp_res = {'query': _res['query']}
            for k, v in _res.items():
                tmp_v = []
                if isinstance(v, list):
                    for item in v:
                        if item["@type"] in output_types or (item["@type"] == 'DiseaseOrPhenotypicFeature' and output_types == ['Disease']):
                            item_copy = deepcopy(item)
                            item_copy['UMLS'] = item_copy.pop('umls')
                            item_copy['pubmed'] = item_copy.pop('pmid')
                            tmp_v.append(item_copy)
                if tmp_v != []:
                    tmp_res[k] = tmp_v
        new_res.append(tmp_res)
    return new_res
