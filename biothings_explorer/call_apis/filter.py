from functools import partial

# from ..config_new import BTE_FILTERS
BTE_FILTERS = ["nodeDegree", "ngd", "drugPhase", "survivalProbability"]


def filter_response(res, criteria):
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

    if not res or not isinstance(res, list) or not len(res) > 0:
        return res
    if not isinstance(criteria, dict):
        return res
    for f, v in criteria.items():
        if not isinstance(v, dict):
            continue
        if f not in BTE_FILTERS:
            if "=" in v:
                res = list(
                    filter(
                        partial(filter_by_operation, key=f, val=v["="], operation="="),
                        res,
                    )
                )
                continue
            if ">" in v:
                res = list(
                    filter(
                        partial(filter_by_operation, key=f, val=v[">"], operation=">"),
                        res,
                    )
                )
            elif "<" in v:
                res = list(
                    filter(
                        partial(filter_by_operation, key=f, val=v["<"], operation="<"),
                        res,
                    )
                )
    return res
