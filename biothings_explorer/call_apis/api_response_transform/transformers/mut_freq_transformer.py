from .biothings_transformer import BioThingsTransformer


class MutFreqTransformer(BioThingsTransformer):
    def wrap(self, res):
        if "hits" not in res or not isinstance(res.get("hits"), list):
            return res
        for doc in res.get("hits"):
            if not doc.get("association"):
                continue
            if not doc["association"].get("freq_by_sample"):
                continue
            doc["association"]["freq_by_sample"] = str(
                doc["association"]["freq_by_sample"]
            )
        return res
