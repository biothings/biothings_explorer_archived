import asyncio
from aiohttp import ClientSession, ClientTimeout


metadata = {
  "mygene.info": {
    "scopes": ['entrezgene', 'symbol', 'name', 'hgnc', 'umls.cui'],
    "id_ranks": ['entrez', 'symbol', 'umls', 'name'],
    "type": "Gene",
    "method": "post",
    "url": "http://mygene.info/v3/query",
    "fields": {
      'entrezgene': 'entrez',
      'name': 'name',
      'symbol': 'symbol',
      'taxid': 'taxonomy',
      'umls.cui': 'umls'
    }
  },
  "myvariant.info": {
    "scopes": ['dbsnp.rsid', '_id', 'clinvar.rsid',
               'dbnsfp.rsid', 'clinvar.hgvs.coding',
               'clinvar.hgvs.genomic', 'clinvar.hgvs.protein'],
    "id_ranks": ['dbsnp', 'hgvs'],
    "type": "SequenceVariant",
    "url": 'http://myvariant.info/v1/query',
    "method": "post",
    "fields": {
      '_id': "hgvs",
      'dbsnp.rsid': 'dbsnp'
    },
  },
  "mychem.info": {
    "scopes": ['chembl.molecule_chembl_id', 'drugbank.id',
               'pubchem.cid', 'chembl.pref_name', 'drugbank.name',
               'unii.unii', 'ginas.preferred_name'],
    "id_ranks": ['chembl', 'drugbank', 'pubchem', 'name'],
    "type": "ChemicalSubstance",
    "url": "http://mychem.info/v1/query",
    "method": "post",
    "fields": {
      'chembl.molecule_chembl_id': 'chembl',
      'drugbank.id': 'drugbank',
      'chembl.pref_name': 'name',
      'pubchem.cid': 'pubchem'
    }
  },
  "mydisease.info": {
    "scopes": ['_id', 'mondo.xrefs.doid', 'mondo.xrefs.hp',
               'mondo.xrefs.mesh', 'mondo.xrefs.umls',
               'mondo.label', 'disgenet.xrefs.disease_name'],
    "id_ranks": ['mondo', 'doid', 'umls', 'mesh', 'name'],
    "type": "DiseaseOrPhenotypicFeature",
    "url": "http://mydisease.info/v1/query",
    "method": "post",
    "fields": {
      '_id': "mondo",
      'mondo.xrefs.doid': 'doid',
      'mondo.xrefs.hp': 'hp',
      'mondo.xrefs.umls': 'umls',
      'mondo.xrefs.mesh': 'mesh',
      'mondo.label': 'name',
      'disgenet.xrefs.disease_name': 'name'
    }
  },
  "pathway": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['reactome', 'wikipathways', 'kegg', 'pharmgkb', 'biocarta', 'name'],
    "type": "Pathway",
    "method": "get",
    "url": "http://pending.biothings.io/geneset/query",
    "add": " AND type:pathway",
    "fields": {
      'name': 'name',
      'reactome': 'reactome',
      'wikipathways': 'wikipathways',
      'kegg': 'kegg',
      'pharmgkb': 'pharmgkb',
      'biocarta': 'biocarta'
    }
  },
  "mf": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['go', 'name'],
    "type": "MolecularFunction",
    "add": " AND type:mf",
    "method": "get",
    "url": "http://pending.biothings.io/geneset/query",
    "fields":{
      'name': 'name',
      'go': 'go'
    }
  },
  "cc": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['go', 'umls', 'name'],
    "type": "CellularComponent",
    "method": "get",
    "add": " AND type:cc",
    "url": "http://pending.biothings.io/geneset/query",
    "fields":{
      'name': 'name',
      'go': 'go',
      'umls': 'umls'
    }
  },
  "bp": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['go', 'umls', 'name'],
    "type": "BiologicalProcess",
    "add": " AND type:bp",
    "method": "get",
    "url": "http://pending.biothings.io/geneset/query",
    "fields": {
      'name': 'name',
      'go': 'go',
      'umls': 'umls'
    }
  },
  "anatomy": {
    "scopes": ['umls', 'name'],
    "id_ranks": ['umls', 'name'],
    "type": "Anatomy",
    "url": "http://pending.biothings.io/semmed_anatomy/query",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    }
  },
  "phenotype": {
    "scopes": ['umls', 'name'],
    "id_ranks": ['umls', 'name'],
    "type": "PhenotypicFeature",
    "url": "http://pending.biothings.io/semmedphenotype/query",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    }
  },
  "umlschem": {
    "scopes": ['umls', 'name'],
    "id_ranks": ['umls', 'name'],
    "type": "ChemicalSubstance",
    "url": "http://pending.biothings.io/umlschem/query",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    }
  }
}


class Hint():
    def __init__(self):
        self.clients = []
        self.types = []
        self.post_apis = []
        self.get_apis = []
        self.id_ranks = []

    def get_primary_id(self, client, json_doc, _type):
        ranks = metadata[client]['id_ranks']
        res = {}
        for _id in ranks:
            if _id in json_doc:
                res['identifier'] = _id
                res['cls'] = _type
                res['value'] = json_doc[_id]
                break
        return res

    async def call_api(self, _input, session):
        if _input['api'] in self.post_apis:
            async with session.post(_input['url'], data=_input['data']) as res:
                return await res.json()
        else:
            async with session.get(_input['url'], params=_input['data']) as res:
                return await res.json()

    async def run(self, _input):
        inputs = []
        for k, v in metadata.items():
            self.clients.append(k)
            self.types.append(v['type'])
            if v['method'] == 'get':
                self.get_apis.append(k)
            elif v['method'] == 'post':
                self.post_apis.append(k)
            _item = {'url': v['url'],
                     'api': k,
                     'data': {'q': ["'" + _input + "'"],
                              'scopes': ','.join(v['scopes']),
                              'fields': ','.join(v['fields']),
                              'size': 5,
                              'dotfield': 1
                             }
                     }
            if 'add' in v:
                _item['data']['q'] = "_id:" + _input + " OR name:" + _input + v["add"]
            inputs.append(_item)
        tasks = []
        timeout = ClientTimeout(total=20)
        async with ClientSession(timeout=timeout) as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_api(i, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            final_res = {}
            for j in self.types:
                final_res[j] = []
            for (k, v, j) in zip(self.clients, responses, self.types):
                # response could be from GET or POST, need to restructure
                if 'hits' in v:
                    v = v['hits']
                for _v in v:
                    if 'notfound' in _v:
                        continue
                    else:
                        _res = {}
                        display = ''
                        for field_name in metadata[k]['fields']:
                            if field_name in _v:
                                if metadata[k]['fields'][field_name] not in _res:
                                    _res[metadata[k]['fields'][field_name]] = _v[field_name]
                                    display += metadata[k]['fields'][field_name] + '(' + str(_v[field_name]) + ')' + ' '
                        _res['display'] = display
                        _res['type'] = j
                        primary = self.get_primary_id(k, _res, j)
                        _res.update({'primary': primary})
                        final_res[j].append(_res)
            return final_res

    def query(self, _input):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(_input))
        return loop.run_until_complete(future)
