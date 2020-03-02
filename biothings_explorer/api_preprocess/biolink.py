def restructure_biolink_response(json_doc):
    """ restructure API response from biolink API before extracting data

    parameters
        * json_doc: the API response from biolink API

    notes: list of prefixes used in biolink API for different semantic types

        * ANATOMY: UBERON, CL, FBbt
        * DISEASE: MONDO
        * GENE: HGNC, NCBIGene, MGI， ZFIN，FlyBase
        * PHENOTYPE: EFO, HP, MONDO
    """
    if json_doc and 'associations' in json_doc:
        for _doc in json_doc['associations']:
            # remove prefix
            if 'object' in _doc and 'id' in _doc['object']:
                object_id = _doc['object']['id']
                try:
                    prefix, value = object_id.split(':')
                    # these IDs have prefix by nature
                    if prefix in ['HGNC', 'NCBIGene', 'REACT']:
                        _doc['object'][prefix] = value
                    else:
                        _doc['object'][prefix] = object_id
                except:
                    pass
            # remove empty value
            if not _doc['publications']:
                _doc.pop('publications')
            else:
                for _item in _doc['publications']:
                    _item['id'] = _item['id'].split(':')[-1]
            if not _doc['provided_by']:
                _doc.pop('provided_by')
            else:
                for i, _item in enumerate(_doc['provided_by']):
                    _doc['provided_by'][i] = _item.split(".")[-2].split("/")[-1]
    return json_doc