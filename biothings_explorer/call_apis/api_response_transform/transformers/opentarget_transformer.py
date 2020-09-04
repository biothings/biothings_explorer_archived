from .base_transformer import BaseTransformer


class OpenTargetTransformer(BaseTransformer):
    def wrap(self, res):
        if not res.get("data"):
            return res
        for _doc in res["data"]:
            if "drug" in _doc:
                if "CHEMBL" in _doc["drug"]["id"]:
                    _doc["drug"]["id"] = _doc["drug"]["id"].split("/")[-1]
        return res
