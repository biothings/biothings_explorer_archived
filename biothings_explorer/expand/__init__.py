from collections import defaultdict

from ..smartapi_kg import MetaKG
from ..call_apis import APIQueryDispatcher
from ..query.utils import annotateEdgesWithInput


class Expander:
    def __init__(self):
        self.kg = MetaKG()
        self.kg.constructMetaKG(source="local")

    def __getEdges(self, semanticType):
        """
        Get a list of smart-api edges based on semantic type.

        :param semanticType: Type of bioentities to expand
        :returns: list of smartapi edges expanding the semantic type
        """
        return self.kg.filter(
            {
                "input_type": semanticType,
                "output_type": semanticType,
                "predicate": "has_subclass",
            }
        )

    @staticmethod
    def __parseResponse(res):
        if not res:
            return
        result = {}
        for rec in res:
            if (
                "$output_id_mapping" in rec
                and "resolved_ids" in rec["$output_id_mapping"]
            ):
                result[
                    rec["$output_id_mapping"]["resolved_ids"]["id"]["identifier"]
                ] = rec["$output_id_mapping"]["resolved_ids"]
        return result

    @staticmethod
    def __groupIDsbySemanticType(output_ids):
        result = defaultdict(list)
        for resolved_ids in output_ids:
            result[resolved_ids.get("type")].append(resolved_ids)
        return result

    def expand(self, inputs):
        """
        Expand input biomedical objects to its children
        :param semanticType: semantic type of the inputs
        :param inputs: list of resolved identifiers
        """
        grpedIDs = self.__groupIDsbySemanticType(inputs)
        bte_edges = []
        for semanticType, resolvedIDs in grpedIDs.items():
            smartapi_edges = self.__getEdges(semanticType)
            if not smartapi_edges:
                continue
            tmp_edges = annotateEdgesWithInput(smartapi_edges, resolvedIDs)
            if not tmp_edges:
                continue
            bte_edges += tmp_edges
        if not bte_edges:
            return
        dp = APIQueryDispatcher(bte_edges)
        res = dp.syncQuery()
        return self.__parseResponse(res)
