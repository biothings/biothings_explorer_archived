def restructure_ctd_response(json_doc):
    """restructure the JSON output from CTD API

    parameters
        * json_doc: the API response from CTD API
    """
    # convert from list to dict
    if isinstance(json_doc, list):
        json_doc = {'data': json_doc}
    for _doc in json_doc['data']:
        if "PubMedIds" in _doc:
            _doc["PubMedIds"] = _doc["PubMedIds"].split("|")
        if "DiseaseID" in _doc:
            _doc["DiseaseID"] = _doc["DiseaseID"].split(':')[-1]
    return json_doc
