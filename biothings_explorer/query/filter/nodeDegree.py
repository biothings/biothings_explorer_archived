from collections import Counter


class NodeDegreeFilter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.cnt = Counter()
        self.criteria = criteria

    def annotateNodeDegree(self):
        """
        Add node degree info to each edge.
        :param stepResult: a list of returned result from query.
        """
        if not self.stepResult:
            return
        for rec in self.stepResult:
            self.cnt[rec.get("$output")] += 1
        for rec in self.stepResult:
            rec["$nodeDegree"] = self.cnt[rec.get("$output")]
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
