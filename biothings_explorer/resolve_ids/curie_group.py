from collections import defaultdict

from ..config_new import ID_RESOLVING_APIS
from ..utils.common import getPrefixFromCurie, getValFromCurie


class CurieGroup:
    def __init__(self, semanticType, curies):
        self.semanticType = semanticType
        self.curies = curies

    @staticmethod
    def _findAPI(semanticType):
        return ID_RESOLVING_APIS.get(semanticType, {})

    def groupCuriesByPrefix(self, curies: list):
        grped = defaultdict(set)
        for curie in curies:
            prefix = getPrefixFromCurie(curie)
            val = getValFromCurie(curie)
            grped[prefix].add(val)
        return grped
