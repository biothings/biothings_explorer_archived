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
    "opentarget"
]

ID_RESOLVING_APIS = {
    "Gene": {
        "scopes": ['entrezgene', 'symbol', 'name', 'HGNC', 'umls.cui', 'uniprot.Swiss-Prot', "ensembl.gene"],
        "semantic": "Gene",
        "api_name": "mygene.info",
        "url": "http://mygene.info/v3",
        "mapping": {
            "NCBIGene": ["entrezgene"],
            "name": ["name"],
            "SYMBOL": ["symbol"],
            "taxonomy": ["taxid"],
            "UMLS": ["umls.cui", "umls.protein_cui"],
            "HGNC": ["HGNC"],
            "UNIPROTKB": ["uniprot.Swiss-Prot"],
            "ENSEMBL": ["ensembl.gene"],
            "OMIM": ["OMIM"]
        }
    },
    "SequenceVariant": {
        "scopes": ['dbsnp.rsid', '_id', 'clinvar.rsid',
                'dbnsfp.rsid', 'clinvar.hgvs.coding',
                'clinvar.hgvs.genomic', 'clinvar.hgvs.protein'],
        "api_name": "myvariant.info",
        "semantic": "SequenceVariant",
        "url": 'http://myvariant.info/v1',
        "mapping": {
            "MYVARIANT_HG19": ["_id"],
            "DBSNP": ["dbsnp.rsid", "clinvar.rsid", "dbnsfp.rsid"],
            "HGNC": ["clinvar.hgvs.genomic", "clinvar.hgvs.protein", "clinvar.hgvs.coding"],
            "ClinVar": ["clinvar.rcv.accession"]
        }
    },
    "ChemicalSubstance": {
        "scopes": ['chembl.molecule_chembl_id', 'drugbank.id', 'chebi.id', 'chebi.xrefs.chembl', 'chembl.smiles', 'pubchem.smiles.canonical', 
                'chebi.smiles','drugcentral.structures.smiles', 'pubchem.cid', 'chembl.pref_name', 'drugbank.name', 
                'unii.unii', 'ginas.preferred_name', 'drugcentral.xrefs.umlscui', "drugcentral.synonyms", 
                "ginas.name_list", "drugcentral.xrefs.chebi", "drugcentral.xrefs.mesh_descriptor_ui"],
        "semantic": "ChemicalSubstance",
        "api_name": "mychem.info",
        "url": "http://mychem.info/v1",
        "mapping": {
            "CHEMBL.COMPOUND": ["chembl.molecule_chembl_id", "drugbank.xrefs.chembl", "drugcentral.xrefs.chembl_id"],
            "DRUGBANK": ["drugcentral.xrefs.drugbank_id", "pharmgkb.xrefs.drugbank", "chebi.xrefs.drugbank", "drugbank.id"],
            "PUBCHEM": ["pubchem.cid", "chebi.xrefs.pubchem.cid", "drugbank.xrefs.pubchem.cid", "drugcentral.xrefs.pubchem_cid", "pharmgkb.xrefs.pubchem.cid"],
            "CHEBI": ["chebi.id", "chembl.chebi_par_id", "drugbank.xrefs.chebi", "drugcentral.xrefs.chebi"],
            "UMLS": ["drugcentral.xrefs.umlscui", "pharmgkb.xrefs.umls", "umls.cui"],
            "MESH": ["umls.mesh", "drugcentral.xrefs.mesh_descriptor_ui", "ginas.xrefs.MESH", "pharmgkb.xrefs.mesh"],
            "UNII": ["drugcentral.xrefs.unii", "unii.unii", "aeolus.unii", "ginas.unii"],
            "name": ["chembl.pref_name", "drugbank.name", "umls.name", "ginas.preferred_name", "pharmgkb.name", "chebi.name"]
        }
    },
    "Disease": {
        "scopes": ['_id', 'mondo.xrefs.doid', 'mondo.xrefs.hp',
                'mondo.xrefs.mesh', 'mondo.xrefs.umls',
                'mondo.label', 'disgenet.xrefs.disease_name'],
        "semantic": "Disease",
        "api_name": "mydisease.info",
        "url": "http://mydisease.info/v1",
        "mapping": {
            "MONDO": ["_id"],
            "DOID": ["mondo.xrefs.doid"],
            "UMLS": ['mondo.xrefs.umls', "disgenet.xrefs.umls"],
            "name": ["mondo.label", "disgenet.xrefs.disease_name"],
            "MESH": ["mondo.xrefs.mesh", "ctd.mesh"]
        }
    },
    "MolecularActivity": {
        "semantic": "MolecularActivity",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "GO": ["go"],
            "name": ["name"]
        }
    },
    "BiologicalProcess": {
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
        "semantic": "Pathway",
        "api_name": "geneset API",
        "url": "http://biothings.ncats.io/geneset",
        "mapping": {
            "REACTOME": ["reactome"],
            "WIKIPATHWAYS": ["wikipathways"],
            "KEGG": ["kegg"],
            "PHARMGKB": ['pharmgkb'],
            "name": ["name"]
        }
    },
    "AnatomicalEntity": {
        "semantic": "AnatomicalEntity",
        "api_name": "Anatomy API",
        "url": "http://biothings.ncats.io/semmed_anatomy",
        "mapping": {
            "name": ["name"],
            "UMLS": ["umls"]
        }
    },
    "PhenotypicFeature": {
        "semantic": "PhenotypicFeature",
        "api_name": "Phenotype API",
        "url": "http://biothings.ncats.io/semmedphenotype",
        "mapping": {
            "name": ["name"],
            "UMLS": ["umls"]
        }
    }
}