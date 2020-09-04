from os.path import commonprefix


def generateCurie(idType, _id):
    if isinstance(_id, list):
        _id = _id[0]
    if ":" in _id:
        _id = _id.split(":")[-1]
    return idType + ":" + _id


def find_longest_common_path(paths) -> str:
    """Find longest common path among a list of paths.

    :param: paths: a list of paths, with '.' as the separator
    """
    return commonprefix(paths).rsplit(".", 1)[0]


def process_publications(res):
    if "pubmed" in res:
        if not isinstance(res["pubmed"], list):
            res["pubmed"] = [res["pubmed"]]
        res["publications"] = [("PMID:" + item) for item in res["pubmed"]]
    if "pmc" in res:
        if not isinstance(res["pmc"], list):
            res["pmc"] = [res["pmc"]]
        res["publications"] = [("PMC:" + item) for item in res["pmc"]]
    return res
