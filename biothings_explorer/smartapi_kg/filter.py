from collections import defaultdict

from .config import FILTER_FIELDS


def filterOps(ops, criteria):
    """filter an array of objects based on the filter criteria"""
    all_values = defaultdict(set)
    filters = {}
    for op in ops:
        for field in FILTER_FIELDS:
            all_values[field].add(op["association"].get(field))
    for field in FILTER_FIELDS:
        if field not in criteria or criteria.get(field) is None:
            filters[field] = all_values[field]
        else:
            if not isinstance(criteria[field], list):
                criteria[field] = [criteria[field]]
            filters[field] = set(criteria[field])
    res = []
    for op in ops:
        match = True
        for field in FILTER_FIELDS:
            if op["association"][field] not in filters[field]:
                match = False
                break
        if match:
            res.append(op)
    return res
