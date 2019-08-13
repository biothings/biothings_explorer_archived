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
                                             'scopes': 'entrezgene,symbol,name,hgnc',
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://myvariant.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': 'dbsnp.rsid, _id, clinvar.rsid, dbnsfp.rsid, clinvar.hgvs.coding, clinvar.hgvs.genomic,clinvar.hgvs.non-coding,clinvar.hgvs.protein,civic.hgvs_expression',
                                             'fields': 'dbsnp.rsid, _id',
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://mychem.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': 'chembl.molecule_chembl_id,drugbank.id,pubchem.cid,unii.unii, chembl.pref_name,drugbank.name,ginas.preferred_name',
                                             'fields': 'chembl.molecule_chembl_id, drugbank.id,chembl.pref_name,pubchem.cid,unii.unii',
                                             'size': 4,
                                             'dotfield': True}))
        requests.append(grequests.post('http://mydisease.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': '_id, mondo.xrefs.doid, mondo.xrefs.hp, mondo.xrefs.mesh, mondo.xrefs.umls,mondo.label',
                                             'fields': '_id,mondo.xrefs.doid,mondo.xrefs.hp, mondo.xrefs.mesh,mondo.xrefs.umls,mondo.label',
                                             'size': 4,
                                             'dotfield': True}))
        t1 = time.time()
        res = grequests.map(requests)
        t2 = time.time()
        print('time to make request {}'.format(t2 - t1))
        res = {k: v.json() for (k, v) in zip(self.types, res)}
        t3 = time.time()
        print('time to parse results {}'.format(t3 - t2))
        return res
