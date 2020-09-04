from .biothings_transformer import BioThingsTransformer


class SemmedTransformer(BioThingsTransformer):
    def wrap(self, res):
        result = {}
        for pred, val in res.items():
            tmp = []
            if isinstance(val, list) and len(val) > 0:
                for item in val:
                    if item["@type"] == self.edge["association"]["output_type"] or (
                        item["@type"] == "DiseaseOrPhenotypicFeature"
                        and self.edge["association"]["output_type"] == "Disease"
                    ):
                        item["UMLS"] = item.pop("umls")
                        item["pubmed"] = item.pop("pmid")
                        tmp.append(item)
            if len(tmp) > 0:
                result[pred] = tmp
        return result

    def jsonTransform(self, res):
        return res
