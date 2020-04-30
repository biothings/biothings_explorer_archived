from pathlib import Path
CURRENT_PATH = Path(__file__)
# these are keys internally used by BTE in the API response mapping file.
INTERNAL_KEYS = ["@context", "@type", "$input", "$source"]

PREFIX_TO_REMOVE = 'bts'

BIOTHINGS_SCHEMA_URL = 'https://raw.githubusercontent.com/data2health/schemas/biothings/biothings/biothings_curie_kevin.jsonld'

id_ranks = {
  'Gene': ['entrez', 'ensembl', 'symbol', 'umls'],
  'SequenceVariant': ['dbsnp', 'hgvs'],
  'ChemicalSubstance': ['chembl', 'drugbank', 'pubchem', 'chebi', 'mesh', 'smiles', 'name', 'umls'],
  'pathway': ['reactome', 'wikipathways', 'kegg', 'pharmgkb', 'biocarta', 'name'],
  'DiseaseOrPhenotypicFeature': ['mondo', 'doid', 'umls', 'mesh', 'hp', 'name'],
  'PhenotypicFeature': ['hp', 'umls'],
  'mf': ['go'],
  'cc': ['go', 'umls'],
  'bp': ['go', 'umls'],
  'anatomy': ['umls'],
  'phenotype': ['umls']
}

