class APIPreprocess():

    def __init__(self, json_doc, api_type, api_name=None):
        self.api_type = api_type
        self.api_name = api_name
        self.json_doc = json_doc
        print('input json doc', self.json_doc)

    def restructure(self):
        if self.api_type == 'biolink':
            return self.restructure_biolink_response(self.json_doc)
        else:
            return self.json_doc

    def restructure_gwascatalog(self, json_doc):
        """restructure gwascatalog"""
        if json_doc:
            associations = json_doc.get('gwascatalog').get("associations")
            if type(associations) == dict:
                associations = [associations]
            for _assoc in associations:
                efo = _assoc.get("efo")
                if efo:
                    efo_id = efo.get("id")
                    if efo_id:
                        efo_id = efo_id.split(':')[-1]
            return json_doc

    def restructure_biolink_response(self, json_doc):
        """
        ANATOMY: UBERON, CL, FBbt
        DISEASE: MONDO
        GENE: HGNC, NCBIGene, MGI， ZFIN，FlyBase
        PHENOTYPE: EFO, HP, MONDO
        """
        if json_doc and 'associations' in json_doc:
            for _doc in json_doc['associations']:
                # remove prefix
                if 'object' in _doc and 'id' in _doc['object']:
                    object_id = _doc['object']['id']
                    try:
                        prefix, value = object_id.split(':')
                        # these IDs have prefix by nature
                        if prefix in ['HGNC', 'NCBIGene']:
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
        print('output json doc', json_doc)
        return json_doc