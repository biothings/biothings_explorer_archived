from collections import defaultdict

from .base_transformer import BaseTransformer


class AutomatTransformer(BaseTransformer):
    def wrap(self, res):
        res = {"data": res}
        result = defaultdict(set)

        for rec in res["data"]:
            obj = rec[-1]
            obj_id_prefix = obj["id"].split(":")[0]
            if obj_id_prefix in ["MONDO", "CHEBI", "DOID"]:
                result[obj_id_prefix.lower()].add(obj["id"])
            elif obj_id_prefix in ["NCBIGene", "ENSEMBL"]:
                result[obj_id_prefix.lower()].add(obj["id"].split(":", 1)[-1])
            elif obj_id_prefix == "CHEMBL.COMPOUND":
                result["chembl"].add(obj["id"].split(":", 1)[-1])
            obj = rec[0]
            obj_id_prefix = obj["id"].split(":")[0]
            if obj_id_prefix in ["MONDO", "CHEBI", "DOID"]:
                result[obj_id_prefix.lower()].add(obj["id"])
            elif obj_id_prefix in ["NCBIGene", "ENSEMBL"]:
                result[obj_id_prefix.lower()].add(obj["id"].split(":", 1)[-1])
            elif obj_id_prefix == "CHEMBL.COMPOUND":
                result["chembl"].add(obj["id"].split(":", 1)[-1])
        new_result = {}
        for k, v in result.items():
            new_result[k] = list(v)
        return {"associated_with": new_result}

