def get_apis(edges):
    apis = []
    for v in edges.values():
        apis.append(v['info'].get("$api"))
    return apis