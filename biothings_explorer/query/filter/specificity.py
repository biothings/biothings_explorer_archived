from collections import defaultdict, Counter
from ...call_apis import APIQueryDispatcher
from ...smartapi_kg import MetaKG
from ..utils import annotateEdgesWithInput
from time import time


class SpecificityFilter:
    def __init__(self, stepResult, criteria, source_types):
        self.stepResult = stepResult
        self.criteria = criteria
        self.source_types = source_types
        self.kg = MetaKG()
        self.kg.constructMetaKG(source="local")

    def _collect_all_outputs(self):
        self.output_dict = {}
        for rec in self.stepResult:
            if rec["$association"]["output_type"] not in self.output_dict:
                self.output_dict[rec["$association"]["output_type"]] = {}
            self.output_dict[rec["$association"]["output_type"]][rec["$output"]] = rec[
                "$output_id_mapping"
            ]["resolved_ids"]

    def _find_smartapi_edges(self, output_type):
        return self.kg.filter(
            {"input_type": output_type, "output_type": self.source_types}
        )

    def _parse_response(self, response):
        cnt = {}
        summary = defaultdict(set)
        if not response:
            return {}
        for rec in response:
            summary[rec["$original_input"][rec["$input"]]["id"]["identifier"]].add(
                rec["$output"]
            )
        for k, v in summary.items():
            cnt[k] = len(v)
        return cnt

    def annotate(self):
        """
        Add specificity info to each edge.
        :param stepResult: a list of returned result from query.
        """
        print("start to annotate edges out")
        print("output types", self.source_types)
        t1 = time()
        if not self.stepResult:
            return
        self._collect_all_outputs()
        if not self.output_dict:
            return
        bte_edges = []
        for semanticType, resolvedIDs in self.output_dict.items():
            smartapi_edges = self._find_smartapi_edges(semanticType)
            if not smartapi_edges:
                continue
            tmp_edges = annotateEdgesWithInput(smartapi_edges, resolvedIDs.values())
            if not tmp_edges:
                continue
            bte_edges += tmp_edges
        print("found {} bte edges".format(len(bte_edges)))
        if not bte_edges:
            return

        dp = APIQueryDispatcher(bte_edges)
        res = dp.syncQuery()
        cnt = self._parse_response(res)
        for rec in self.stepResult:
            rec["$edgesOut"] = (
                cnt[rec.get("$output")] if rec.get("$output") in cnt else None
            )
        t2 = time()
        print("Annotating results took {} seconds".format(t2 - t1))
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
