API_LIST = [
    "mygene",
    "ctd",
    "cord_gene",
    "cord_protein",
    "cord_chemical",
    "cord_disease",
    "cord_cell",
    "cord_molecular_activity",
    "cord_biological_process",
    "cord_cellular_component",
    "cord_anatomy",
    "cord_genomic_entity",
    "semmed_gene",
    "semmed_chemical",
    "semmed_disease",
    "semmed_biological_process",
    "semmed_anatomy",
    "semmed_phenotype",
    "scibite",
    "biolink",
    "opentarget",
    "dgidb",
    "mydisease",
    "mychem",
    "myvariant",
    "DISEASES",
    "scigraph",
    "pharos",
    "hmdb",
    "hetio",
    "chembio",
    "mgi_gene2phenotype"
]

ID_RESOLVING_APIS = {
    "Gene": {
        "id_ranks": ["NCBIGene", "ENSEMBL", "HGNC", "UMLS", "UNIPROTKB", "SYMBOL", "OMIM", "MGI"],
        "semantic": "Gene",
        "api_name": "mygene.info",
        "url": "http://mygene.info/v3",
        "mapping": {
            "NCBIGene": ["entrezgene"],
            "name": ["name"],
            "SYMBOL": ["symbol"],
            "UMLS": ["umls.cui", "umls.protein_cui"],
            "HGNC": ["HGNC"],
            "UNIPROTKB": ["uniprot.Swiss-Prot"],
            "ENSEMBL": ["ensembl.gene"],
            "OMIM": ["OMIM"],
            "MGI": ["MGI"]
        }
    },
    "SequenceVariant": {
        "id_ranks": ["DBSNP", "MYVARIANT_HG19", "HGVS", "ClinVar"],
        "api_name": "myvariant.info",
        "semantic": "SequenceVariant",
        "url": 'http://myvariant.info/v1',
        "mapping": {
            "MYVARIANT_HG19": ["_id"],
            "DBSNP": ["dbsnp.rsid", "clinvar.rsid", "dbnsfp.rsid"],
            "HGVS": ["clinvar.hgvs.genomic", "clinvar.hgvs.protein", "clinvar.hgvs.coding"],
            "ClinVar": ["clinvar.rcv.accession"]
        }
    },
    "ChemicalSubstance": {
        "id_ranks": ["CHEBI", "CHEMBL.COMPOUND", "DRUGBANK", "PUBCHEM", "MESH", "UNII", "UMLS", "name"],
        "semantic": "ChemicalSubstance",
        "api_name": "mychem.info",
        "url": "http://mychem.info/v1",
        "mapping": {
            "CHEMBL.COMPOUND": ["chembl.molecule_chembl_id", "drugbank.xrefs.chembl", "drugcentral.xrefs.chembl_id"],
            "DRUGBANK": ["drugcentral.xrefs.drugbank_id", "pharmgkb.xrefs.drugbank", "chebi.xrefs.drugbank", "drugbank.id"],
            "PUBCHEM": ["pubchem.cid", "drugbank.xrefs.pubchem.cid", "drugcentral.xrefs.pubchem_cid", "pharmgkb.xrefs.pubchem.cid"],
            "CHEBI": ["chebi.id", "chembl.chebi_par_id", "drugbank.xrefs.chebi", "drugcentral.xrefs.chebi"],
            "UMLS": ["drugcentral.xrefs.umlscui", "pharmgkb.xrefs.umls", "umls.cui"],
            "MESH": ["umls.mesh", "drugcentral.xrefs.mesh_descriptor_ui", "ginas.xrefs.MESH", "pharmgkb.xrefs.mesh"],
            "UNII": ["drugcentral.xrefs.unii", "unii.unii", "aeolus.unii", "ginas.unii"],
            "name": ["chembl.pref_name", "drugbank.name", "umls.name", "ginas.preferred_name", "pharmgkb.name", "chebi.name"]
        }
    },
    "Disease": {
        "id_ranks": ["MONDO", "DOID", "OMIM", "ORPHANET", "UMLS", "MESH", "name"],
        "semantic": "Disease",
        "api_name": "mydisease.info",
        "url": "http://mydisease.info/v1",
        "mapping": {
            "MONDO": ["_id"],
            "DOID": ["mondo.xrefs.doid"],
            "UMLS": ['mondo.xrefs.umls', "disgenet.xrefs.umls"],
            "name": ["mondo.label", "disgenet.xrefs.disease_name"],
            "MESH": ["mondo.xrefs.mesh", "ctd.mesh"],
            "OMIM": ["mondo.xrefs.omim", "hpo.omim"],
            "ORPHANET": ["hpo.orphanet", "mondo.xrefs.orphanet"]
        }
    },
    "MolecularActivity": {
        "id_ranks": ["GO", "name"],
        "semantic": "MolecularActivity",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "GO": ["go"],
            "name": ["name"]
        }
    },
    "BiologicalProcess": {
        "id_ranks": ["GO", "UMLS", "name"],
        "semantic": "BiologicalProcess",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "GO": ["go"],
            "name": ["name"],
            "UMLS": ["umls"]
        }
    },
    "CellularComponent": {
        "id_ranks": ["GO", "UMLS", "name"],
        "semantic": "CellularComponent",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "GO": ["go"],
            "name": ["name"],
            "UMLS": ["umls"]
        }
    },
    "Pathway": {
        "id_ranks": ["Reactome", "KEGG", "PHARMGKB", "WIKIPATHWAYS", "name"],
        "semantic": "Pathway",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "Reactome": ["reactome"],
            "WIKIPATHWAYS": ["wikipathways"],
            "KEGG": ["kegg"],
            "PHARMGKB": ['pharmgkb'],
            "name": ["name"]
        }
    },
    "AnatomicalEntity": {
        "id_ranks": ["UMLS", "name"],
        "semantic": "AnatomicalEntity",
        "api_name": "Anatomy API",
        "url": "http://biothings.ncats.io/semmed_anatomy",
        "mapping": {
            "name": ["name"],
            "UMLS": ["umls"]
        }
    },
    "PhenotypicFeature": {
        "id_ranks": ["UMLS", "name"],
        "semantic": "PhenotypicFeature",
        "api_name": "Phenotype API",
        "url": "http://biothings.ncats.io/semmedphenotype",
        "mapping": {
            "name": ["name"],
            "UMLS": ["umls"]
        }
    }
}