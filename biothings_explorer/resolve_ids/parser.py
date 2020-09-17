from collections import defaultdict

from ..config_new import ID_RESOLVING_APIS, ALWAYS_PREFIXED


class BioThingsParser:
    def __init__(self, response, semanticType, prefix):
        self.response = response
        self.semanticType = semanticType
        self.prefix = prefix
        self.invalid = []

    def parse(self):
        result = {}
        if not self.response or len(self.response) == 0:
            return result
        mapping = ID_RESOLVING_APIS[self.semanticType]["mapping"]
        for rec in self.response:
            if not rec:
                continue
            if self.prefix in ALWAYS_PREFIXED:
                curie = rec.get("query")
            else:
                curie = self.prefix + ":" + rec.get("query")
            if "notfound" in rec:
                self.invalid.append(curie)
                continue
            if curie not in result:
                result[curie] = defaultdict(set)
            if (
                self.semanticType == "Gene"
                and "symbol" in rec
                and "label" not in result[curie]
            ):
                result[curie]["label"] = (
                    set([rec["symbol"]])
                    if not isinstance(rec["symbol"], list)
                    else set([rec["symbol"][0]])
                )
            for prefix, fields in mapping.items():
                for field in fields:
                    if field in rec:
                        if isinstance(rec[field], list):
                            if prefix == "name" and "label" not in result[curie]:
                                result[curie]["label"].add(str(rec[field][0]))
                            rec[field] = [str(item) for item in rec[field]]
                            result[curie][prefix].update(rec[field])
                        else:
                            if prefix == "name" and "label" not in result[curie]:
                                result[curie]["label"].add(str(rec[field]))
                            result[curie][prefix].add(str(rec[field]))
        return self.restructureOutput(result, self.semanticType)

    def restructureOutput(self, res, semanticType):
        result = {}
        for curie in self.invalid:
            db_id = curie
            if curie.split(":")[0] not in ALWAYS_PREFIXED:
                db_id = curie.split(":", 1)[-1]
            result[curie] = {
                "id": {"identifier": curie, "label": curie},
                "curies": [curie],
                "db_ids": {curie.split(":")[0]: [db_id]},
                "type": semanticType,
                "flag": "failed",
            }
        ranks = ID_RESOLVING_APIS[semanticType]["id_ranks"]
        for curie, resolved_ids in res.items():
            ids = set()
            result[curie] = {"id": {}, "db_ids": {}, "type": semanticType}
            if "label" in resolved_ids:
                result[curie]["id"]["label"] = list(res[curie]["label"])[0]
            elif "name" in resolved_ids:
                result[curie]["id"]["label"] = list(res[curie]["name"])[0]
            else:
                result[curie]["id"]["label"] = curie
            primary_id_found = False
            for _id in ranks:
                if resolved_ids[_id] and len(resolved_ids[_id]) > 0:
                    result[curie]["db_ids"][_id] = list(res[curie][_id])
                    for item in res[curie][_id]:
                        item_curie = item
                        if _id not in ALWAYS_PREFIXED:
                            item_curie = _id + ":" + str(item)
                        if not primary_id_found:
                            result[curie]["id"]["identifier"] = item_curie
                            primary_id_found = True
                        if _id != "name":
                            ids.add(item_curie)
            result[curie]["curies"] = list(ids)
        return result
