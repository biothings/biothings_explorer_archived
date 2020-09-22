from .base_transformer import BaseTransformer


class COHDTransformer(BaseTransformer):
    def wrap(self, res):
        print("cohd transformer triggerd")
        if not res.get("results"):
            return res
        new_res = {"results": []}
        for _doc in res["results"]:
            if _doc.get("adj_p-value") == 0:
                for k in _doc:
                    _doc[k] = str(_doc[k])
                new_res["results"].append(_doc)
        return new_res
