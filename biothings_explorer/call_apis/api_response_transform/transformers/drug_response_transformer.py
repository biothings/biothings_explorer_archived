from .biothings_transformer import BioThingsTransformer


class DrugResponseTransformer(BioThingsTransformer):
    def wrap(self, res):
        if "filter" not in self.edge or "disease_context" not in self.edge["filter"]:
            return []
        if "hits" not in res or not isinstance(res.get("hits"), list):
            return res
        for doc in res.get("hits"):
            if not doc.get("association"):
                continue
            if not doc["association"].get("effect_size"):
                continue
            if not doc["association"].get("pvalue"):
                continue
            doc["association"]["pvalue"] = str(doc["association"]["pvalue"])
            doc["association"]["effect_size"] = str(doc["association"]["effect_size"])
        return res