metadata = {
  "mygene.info": {
    "scopes": ['entrezgene', 'symbol', 'name', 'HGNC', 'umls.cui', 'uniprot.Swiss-Prot', "ensembl.gene"],
    "id_ranks": ['entrez', 'symbol', 'hgnc', 'umls', 'uniprot', 'ensembl', 'name'],
    "doc_type": "Gene",
    "api_type": "biothings",
    "method": "post",
    "url": "http://mygene.info/v3/query",
    "mapping_url": Path.joinpath(CURRENT_PATH, 'smartapi/schema/mygene.info.json'),
    "hint": True,
    "fields": {
      'entrezgene': 'entrez',
      'name': 'name',
      'symbol': 'symbol',
      'taxid': 'taxonomy',
      'umls.cui': 'umls',
      'uniprot.Swiss-Prot': 'uniprot',
      'HGNC': 'hgnc',
      "ensembl.gene": 'ensembl'
    },
    'api_name': "MyGene.info API",
    'smart_api_id': "59dce17363dce279d389100834e43648"
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
    "mapping_url": Path.joinpath(CURRENT_PATH, 'smartapi/schema/myvariant.info.json'),
    "method": "post",
    "fields": {
      '_id': "hgvs",
      'dbsnp.rsid': 'dbsnp'
    },
    'api_name': "MyVariant.info API",
    'smart_api_id': "09c8782d9f4027712e65b95424adba79"
  },
  "mychem.info": {
    "scopes": ['chembl.molecule_chembl_id', 'drugbank.id', 'chebi.id', 'chebi.xrefs.chembl', 'chembl.smiles', 'pubchem.smiles.canonical', 
               'chebi.smiles','drugcentral.structures.smiles', 'pubchem.cid', 'chembl.pref_name', 'drugbank.name', 
               'unii.unii', 'ginas.preferred_name', 'drugcentral.xrefs.umlscui', "drugcentral.synonyms", 
               "ginas.name_list", "drugcentral.xrefs.chebi", "drugcentral.xrefs.mesh_descriptor_ui"],
    "id_ranks": ['chembl', 'drugbank', 'pubchem', 'mesh', 'chebi', 'name'],
    "doc_type": "ChemicalSubstance",
    "api_type": "biothings",
    "hint": True,
    "url": "http://mychem.info/v1/query",
    "mapping_url": Path.joinpath(CURRENT_PATH, 'smartapi/schema/mychem.info.json'),
    "method": "post",
    "fields": {
      'chembl.molecule_chembl_id': 'chembl',
      'chebi.xrefs.chembl': 'chembl',
      'drugbank.id': 'drugbank',
      'drugbank.name': 'name',
      'chembl.pref_name': 'name',
      'pubchem.cid': 'pubchem',
      'drugcentral.xrefs.umlscui': 'umls',
      'drugcentral.xrefs.mesh_descriptor_ui': 'mesh',
      'chebi.id': 'chebi',
      'chebi.xrefs.pubchem.cid': 'pubchem',
      'drugcentral.xrefs.chebi': 'chebi',
      'chembl.smiles': 'smiles',
      'pubchem.smiles.canonical': 'smiles',
      'chebi.smiles': 'smiles',
      'drugcentral.structures.smiles': 'smiles'
    },
    'api_name': "MyChem.info API",
    "smart_api_id": "8f08d1446e0bb9c2b323713ce83e2bd3"
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
    },
    'api_name': "MyDisease.info API",
    "smart_api_id": "f307760715d91908d0ae6de7f0810b22"
  },
  "semmeddisease": {
    "url": "http://biothings.ncats.io/semmed/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmed/schema.json',
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'DiseaseOrPhenotypicFeature',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "semmedanatomy": {
    "url": "https://biothings.ncats.io/semmed_anatomy/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedanatomy/schema.json',
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'AnatomicalEntity',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "semmedbp": {
    "url": "https://biothings.ncats.io/semmedbp/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedbp/schema.json",
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'BiologicalProcess',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "semmedchemical": {
    "url": "https://biothings.ncats.io/semmedchemical/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedchemical/schema.json",
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'ChemicalSubstance',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "semmedgene": {
    "url": "https://biothings.ncats.io/semmedgene/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedgene/schema.json',
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'Gene',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "semmedphenotype": {
    "url": "https://biothings.ncats.io/semmedphenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'SEMMED API',
    'doc_type': 'PhenotypicFeature',
    "smart_api_id": "e99229fc6ccb9ad9889bcc9c77a36bad"
  },
  "cordgene": {
    "url": "https://biothings.ncats.io/cord_gene/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'Gene',
    "smart_api_id": "6bc54230a6fa7693b2cd113430387ca7"
  },
  "cordprotein": {
    "url": "https://biothings.ncats.io/cord_protein/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'Protein',
    "smart_api_id": "1066244f2976e931654394581255630e"
  },
  "cordchemical": {
    "url": "https://biothings.ncats.io/cord_chemical/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'ChemicalSubstance',
    "smart_api_id": "503e8c42d041aa5b8b1ffafaf612c298"
  },
  "cordcell": {
    "url": "https://biothings.ncats.io/cord_cell/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'Cell',
    "smart_api_id": "3d6bacf6e305bee5efdd25d1560996e1"
  },
  "corddisease": {
    "url": "https://biothings.ncats.io/cord_disease/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'DiseaseOrPhenotypicFeature',
    "smart_api_id": "871d5b6761d91a7805572c47f016fe47"
  },
  "cordma": {
    "url": "https://biothings.ncats.io/cord_ma/query",
    'api_type': "biothings",
    'api_name': 'CORD API ',
    'doc_type': 'MolecularActivity',
    "smart_api_id": "066a2ef51223a5a95216355facaac9d0"
  },
  "cordbp": {
    "url": "https://biothings.ncats.io/cord_bp/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'BiologicalProcess',
    "smart_api_id": "7cbc3ff9b2d09cb8075715bde740ce4f"
  },
  "cordgenomicentity": {
    "url": "https://biothings.ncats.io/cord_genomic_entity/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'GenomicEntity',
    "smart_api_id": "bffe279a1387ef956a423e2e8a133cf6"
  },
  "cordanatomy": {
    "url": "https://biothings.ncats.io/cord_anatomy/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'AnatomicalEntity',
    "smart_api_id": "52f5867b9cc9cf8664565cc9ef2af276"
  },
  "cordcc": {
    "url": "https://biothings.ncats.io/cord_cc/query",
    'api_type': "biothings",
    'api_name': 'CORD API',
    'doc_type': 'CellularComponent',
    "smart_api_id": "bf5aac143254714988018d87dc447a5c"
  },
  "mgigene2phenotype": {
    "url": "https://biothings.ncats.io/mgigene2phenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mgigene2phenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'MGIgene2phenotype API',
    "smart_api_id": "77ed27f111262d0289ed4f4071faa619"
  },
  "ebigene2phenotype": {
    "url": "https://biothings.ncats.io/ebigene2phenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ebigene2phenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'EBIgene2phenotype API',
    "smart_api_id": "1f47552dabd67351d4c625adb0a10d00"
  },
  "DISEASES": {
    "url": "https://biothings.ncats.io/DISEASES/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/DISEASES/schema.json",
    'api_type': "biothings",
    'api_name': 'DISEASES API',
    'smart_api_id': "a7f784626a426d054885a5f33f17d3f8"
  },
  "pfocr": {
    "url": "https://biothings.ncats.io/pfocr/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/pfocr/schema.json",
    'api_type': "biothings",
    'api_name': 'pfocr API',
    "smart_api_id": "edeb26858bd27d0322af93e7a9e08761"
  },
  "pathway": {
    "scopes": ['_id', 'name'],
    "id_ranks": ['reactome', 'wikipathways', 'kegg', 'pharmgkb', 'biocarta', 'name'],
    "doc_type": "Pathway",
    "api_type": "biothings",
    "method": "get",
    "url": "http://biothings.ncats.io/geneset/query",
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
    "url": "http://biothings.ncats.io/geneset/query",
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
    "url": "http://biothings.ncats.io/geneset/query",
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
    "url": "http://biothings.ncats.io/geneset/query",
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
    "url": "http://biothings.ncats.io/semmed_anatomy/query",
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
    "url": "http://biothings.ncats.io/semmedphenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    },
    "hint": True
  },
  "umlschem": {
    "scopes": ['umls', 'name'],
    "id_ranks": ['umls', 'name'],
    "doc_type": "ChemicalSubstance",
    "api_type": "biothings",
    "hint": True,
    "url": "http://biothings.ncats.io/umlschem/query",
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
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_disease2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2gene.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },

  "biolink_disease2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2pathway.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_disease2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2phenotype.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_gene2anatomy": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/anatomy?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2anatomy.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_gene2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2disease.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_geneinteraction": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/interactions?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_geneinteraction.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_gene2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2phenotype.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_pathway2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2disease.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_pathway2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2phenotype.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_phenotype2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2disease.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_phenotype2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2gene.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "biolink_phenotype2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2pathway.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': "BioLink API",
    "smart_api_id": "d22b657426375a5295e7da8a303b9893"
  },
  "dgidb_gene2chemical": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?genes={gene_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_gene2chemical.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "other",
    'api_name': "DGIdb API",
    "smart_api_id": "e3edd325c76f2992a111b43a907a4870"
  },
  "dgidb_chemical2gene": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?drugs={chembl_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_chemical2gene.json",
    "method": "get",
    "path": "chembl_id",
    'api_type': "other",
    'api_name': "DGIdb API",
    "smart_api_id": "e3edd325c76f2992a111b43a907a4870"
  },
  "quickgo_children": {
    "url": "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{goterm}/children",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/quickgo/schema/children.json",
    "method": "get",
    "path": "goterm",
    'api_type': "other",
    'api_name': 'QuickGO API',
    "smart_api_id": "1f277e1563fcfd124bfae2cc3c4bcdec"
  },
  "litvar": {
    "url": "https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/entity/litvar/{dbsnp}##",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/litvar/schema/schema.json",
    "method": "get",
    "path": "dbsnp",
    'api_type': "other",
    'api_name': 'LitVar API',
    "smart_api_id": "dca415f2d792976af9d642b7e73f7a41"
  },
  "ols_children": {
    "url": "https://www.ebi.ac.uk/ols/api/ontologies/doid/children?id={doid}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ols/schema/schema.json",
    "method": "get",
    "path": "doid",
    'api_type': "other",
    'api_name': "Ontology Lookup Service API",
    "smart_api_id": "1c056ffc7ed0dd1229e71c4752239465"
  },
  "stanford_biosample_disease2sample": {
    "url": "http://api.kp.metadatacenter.org/biosample/search?q=biolink:Disease={mondo}&limit=1000",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/stanford/disease2sample.json",
    "method": "get",
    "path": "mondo",
    "api_type": "stanford",
    "api_name": "Stanford BioSample API",
    "smart_api_id": "553a49d112bb19306253942ebd6377a9"
  },
  "stanford_biosample_cl2sample": {
    "url": "http://api.kp.metadatacenter.org/biosample/search?q=biolink:CellLine={clo}&limit=1000",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/stanford/cl2sample.json",
    "method": "get",
    "path": "clo",
    "api_type": "stanford",
    "api_name": "Stanford BioSample API",
    "smart_api_id": "553a49d112bb19306253942ebd6377a9"
  },
  "chembl_drug_mechanism": {
    "url": "https://www.ebi.ac.uk/chembl/api/data/mechanism.json?molecule_chembl_id={chembl}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ChEMBL/drugmechanism.json",
    "method": "get",
    "path": "chembl",
    "api_type": "other",
    "api_name": "ChEMBL API",
    "smart_api_id": "71add13e7c8b26b0046cfb8cf5092395"
  },
  "ctd_chemical2gene": {
    "url": "http://ctdbase.org/tools/batchQuery.go?inputType=chem&inputTerms={mesh}|mercury&report=genes_curated&format=json",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/CTD_api/chemical2gene.json",
    "method": "get",
    "path": "mesh",
    "api_type": "ctd",
    "api_name": "CTD API",
    "smart_api_id": "0212611d1c670f9107baf00b77f0889a"
  },
  "ctd_gene2disease": {
    "url": "http://ctdbase.org/tools/batchQuery.go?inputType=gene&inputTerms={entrez}&report=diseases_curated&format=json",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/CTD_api/gene2disease.json",
    "method": "get",
    "path": "entrez",
    "api_type": "ctd",
    "api_name": "CTD API",
    "smart_api_id": "0212611d1c670f9107baf00b77f0889a"
  },
  "opentarget": {
    "url": "https://platform-api.opentargets.io/v3/platform/public/evidence/filter?target={ensembl}&datasource=chembl&size=15&fields=drug",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/opentarget/gene2chemical.json",
    "method": "get",
    "path": "ensembl",
    "api_type": "opentarget",
    "api_name": "OpenTarget API",
    "smart_api_id": "542ba165e1b4227854cf7c0a8addcc79"
  },
  "RGD": {
    "url": "https://rest.rgd.mcw.edu/rgdws/genes/{rgd}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/RGD/schema.json",
    "method": "get",
    "path": "rgd",
    "api_type": "other",
    "api_name": "RGD API",
    "smart_api_id": "eb28713e2e23160e80e88f3a5dabcca4"
  },
  "scibite_gene2chemical": {
    "url": "https://automat.renci.org/cord19_scibite_v2/gene/chemical_substance/NCBIGene:{entrez}",
    "path": "entrez",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_gene2chemical/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  },
  "scibite_chemical2gene": {
    "url": "https://automat.renci.org/cord19_scibite_v2/chemical_substance/gene/{chebi}",
    "path": "chebi",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_chemical2gene/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  },
  "scibite_chemical2disease": {
    "url": "https://automat.renci.org/cord19_scibite_v2/chemical_substance/disease/{chebi}",
    "path": "chebi",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_chemical2disease/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  },
  "scibite_gene2disease": {
    "url": "https://automat.renci.org/cord19_scibite_v2/gene/disease/NCBIGene:{entrez}",
    "path": "entrez",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_gene2disease/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  },
  "scibite_disease2gene": {
    "url": "https://automat.renci.org/cord19_scibite_v2/disease/gene/{mondo}",
    "path": "mondo",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_disease2gene/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  },
  "scibite_disease2chemical": {
    "url": "https://automat.renci.org/cord19_scibite_v2/disease/chemical_substance/{mondo}",
    "path": "mondo",
    "method": "get",
    "api_type": "automat",
    "api_name": "Automat CORD19 Scibite API",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/scibite_disease2chemical/schema.json",
    "smart_api_id": "5c5a0b5bc77e5d25d1a04e1385f9fad7"
  }
}


METADATA_OPTIOINAL = {
  "robokop_gene2chemical": {
    "url": "https://robokop.renci.org/api/simple/expand/gene/HGNC:{hgnc_id}/chemical_substance/",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/robokop/gene2chemical.json",
    "method": "get",
    "path": "hgnc_id",
    'api_type': "reasoner",
    'api_name': "robokop"
  },
  "robokop_gene2genefamily": {
    "url": "https://robokop.renci.org/api/simple/expand/gene/HGNC:{hgnc_id}/gene_family/",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/robokop/gene2genefamily.json",
    "method": "get",
    "path": "hgnc_id",
    'api_type': "reasoner",
    'api_name': "robokop"
  },
  "robokop_chemical2disease": {
    "url": "https://robokop.renci.org/api/simple/expand/chemical_substance/CHEMBL:{hgnc_id}/disease_or_phenotypic_feature/",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/robokop/chemical2disease.json",
    "method": "get",
    "path": "hgnc_id",
    'api_type': "reasoner",
    'api_name': "robokop"
  },
  "cohd_disease2chemical": {
    "url": "http://cohd.io/api/frequencies/associatedConceptDomainFreq?dataset_id=1&concept_id={cohd}&domain=Drug",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/cohd/schema/disease2chemical.json",
    "method": "get",
    "path": "cohd",
    'api_type': "other",
    'api_name': 'cohd'
  },
}