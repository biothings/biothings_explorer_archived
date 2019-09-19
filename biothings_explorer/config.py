metadata = {
  "mygene.info": {
    "scopes": ['entrezgene', 'symbol', 'name', 'hgnc', 'umls.cui'],
    "id_ranks": ['entrez', 'symbol', 'umls', 'name'],
    "doc_type": "Gene",
    "api_type": "biothings",
    "method": "post",
    "url": "http://mygene.info/v3/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mygene.info/schema.json',
    "hint": True,
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
    "doc_type": "SequenceVariant",
    "hint": True,
    "api_type": "biothings",
    "url": 'http://myvariant.info/v1/query',
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/myvariant.info/schema.json',
    "method": "post",
    "fields": {
      '_id': "hgvs",
      'dbsnp.rsid': 'dbsnp'
    },
  },
  "mychem.info": {
    "scopes": ['chembl.molecule_chembl_id', 'drugbank.id',
               'pubchem.cid', 'chembl.pref_name', 'drugbank.name',
               'unii.unii', 'ginas.preferred_name', 'drugcentral.xrefs.umlscui', "drugcentral.synonyms", "ginas.name_list", "drugcentral.xrefs.chebi"],
    "id_ranks": ['chembl', 'drugbank', 'pubchem', 'name'],
    "doc_type": "ChemicalSubstance",
    "api_type": "biothings",
    "hint": True,
    "url": "http://mychem.info/v1/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mychem.info/schema.json',
    "method": "post",
    "fields": {
      'chembl.molecule_chembl_id': 'chembl',
      'drugbank.id': 'drugbank',
      'chembl.pref_name': 'name',
      'pubchem.cid': 'pubchem',
      'drugcentral.xrefs.umlscui': 'umls'
    }
  },
  "mydisease.info": {
    "scopes": ['_id', 'mondo.xrefs.doid', 'mondo.xrefs.hp',
               'mondo.xrefs.mesh', 'mondo.xrefs.umls',
               'mondo.label', 'disgenet.xrefs.disease_name'],
    "id_ranks": ['mondo', 'doid', 'umls', 'mesh', 'name'],
    "doc_type": "DiseaseOrPhenotypicFeature",
    "api_type": "biothings",
    "hint": True,
    "url": "http://mydisease.info/v1/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mydisease.info/schema.json',
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
  "semmeddisease": {
    "url": "http://pending.biothings.io/semmed/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmed/schema.json',
    'api_type': "biothings"
  },
  "semmedanatomy": {
    "url": "https://pending.biothings.io/semmed_anatomy/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedanatomy/schema.json',
    'api_type': "biothings"
  },
  "semmedbp": {
    "url": "https://pending.biothings.io/semmedbp/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedbp/schema.json",
    'api_type': "biothings"
  },
  "semmedchemical": {
    "url": "https://pending.biothings.io/semmedchemical/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedchemical/schema.json",
    'api_type': "biothings"
  },
  "semmedgene": {
    "url": "https://pending.biothings.io/semmedgene/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedgene/schema.json',
    'api_type': "biothings"
  },
  "semmedphenotype": {
    "url": "https://pending.biothings.io/semmedphenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json",
    'api_type': "biothings"
  },
  "pathway": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['reactome', 'wikipathways', 'kegg', 'pharmgkb', 'biocarta', 'name'],
    "doc_type": "Pathway",
    "api_type": "biothings",
    "method": "get",
    "url": "http://pending.biothings.io/geneset/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/geneset/pathway_schema.json",
    "add": " AND type:pathway",
    "hint": True,
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
    "doc_type": "MolecularActivity",
    "api_type": "biothings",
    "add": " AND type:mf",
    "method": "get",
    "hint": True,
    "url": "http://pending.biothings.io/geneset/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/geneset/mf_schema.json",
    "fields":{
      'name': 'name',
      'go': 'go'
    }
  },
  "cc": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['go', 'umls', 'name'],
    "doc_type": "CellularComponent",
    "api_type": "biothings",
    "method": "get",
    "add": " AND type:cc",
    "hint": True,
    "url": "http://pending.biothings.io/geneset/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/geneset/cc_schema.json",
    "fields":{
      'name': 'name',
      'go': 'go',
      'umls': 'umls'
    }
  },
  "bp": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['go', 'umls', 'name'],
    "doc_type": "BiologicalProcess",
    "api_type": "biothings",
    "add": " AND type:bp",
    "method": "get",
    "hint": True,
    "url": "http://pending.biothings.io/geneset/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/geneset/bp_schema.json",
    "fields": {
      'name': 'name',
      'go': 'go',
      'umls': 'umls'
    }
  },
  "anatomy": {
    "scopes": ['umls', 'name'],
    "id_ranks": ['umls', 'name'],
    "doc_type": "Anatomy",
    "api_type": "biothings",
    "hint": True,
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
    "doc_type": "PhenotypicFeature",
    "api_type": "biothings",
    "hint": True,
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
    "doc_type": "ChemicalSubstance",
    "api_type": "biothings",
    "hint": True,
    "url": "http://pending.biothings.io/umlschem/query",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    }
  },
  "biolink_anatomy2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/anatomy/{anatomy_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_anatomy2gene.json",
    "method": "get",
    "path": "anatomy_id",
    'api_type': "biolink"
  },
  "biolink_disease2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2gene.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink"
  },
  "biolink_disease2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2pathway.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink"
  },
  "biolink_disease2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2phenotype.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink"
  },
  "biolink_gene2anatomy": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/anatomy?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2anatomy.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink"
  },
  "biolink_gene2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2disease.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink"
  },
  "biolink_geneinteraction": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/interactions?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_geneinteraction.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink"
  },
  "biolink_gene2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2phenotype.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink"
  },
  "biolink_pathway2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2disease.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink"
  },
  "biolink_pathway2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2phenotype.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink"
  },
  "biolink_phenotype2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2disease.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink"
  },
  "biolink_phenotype2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2gene.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink"
  },
  "biolink_phenotype2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2pathway.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink"
  },
  "dgidb_gene2chemical": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?genes={gene_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_gene2chemical.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "other"
  },
  "dgidb_chemical2gene": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?drugs={chembl_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_chemical2gene.json",
    "method": "get",
    "path": "chembl_id",
    'api_type': "other"
  },
}
