from collections import Counter, defaultdict
import requests
import json


class DrugPhaseFilter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.cnt = Counter()
        self.criteria = criteria

    @staticmethod
    def _extractInputID(resolvedIDs, semanticType):
        if semanticType != "ChemicalSubstance":
            return
        if "db_ids" not in resolvedIDs or not isinstance(resolvedIDs["db_ids"], dict):
            return
        prefix = "CHEMBL.COMPOUND"
        if not prefix in resolvedIDs["db_ids"]:
            return
        return resolvedIDs["db_ids"][prefix]

    @staticmethod
    def _queryDrug(inputs):
        if not inputs:
            return
        result = []
        for i in range(0, len(inputs), 1000):
            a = {
                "q": ",".join(inputs[i : i + 1000]),
                "scopes": "chembl.molecule_chembl_id",
                "fields": "chembl.max_phase",
                "dotfield": True,
            }
            res = requests.post("https://mychem.info/v1/query", json=a,)
            result += res.json()
        return result

    @staticmethod
    def _parseResponse(res):
        if not res:
            return
        result = {}
        for rec in res:
            if "chembl.max_phase" in rec:
                if isinstance(rec["chembl.max_phase"], list):
                    rec["chembl.max_phase"] = max(rec["chembl.max_phase"])
                result[rec["query"]] = rec["chembl.max_phase"]
        return result

    def annotate(self):
        """
        Add node degree info to each edge.
        :param stepResult: a list of returned result from query.
        """
        id_dict = defaultdict(list)
        chembl_ids = set()
        if not self.stepResult:
            return
        for i, rec in enumerate(self.stepResult):
            if "$association" not in rec:
                continue
            output_type = rec["$association"]["output_type"]
            if output_type != "ChemicalSubstance":
                continue
            output_resolved_ids = rec["$output_id_mapping"]["resolved_ids"]
            output_id = self._extractInputID(output_resolved_ids, output_type)
            if not output_id:
                continue
            for o_id in output_id:
                chembl_ids.add(o_id)
                id_dict[i].append(o_id)
        annotatedResult = self._parseResponse(self._queryDrug(list(chembl_ids)))
        cnt = 0
        for i, rec in enumerate(self.stepResult):
            if i in id_dict:
                drug_phases = []
                for o_id in id_dict[i]:
                    if o_id in annotatedResult:
                        drug_phases.append(annotatedResult[o_id])
                if drug_phases:
                    rec["$drug_phase"] = max(drug_phases)
                    cnt += 1
            else:
                rec["$drug_phase"] = 0
        if cnt > 0:
            print(
                "Number of output edges sent to Drug Phase annotation is {}. Number of output edges annotated with Drug Phase is {}".format(
                    len(self.stepResult), cnt
                )
            )
        return

    def filter(self):
        res = []
        if "sort" in self.criteria:
            limit = (
                int(self.criteria["sort"].get("limit"))
                if self.criteria["sort"].get("limit")
                else 0
            )
            if self.criteria["sort"].get("direction") != "descend":
                idList = [item[0] for item in self.cnt.most_common(limit)]
                for rec in self.stepResult:
                    if rec["$output"] in idList:
                        res.append(rec)
                return res
            sortedList = self.cnt.most_common(len(self.cnt))
            sortedList.reverse()
            idList = [item[0] for i, item in enumerate(sortedList) if i < limit]
            for rec in self.stepResult:
                if rec["$output"] in idList:
                    res.append(rec)
            return res
