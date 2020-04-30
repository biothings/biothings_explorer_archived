"""Parse the biothings schema"""

from .config import BIOTHINGS_SCHEMA_URL, PREFIX_TO_REMOVE
from .utils.dataload import load_json_or_yaml
from .utils.common import remove_prefix

class SchemaParser():
    def __init__(self):
        self.schema_json = remove_prefix(load_json_or_yaml(BIOTHINGS_SCHEMA_URL),
                                         PREFIX_TO_REMOVE)
        self.properties = {}
        self.ids = []
        self.clses = []
        self.process_schema()

    def process_schema(self):
        for rec in self.schema_json['@graph']:
            if "rdfs:subPropertyOf" in rec and rec["rdfs:subPropertyOf"]["@id"] == "http://schema.org/identifier":
                self.ids.append(rec["@id"])
            elif rec["@type"] == "rdf:Property":
                self.properties[rec["@id"]] = {"inverse_property": None}
                if "schema:inverseOf" in rec:
                    self.properties[rec["@id"]]["inverse_property"] = rec["schema:inverseOf"]["@id"]
            elif rec["@type"] == "rdfs:Class":
                self.clses.append(rec["@id"])
