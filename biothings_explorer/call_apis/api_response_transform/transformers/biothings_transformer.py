from .base_transformer import BaseTransformer
from .utils import generateCurie


class BioThingsTransformer(BaseTransformer):
    def pairInputWithAPIResponse(self):
        res = {}
        for item in self.data["response"]:
            if "notfound" not in item:
                _input = generateCurie(
                    self.edge["association"]["input_id"], item["query"]
                )
                if _input in res:
                    res[_input].append(item)
                else:
                    res[_input] = [item]
        return res
