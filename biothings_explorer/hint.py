import asyncio
from aiohttp import ClientSession

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
                     "name": "mondo.label"
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
                          'taxid': 'taxonomy',
                          'umls.cui': 'umls'},
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
                             'mondo.label': 'name'}
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

    async def call_api(self, _input, session):
        async with session.post(_input['url'], data=_input['data']) as res:
            return await res.json()

    async def run(self, _input):
        inputs = []
        inputs.append({'url': 'http://mygene.info/v3/query',
                       'data': {'q': ["'" + _input + "'"],
                                'scopes': ','.join(scopes['mygene.info']),
                                'size': 5,
                                'dotfield': True}})
        inputs.append({'url': 'http://myvariant.info/v1/query',
                       'data': {'q': ["'" + _input + "'"],
                                'scopes': ','.join(scopes['myvariant.info']),
                                'fields': ','.join(fields['myvariant.info'].keys()),
                                'size': 5,
                                'dotfield': True}})
        inputs.append({'url': 'http://mychem.info/v1/query',
                       'data': {'q': ["'" + _input + "'"],
                                'scopes': ','.join(scopes['mychem.info']),
                                'fields': ','.join(fields['mychem.info'].keys()),
                                'size': 5,
                                'dotfield': True}})
        inputs.append({'url': 'http://mydisease.info/v1/query',
                       'data': {'q': ["'" + _input + "'"],
                                'scopes': ','.join(scopes['mydisease.info']),
                                'fields': ','.join(fields['mydisease.info']),
                                'size': 5,
                                'dotfield': True}
                    })
        tasks = []
        async with ClientSession() as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_api(i, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            final_res = {}
            for j in self.types:
                final_res[j] = []
            for (k, v, j) in zip(self.clients, responses, self.types):
                for _v in v:
                    if 'notfound' in _v:
                        continue
                    else:
                        _res = {}
                        display = ''
                        for field_name in fields[k]:
                            if field_name in _v:
                                _res[fields[k][field_name]] = _v[field_name]
                                display += fields[k][field_name] + '(' + str(_v[field_name]) + ')' + ' '
                        _res['display'] = display
                        final_res[j].append(_res)
            return final_res

    def query(self, _input):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(_input))
        return loop.run_until_complete(future)
