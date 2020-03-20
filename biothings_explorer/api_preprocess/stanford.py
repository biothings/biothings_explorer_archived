def restructure_stanford_response(json_doc):
    """Restructure the JSON output from stanford KP.

    :param: json_doc: the API response from stanford KP
    """
    # convert from list to dict
    if isinstance(json_doc, list):
        json_doc = {'data': json_doc}
    if 'data' in json_doc:
        for _doc in json_doc['data']:
            # store restructured attributes info
            new_attr = {}
            for _attr in _doc['attributes']:
                if 'attributeValueTermUri' not in _attr:
                    new_attr[_attr['attributeName'].replace(' ', '_')] = _attr['attributeValue']
                else:
                    new_attr[_attr['attributeName'].replace(' ', '_')] = {'name': _attr['attributeValue']}
                    if 'PATO_' in _attr['attributeValueTermUri']:
                        new_attr[_attr['attributeName'].replace(' ', '_')]['pato'] = 'PATO:' + _attr['attributeValueTermUri'].split('_')[-1]
                    elif 'MONDO_' in _attr['attributeValueTermUri']:
                        new_attr[_attr['attributeName'].replace(' ', '_')]['mondo'] = 'MONDO:' + _attr['attributeValueTermUri'].split('_')[-1]
                    elif 'BTO_' in _attr['attributeValueTermUri']:
                        new_attr[_attr['attributeName'].replace(' ', '_')]['bto'] = 'BTO:' + _attr['attributeValueTermUri'].split('_')[-1]
                    elif 'CLO_' in _attr['attributeValueTermUri']:
                        new_attr[_attr['attributeName'].replace(' ', '_')]['clo'] = 'CLO:' + _attr['attributeValueTermUri'].split('_')[-1]
            _doc['attributes'] = new_attr
        return json_doc
    return {}
