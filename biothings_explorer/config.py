# these are keys internally used by BTE in the API response mapping file.
INTERNAL_KEYS = ["@context", "@type", "$input", "$source"]

id_ranks = {
  'Gene': ['entrez', 'ensembl', 'symbol', 'umls'],
  'SequenceVariant': ['dbsnp', 'hgvs'],
  'ChemicalSubstance': ['chembl', 'drugbank', 'pubchem', 'mesh', 'smiles', 'name', 'umls'],
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
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mygene.info/schema.json',
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
    'api_name': "mygene.info"
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
    'api_name': "myvariant.info"
  },
  "mychem.info": {
    "scopes": ['chembl.molecule_chembl_id', 'drugbank.id', 'chebi.id', 'chembl.smiles', 'pubchem.smiles.canonical', 
               'chebi.smiles','drugcentral.structures.smiles', 'pubchem.cid', 'chembl.pref_name', 'drugbank.name', 
               'unii.unii', 'ginas.preferred_name', 'drugcentral.xrefs.umlscui', "drugcentral.synonyms", 
               "ginas.name_list", "drugcentral.xrefs.chebi", "drugcentral.xrefs.mesh_descriptor_ui"],
    "id_ranks": ['chembl', 'drugbank', 'pubchem', 'mesh', 'chebi', 'name'],
    "doc_type": "ChemicalSubstance",
    "api_type": "biothings",
    "hint": True,
    "url": "http://mychem.info/v1/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mychem.info/schema.json',
    "method": "post",
    "fields": {
      'chembl.molecule_chembl_id': 'chembl',
      'drugbank.id': 'drugbank',
      'drugbank.name': 'name',
      'chembl.pref_name': 'name',
      'pubchem.cid': 'pubchem',
      'drugcentral.xrefs.umlscui': 'umls',
      'drugcentral.xrefs.mesh_descriptor_ui': 'mesh',
      'chebi.id': 'chebi',
      'drugcentral.xrefs.chebi': 'chebi',
      'chembl.smiles': 'smiles',
      'pubchem.smiles.canonical': 'smiles',
      'chebi.smiles': 'smiles',
      'drugcentral.structures.smiles': 'smiles'
    },
    'api_name': "mychem.info"
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
    'api_name': "mydisease.info"
  },
  "semmeddisease": {
    "url": "http://pending.biothings.io/semmed/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmed/schema.json',
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "semmedanatomy": {
    "url": "https://pending.biothings.io/semmed_anatomy/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedanatomy/schema.json',
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "semmedbp": {
    "url": "https://pending.biothings.io/semmedbp/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedbp/schema.json",
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "semmedchemical": {
    "url": "https://pending.biothings.io/semmedchemical/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedchemical/schema.json",
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "semmedgene": {
    "url": "https://pending.biothings.io/semmedgene/query",
    "mapping_url": 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedgene/schema.json',
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "semmedphenotype": {
    "url": "https://pending.biothings.io/semmedphenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'semmed'
  },
  "mgigene2phenotype": {
    "url": "https://pending.biothings.io/mgigene2phenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/mgigene2phenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'mgigene2phenotype'
  },
  "ebigene2phenotype": {
    "url": "https://pending.biothings.io/ebigene2phenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ebigene2phenotype/schema.json",
    'api_type': "biothings",
    'api_name': 'ebigene2phenotype'
  },
  "DISEASES": {
    "url": "https://pending.biothings.io/DISEASES/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/DISEASES/schema.json",
    'api_type': "biothings",
    'api_name': 'DISEASES'
  },
  "pfocr": {
    "url": "https://pending.biothings.io/pfocr/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/pfocr/schema.json",
    'api_type': "biothings",
    'api_name': 'pfocr'
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
    },
    'api_name': 'semmed'
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
    },
    'api_name': 'semmed'
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
    },
    'api_name': 'semmed'
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
    },
    'api_name': 'semmed'
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
    },
    'api_name': 'semmed'
  },
  "phenotype": {
    "scopes": ['umls', 'name'],
    "doc_type": "PhenotypicFeature",
    "api_type": "biothings",
    "url": "http://pending.biothings.io/semmedphenotype/query",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/semmedphenotype/schema.json",
    "method": "post",
    "fields": {
      "name": "name",
      "umls": "umls"
    },
    "hint": True,
    'api_name': 'semmed'
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
    },
    'api_name': 'semmed'
  },
  "biolink_anatomy2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/anatomy/{anatomy_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_anatomy2gene.json",
    "method": "get",
    "path": "anatomy_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_disease2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2gene.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },

  "biolink_disease2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2pathway.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_disease2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/disease/{disease_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_disease2phenotype.json",
    "method": "get",
    "path": "disease_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_gene2anatomy": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/anatomy?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2anatomy.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_gene2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2disease.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_geneinteraction": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/interactions?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_geneinteraction.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_gene2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:{gene_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_gene2phenotype.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_pathway2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2disease.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink",
    'api_name': 'biolink'
  },
  "biolink_pathway2phenotype": {
    "url": "https://api.monarchinitiative.org/api/bioentity/pathway/REACT:{pathway_id}/phenotypes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_pathway2phenotype.json",
    "method": "get",
    "path": "pathway_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_phenotype2disease": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/diseases?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2disease.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': 'biolink'
  },
  "biolink_phenotype2gene": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/genes?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2gene.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
  "biolink_phenotype2pathway": {
    "url": "https://api.monarchinitiative.org/api/bioentity/phenotype/{phenotype_id}/pathways?rows=100",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/biolink/schema/biolink_phenotype2pathway.json",
    "method": "get",
    "path": "phenotype_id",
    'api_type': "biolink",
    'api_name': "biolink"
  },
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
  "dgidb_gene2chemical": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?genes={gene_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_gene2chemical.json",
    "method": "get",
    "path": "gene_id",
    'api_type': "other",
    'api_name': "dgidb"
  },
  "dgidb_chemical2gene": {
    "url": "http://www.dgidb.org/api/v2/interactions.json?drugs={chembl_id}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/dgidb/schema/dgidb_chemical2gene.json",
    "method": "get",
    "path": "chembl_id",
    'api_type': "other",
    'api_name': "dgidb"
  },
  "quickgo_children": {
    "url": "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{goterm}/children",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/quickgo/schema/children.json",
    "method": "get",
    "path": "goterm",
    'api_type': "other",
    'api_name': 'quickgo'
  },
  "litvar": {
    "url": "https://www.ncbi.nlm.nih.gov/research/bionlp/litvar/api/v1/entity/litvar/{dbsnp}##",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/litvar/schema/schema.json",
    "method": "get",
    "path": "dbsnp",
    'api_type': "other",
    'api_name': 'litvar'
  },
  "ols_children": {
    "url": "https://www.ebi.ac.uk/ols/api/ontologies/doid/children?id={doid}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ols/schema/schema.json",
    "method": "get",
    "path": "doid",
    'api_type': "other",
    'api_name': "ontology lookup service"
  },
  "cohd_disease2chemical": {
    "url": "http://cohd.io/api/frequencies/associatedConceptDomainFreq?dataset_id=1&concept_id={cohd}&domain=Drug",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/cohd/schema/disease2chemical.json",
    "method": "get",
    "path": "cohd",
    'api_type': "other",
    'api_name': 'cohd'
  },
  "stanford_biosample_disease2sample": {
    "url": "http://api.kp.metadatacenter.org/biosample/search?q=biolink:Disease={mondo}&limit=1000",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/stanford/disease2sample.json",
    "method": "get",
    "path": "mondo",
    "api_type": "stanford",
    "api_name": "stanford_kp"
  },
  "stanford_biosample_cl2sample": {
    "url": "http://api.kp.metadatacenter.org/biosample/search?q=biolink:CellLine={clo}&limit=1000",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/stanford/cl2sample.json",
    "method": "get",
    "path": "clo",
    "api_type": "stanford",
    "api_name": "stanford_kp"
  },
  "chembl_drug_mechanism": {
    "url": "https://www.ebi.ac.uk/chembl/api/data/mechanism.json?molecule_chembl_id={chembl}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/ChEMBL/drugmechanism.json",
    "method": "get",
    "path": "chembl",
    "api_type": "other",
    "api_name": "ChEMBL"
  },
  "ctd_chemical2gene": {
    "url": "http://ctdbase.org/tools/batchQuery.go?inputType=chem&inputTerms={mesh}|mercury&report=genes_curated&format=json",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/CTD_api/chemical2gene.json",
    "method": "get",
    "path": "mesh",
    "api_type": "ctd",
    "api_name": "CTD"
  },
  "ctd_gene2disease": {
    "url": "http://ctdbase.org/tools/batchQuery.go?inputType=gene&inputTerms={entrez}&report=diseases_curated&format=json",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/CTD_api/gene2disease.json",
    "method": "get",
    "path": "entrez",
    "api_type": "ctd",
    "api_name": "CTD"
  },
  "opentarget": {
    "url": "https://platform-api.opentargets.io/v3/platform/public/evidence/filter?target={ensembl}&datasource=chembl&size=15&fields=drug",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/opentarget/gene2chemical.json",
    "method": "get",
    "path": "ensembl",
    "api_type": "opentarget",
    "api_name": "opentarget"
  },
  "RGD": {
    "url": "https://rest.rgd.mcw.edu/rgdws/genes/{rgd}",
    "mapping_url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/openapi_2.0/RGD/schema.json",
    "method": "get",
    "path": "rgd",
    "api_type": "other",
    "api_name": "RGD"
  }
}
