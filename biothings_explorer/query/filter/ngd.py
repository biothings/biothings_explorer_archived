from collections import Counter, defaultdict
import requests
import json


TYPE_TO_ID_MAPPING = {
    "Gene": "NCBIGene",
    "ChemicalSubstance": "CHEBI",
    "AnatomicalEntity": "UBERON",
    "BiologicalProcess": "GO",
    "MolecularActivity": "GO",
    "Cell": "CL",
    "SequenceVariant": "SO",
    "Disease": "MONDO",
    "PhenotypicFeature": "HP",
}


class NGDFilter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.cnt = Counter()
        self.criteria = criteria

    @staticmethod
    def _extractInputID(resolvedIDs, semanticType):
        if semanticType not in TYPE_TO_ID_MAPPING:
            return
        if "db_ids" not in resolvedIDs or not isinstance(resolvedIDs["db_ids"], dict):
            return
        prefix = TYPE_TO_ID_MAPPING[semanticType]
        if not prefix in resolvedIDs["db_ids"]:
            return
        return resolvedIDs["db_ids"][prefix]

    @staticmethod
    def _queryNGD(inputs):
        if not inputs:
            return
        result = []
        for i in range(0, len(inputs), 1000):
            a = {
                "q": [item.split("-") for item in inputs[i : i + 1000]],
                "scopes": [["subject.id", "object.id"], ["object.id", "subject.id"],],
                "fields": "association.ngd",
                "dotfield": True,
            }
            res = requests.post(
                "https://biothings.ncats.io/text_mining_co_occurrence_kp/query", json=a,
            )
            res = res.json()
            result += res
        return result

    @staticmethod
    def _parseResponse(res):
        if not res:
            return
        result = {}
        for rec in res:
            if "association.ngd" in rec:
                result["-".join(rec["query"])] = rec["association.ngd"]
        return result

    def annotateNGD(self):
        """
        Add node degree info to each edge.
        :param stepResult: a list of returned result from query.
        """
        id_dict = defaultdict(list)
        ngd_inputs = set()
        if not self.stepResult:
            return
        for i, rec in enumerate(self.stepResult):
            if not "$association" in rec:
                continue
            input_type = rec["$association"]["input_type"]
            input_resolved_ids = rec["$original_input"][rec["$input"]]
            output_type = rec["$association"]["output_type"]
            output_resolved_ids = rec["$output_id_mapping"]["resolved_ids"]
            input_id = self._extractInputID(input_resolved_ids, input_type)
            output_id = self._extractInputID(output_resolved_ids, output_type)
            if not input_id or not output_id:
                continue
            for s_id, o_id in zip(input_id, output_id):
                if input_type == "Gene":
                    s_id = "NCBIGene:" + str(s_id)
                if output_type == "Gene":
                    o_id = "NCBIGene:" + str(o_id)
                ngd_inputs.add(str(s_id) + "-" + str(o_id))
                id_dict[i].append(str(s_id) + "-" + str(o_id))
        annotatedResult = self._parseResponse(self._queryNGD(list(ngd_inputs)))
        cnt = 0
        for i, rec in enumerate(self.stepResult):
            if i in id_dict:
                ngd_scores = []
                for pair in id_dict[i]:
                    if pair in annotatedResult:
                        ngd_scores.append(annotatedResult[pair])
                if ngd_scores:
                    rec["$ngd"] = min(ngd_scores)
                    cnt += 1
        if cnt > 0:
            print(
                "Number of output edges sent to NGD score annotation is {}. Number of output edges annotated with NGD score is {}".format(
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
