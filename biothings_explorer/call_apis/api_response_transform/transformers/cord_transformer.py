from .biothings_transformer import BioThingsTransformer


class CordTransformer(BioThingsTransformer):
    def wrap(self, res):
        PREFIXES = ["pr", "go", "mop", "hgnc", "uberon", "so", "cl", "doid", "chebi"]
        result = {}
        for val in res.values():
            tmp = []
            if isinstance(val, list) and len(val) > 0:
                for item in val:
                    if item["@type"] == self.edge["association"]["output_type"] or (
                        item["@type"] == "DiseaseOrPhenotypicFeature"
                        and self.edge["association"]["output_type"] == "Disease"
                    ):
                        for k in item.keys():
                            if k in PREFIXES:
                                item[k.upper()] = item.pop(k)
                        tmp.append(item)
            if len(tmp) > 0:
                result["related_to"] = tmp
        return result

    def jsonTransform(self, res):
        return res
