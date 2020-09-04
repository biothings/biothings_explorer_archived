def generateFailedResponse(curie, _type):
    return {
        "id": {"identifier": curie, "label": curie},
        "curies": [curie],
        "db_ids": {curie.split(":")[0]: [curie]},
        "type": _type,
        "flag": "failed",
    }
