import grequests
import time

MYGENE_MAPPING = {"entrez": "entrezgene",
                  "name": "name",
                  "symbol": "symbol",
                  "taxonomy": "taxid"}

MYVARIANT_MAPPING = {"hgvs": "_id",
                     "dbsnp": "dbsnp.rsid"}

MYCHEM_MAPPING = {"chembl": "chembl.molecule_chembl_id",
                  "drugbank": "drugbank.id",
                  "name": "chembl.pref_name",
                  "pubchem": "pubchem.cid",
                  "unii": "unii.unii"
                  }

MYDISEASE_MAPPING = {"mondo": "_id",
                     "doid": "mondo.xrefs.doid",
                     "hp": "mondo.xrefs.hp",
                     "mesh": "mondo.xrefs.mesh",
                     "umls": "mondo.xrefs.umls",
                     "name": "xrefs.umls,mondo.label"
                     }
scopes = {'mygene.info': ['entrezgene', 'symbol', 'name', 'hgnc', 'umls.cui'],
          'myvariant.info': ['dbsnp.rsid', '_id', 'clinvar.rsid',
                             'dbnsfp.rsid', 'clinvar.hgvs.coding',
                             'clinvar.hgvs.genomic', 'clinvar.hgvs.protein'],
          'mychem.info': ['chembl.molecule_chembl_id', 'drugbank.id',
                          'pubchem.cid', 'chembl.pref_name', 'drugbank.name',
                          'unii.unii', 'ginas.preferred_name'],
          'mydisease.info': ['_id', 'mondo.xrefs.doid', 'mondo.xrefs.hp',
                             'mondo.xrefs.mesh', 'mondo.xrefs.umls',
                             'mondo.label']}

fields = {'mygene.info': {'entrezgene': 'entrez',
                          'name': 'name',
                          'symbol': 'symbol',
                          'taxid': 'taxonomy'},
          'myvariant.info': {'_id': "hgvs",
                             'dbsnp.rsid': 'dbsnp'},
          'mychem.info': {'chembl.molecule_chembl_id': 'chembl',
                          'drugbank.id': 'drugbank',
                          'chembl.pref_name': 'name',
                          'pubchem.cid': 'pubchem'},
          'mydisease.info': {'_id': "mondo",
                             'mondo.xrefs.doid': 'doid',
                             'mondo.xrefs.hp': 'hp',
                             'mondo.xrefs.umls': 'umls',
                             'mondo.xrefs.mesh': 'mesh',
                             'mondo.xrefs.label': 'name'}
          }


class Hint():
    def __init__(self):
        self.clients = ['mygene.info', 'myvariant.info',
                        'mychem.info', 'mydisease.info']
        self.types = ['gene', 'variant', 'chemical', 'disease']
        self.mapping = {'mygene.info': MYGENE_MAPPING,
                        'myvariant.info': MYVARIANT_MAPPING,
                        'mychem.info': MYCHEM_MAPPING,
                        'mydisease.info': MYDISEASE_MAPPING}

    def query(self, _input):
        """query input using 4 APIs"""
        requests = []
        requests.append(grequests.post('http://mygene.info/v3/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': ','.join(scopes['mygene.info']),
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://myvariant.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': ','.join(scopes['myvariant.info']),
                                             'fields': ','.join(fields['myvariant.info'].keys()),
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://mychem.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': ','.join(scopes['mychem.info']),
                                             'fields': ','.join(fields['mychem.info'].keys()),
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://mydisease.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': ','.join(scopes['mydisease.info']),
                                             'fields': ','.join(fields['mydisease.info']),
                                             'size': 4,
                                             'dotfield': True}))
        res = grequests.map(requests)
        final_res = []
        for (k, v, j) in zip(self.clients, res, self.types):
            _res = {}
            v = v.json()
            for _v in v:
                if 'notfound' in _v:
                    continue
                else:
                    display = ''
                    for field_name in fields[k]:
                        if field_name in _v:
                            _res[fields[k][field_name]] = _v[field_name]
                            display += fields[k][field_name] + '(' + str(_v[field_name]) + ')' + ' '
                    _res['display'] = display
                    _res['type'] = j
                    final_res.append(_res)
        return final_res
