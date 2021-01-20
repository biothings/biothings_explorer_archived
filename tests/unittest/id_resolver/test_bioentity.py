import unittest
from biothings_explorer.resolve_ids.bioentity import BioEntity

CDK2_DB_IDs = {
    "NCBIGene": ["1017"],
    "HGNC": ["1771"],
    "SYMBOL": ["CDK2"],
    "name": ["cyclin dependent kinase 2"],
}

RILUZOLE_DB_IDS = {
    "CHEMBL.COMPOUND": ["CHEMBL744"],
    "name": ["Riluzole", "RILUZOLE"],
    "PUBCHEM": ["5070"],
}

CHEMBL7512_DB_IDS = {"CHEMBL.COMPOUND": ["CHEMBL7512"], "PUBCHEM": ["53428"]}

KARTAGENER_SYNDROME_DB_IDS = {
    "MONDO": ["MONDO:0016575"],
    "DOID": ["DOID:0050144"],
    "MESH": ["D007619"],
}


class TestBioEntityClass(unittest.TestCase):
    def test_get_primary_id(self):
        entity = BioEntity("Gene", CDK2_DB_IDs)
        primary_id = entity.get_primary_id()
        self.assertEqual(primary_id, "NCBIGene:1017")

    def test_get_label_if_symbol_provided(self):
        entity = BioEntity("Gene", CDK2_DB_IDs)
        label = entity.get_label()
        self.assertEqual(label, "CDK2")

    def test_get_label_if_symbol_not_provided(self):
        entity = BioEntity("ChemicalSubstance", RILUZOLE_DB_IDS)
        label = entity.get_label()
        self.assertEqual(label, "Riluzole")

    def test_get_label_if_symbol_and_label_are_not_provided(self):
        entity = BioEntity("ChemicalSubstance", CHEMBL7512_DB_IDS)
        label = entity.get_label()
        self.assertEqual(label, "CHEMBL.COMPOUND:CHEMBL7512")

    def test_get_curies(self):
        entity = BioEntity("Disease", KARTAGENER_SYNDROME_DB_IDS)
        curies = entity.get_curies()
        self.assertIn("MONDO:0016575", curies)
        self.assertIn("DOID:0050144", curies)
        self.assertIn("MESH:D007619", curies)
