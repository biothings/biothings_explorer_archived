from .nodeDegree import NodeDegreeFilter
from .ngd import NGDFilter
from .drugPhase import DrugPhaseFilter


class Filter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.criteria = criteria

    def annotate(self):
        if "nodeDegree" in self.criteria:
            f = NodeDegreeFilter(self.stepResult, {})
            f.annotateNodeDegree()
        if "ngd" in self.criteria:
            f = NGDFilter(self.stepResult, {})
            f.annotateNGD()
        if "drugPhase" in self.criteria:
            f = DrugPhaseFilter(self.stepResult, {})
            f.annotate()
        return self.stepResult

    # def filter(self):
    #     if "nodeDegree" in self.criteria:
    #         f = NodeDegreeFilter(self.stepResult, self.criteria.get("nodeDegree"))
    #         f.annotateNodeDegree()
    #         self.stepResult = f.filter()
    #     return self.stepResult
