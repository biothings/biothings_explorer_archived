from .nodeDegree import NodeDegreeFilter
from .ngd import NGDFilter
from .drugPhase import DrugPhaseFilter
from .hypothesis import HypothesisFilter
from .specificity import SpecificityFilter
from functools import partial

BTE_FILTERS = ["nodeDegree", "ngd", "drugPhase", "survivalProbability", "edgesOut"]


class Filter:
    def __init__(self, stepResult, criteria, source_types):
        self.stepResult = stepResult
        self.criteria = criteria
        self.source_types = source_types
        self.annotated = False

    def annotate(self):
        f = NodeDegreeFilter(self.stepResult, {})
        f.annotateNodeDegree()
        if "ngd" in self.criteria:
            f = NGDFilter(self.stepResult, {})
            f.annotateNGD()
        if "edgesOut" in self.criteria:
            f = SpecificityFilter(self.stepResult, {}, self.source_types)
            f.annotate()
        if "drugPhase" in self.criteria:
            f = DrugPhaseFilter(self.stepResult, {})
            f.annotate()
        if "survivalProbability" in self.criteria:
            f = HypothesisFilter(self.stepResult, {})
            f.annotate()
        self.annotated = True
        return self.stepResult

    def filter_response(self):
        """
        Filter API response based on filtering criteria
        :param res: API Response
        :param criteria: filtering criteria
        """

        def filter_by_operation(rec, key, val, operation):
            if rec.get(key):
                if isinstance(rec.get(key), list):
                    rec[key] = rec[key][0]
                try:
                    if operation == "=" and type(val)(rec[key]) == val:
                        return True
                    if operation == ">" and type(val)(rec[key]) > val:
                        return True
                    if operation == "<" and type(val)(rec[key]) < val:
                        return True
                    return False
                except (ValueError, TypeError):
                    return False
            return False

        if not self.annotated:
            self.annotate()
        if (
            not self.stepResult
            or not isinstance(self.stepResult, list)
            or not len(self.stepResult) > 0
        ):
            return self.stepResult
        if not isinstance(self.criteria, dict):
            return self.stepResult
        for f, v in self.criteria.items():
            if not isinstance(v, dict):
                continue
            if f in BTE_FILTERS:
                f = "$" + f
                if "=" in v:
                    self.stepResult = list(
                        filter(
                            partial(
                                filter_by_operation, key=f, val=v["="], operation="="
                            ),
                            self.stepResult,
                        )
                    )
                    continue
                if ">" in v:
                    self.stepResult = list(
                        filter(
                            partial(
                                filter_by_operation, key=f, val=v[">"], operation=">"
                            ),
                            self.stepResult,
                        )
                    )
                elif "<" in v:
                    self.stepResult = list(
                        filter(
                            partial(
                                filter_by_operation, key=f, val=v["<"], operation="<"
                            ),
                            self.stepResult,
                        )
                    )
        return self.stepResult
