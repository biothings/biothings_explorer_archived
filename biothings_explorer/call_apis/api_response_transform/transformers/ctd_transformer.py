from .base_transformer import BaseTransformer


class CTDTransformer(BaseTransformer):
    def wrap(self, res):
        if isinstance(res, list):
            res = {"data": res}
        for _doc in res["data"]:
            if "PubMedIds" in _doc:
                _doc["PubMedIds"] = _doc["PubMedIds"].split("|")
            if "DiseaseID" in _doc:
                _doc["DiseaseID"] = _doc["DiseaseID"].split(":")[-1]
        return res
