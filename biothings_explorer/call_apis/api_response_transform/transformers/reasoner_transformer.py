from collections import defaultdict

from .base_transformer import BaseTransformer
from ....config_new import ALWAYS_PREFIXED


class ReasonerTransformer(BaseTransformer):
    def wrap(self, res):
        result = defaultdict(list)
        if not res.get("knowledge_graph"):
            return res
        if not res["knowledge_graph"].get("edges"):
            return res
        for edge in res["knowledge_graph"]["edges"]:
            if "target_id" in edge:
                prefix = edge["target_id"].split(":")[0]
                if prefix in ALWAYS_PREFIXED:
                    result[prefix].append(edge["target_id"])
                else:
                    result[prefix].append(edge["target_id"].split(":")[-1])
        return {self.edge["association"]["predicate"]: result}

    def jsonTransform(self, res):
        return res
