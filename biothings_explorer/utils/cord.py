SEMANTIC_TYPE_ID_MAPPING = {
    'ChemicalSubstance': ['CHEBI'],
    'Cell': ['CL'],
    'DiseaseOrPhenotypicFeature': ['DOID'],
    'Gene': ['HGNC'],
    'MolecularActivity': ['MOP', 'GO'],
    'BiologicalProcess': ['GO'],
    "Protein": ['PR'],
    "GenomicEntity": ['SO'],
    "AnatomicalEntity": ["UBERON"],
    "CellularComponent": ['GO']
}
cord = {
    "Gene": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "Cell": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "DiseaseOrPhenotypicFeature": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "MolecularActivity": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "Protein": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "GenomicEntity": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "AnatomicalEntity": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "BiologicalProcess": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "CellularComponent": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    },
    "ChemicalSubstance": {
        "associated_with": [
            "ChemicalSubstance",
            "Cell",
            "DiseaseOrPhenotypicFeature",
            "MolecularActivity",
            "Protein",
            "GenomicEntity",
            "Gene",
            "AnatomicalEntity",
            "BiologicalProcess",
            "CellularComponent"
        ]
    }
}