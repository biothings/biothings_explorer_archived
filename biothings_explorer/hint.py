import grequests


class Hint():
    def __init__(self):
        self.clients = ['gene', 'variant', 'chem', 'disease']

    def query(self, _input):
        """query input using 4 APIs"""
        requests = []
        requests.append(grequests.post('http://mygene.info/v3/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': 'entrezgene,symbol,name,hgnc'}))
        requests.append(grequests.post('http://myvariant.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': 'dbsnp.rsid, _id, clinvar.rsid, dbnsfp.rsid, clinvar.hgvs.coding, clinvar.hgvs.genomic,clinvar.hgvs.non-coding,clinvar.hgvs.protein,civic.hgvs_expression',
                                             'fields': 'dbsnp.rsid, _id'}))
        requests.append(grequests.post('http://mychem.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': 'chembl.molecule_chembl_id,drugbank.id,pubchem.cid,unii.unii, chembl.pref_name,drugbank.name,ginas.preferred_name',
                                             'fields': 'chembl.molecule_chembl_id, drugbank.id,chembl.pref_name,pubchem.cid,unii.unii'}))
        requests.append(grequests.post('http://mydisease.info/v1/query',
                                       data={'q': ["'" + _input + "'"],
                                             'scopes': '_id, mondo.xrefs.doid, mondo.xrefs.hp, mondo.xrefs.mesh, mondo.xrefs.umls,mondo.label',
                                             'fields': '_id,mondo.xrefs.doid,mondo.xrefs.hp, mondo.xrefs.mesh,mondo.xrefs.umls,mondo.label'}))
        res = grequests.map(requests)
        return {k: v.json() for (k, v) in zip(self.clients, res)}
