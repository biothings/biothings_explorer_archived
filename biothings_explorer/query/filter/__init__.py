from .nodeDegree import NodeDegreeFilter


class Filter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.criteria = criteria

    def filter(self):
        if "nodeDegree" in self.criteria:
            f = NodeDegreeFilter(self.stepResult, self.criteria.get("nodeDegree"))
            f.annotateNodeDegree()
            self.stepResult = f.filter()
        return self.stepResult
