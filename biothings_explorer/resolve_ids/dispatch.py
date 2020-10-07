from collections import defaultdict
from aiohttp import ClientTimeout
import traceback

from .parser import BioThingsParser

from ..config_new import (
    ALWAYS_PREFIXED,
    ID_RESOLVING_APIS,
    MAX_CONCURRENT_QUERIES_ON_SINGLE_API,
)


class Dispatcher:
    def __init__(self, inputIDs, session):
        self.inputIds = inputIDs
        self.tasks = defaultdict(list)
        self.invalid = {}
        self.session = session

    def dispatch(self):
        for semantic_type, curies in self.inputIds.items():
            res = self.generateQueryTasks(curies, semantic_type)
            for i in range(0, len(res["valid"]), MAX_CONCURRENT_QUERIES_ON_SINGLE_API):
                self.tasks[i] += res["valid"][
                    i : i + MAX_CONCURRENT_QUERIES_ON_SINGLE_API
                ]
            self.invalid[semantic_type] = res.get("invalid")

    def groupIdByPrefix(self, ids, semantic_type):
        if not ids:
            return {}
        mapping = {}
        res = defaultdict(set)
        for _id in ids:
            if isinstance(_id, int):
                res["invalid"].add(str(_id))
                continue
            if not isinstance(_id, str):
                continue
            splitted = _id.split(":", 1)
            if len(splitted) == 1:
                res["invalid"].add(_id)
            else:
                prefix = splitted[0]
                if semantic_type not in ID_RESOLVING_APIS:
                    res["invalid"].add(_id)
                    continue
                if prefix not in ID_RESOLVING_APIS[semantic_type]["mapping"]:
                    res["invalid"].add(_id)
                    continue
                val = splitted[-1]
                if prefix in ALWAYS_PREFIXED:
                    val = prefix + ":" + val
                mapping[prefix + ":" + val] = _id
                val = '"' + val + '"'
                res[prefix].add(val)
        res = dict(res)
        if mapping:
            res.update({"mapping": mapping})
        return res

    def generateQueryTasks(self, curies, semantic_type):
        inputs = self.groupIdByPrefix(curies, semantic_type)
        res = {"valid": [], "invalid": []}
        if not inputs:
            return res
        for prefix, ids in inputs.items():
            if prefix == "invalid":
                res["invalid"] = list(ids)
                continue
            if prefix == "mapping":
                res["mapping"] = ids
                continue
            ids = list(ids)
            for i in range(0, len(ids), 1000):
                query = self.constructQuery(ids[i : i + 1000], semantic_type, prefix)
                if not query:
                    res["invalid"] += [
                        (prefix + ":" + item) for item in ids[i : i + 1000]
                    ]
                else:
                    res["valid"].append(query)
        return res

    def constructQuery(self, inputs, semantic_type, prefix):
        """construct a BioThings batch query using axios
        The query aims to fetch all equivalent IDs for the inputs
        note: the input IDs must be less than 1000;
        The return value is an axios post query promises
        """
        query = "q={inputs}&scopes={scopes}&fields={fields}&dotfield=true&species=human"
        if not inputs:
            return
        if semantic_type not in ID_RESOLVING_APIS:
            return
        if prefix not in ID_RESOLVING_APIS[semantic_type]["mapping"]:
            return
        fields = []
        for item in ID_RESOLVING_APIS[semantic_type]["mapping"].values():
            fields += item
        scopes = ID_RESOLVING_APIS[semantic_type]["mapping"][prefix]
        query = (
            query.replace("{inputs}", ",".join(inputs))
            .replace("{scopes}", ",".join(scopes))
            .replace("{fields}", ",".join(fields))
        )
        return self.callSingleAPI(semantic_type, query, prefix)

    async def callSingleAPI(self, semanticType, query, prefix):
        async with self.session.post(
            ID_RESOLVING_APIS[semanticType]["url"] + "/query",
            data=query,
            timeout=ClientTimeout(20),
            headers={"content-type": "application/x-www-form-urlencoded"},
        ) as res:
            if res.status >= 400:

                print(
                    "api call to {} failed with status code {}".format(
                        ID_RESOLVING_APIS[semanticType]["url"] + "/query", res.status
                    )
                )
                print(res.json())
                return
            try:
                res = await res.json()
                parser = BioThingsParser(res, semanticType, prefix)
                res = parser.parse()
                return res
            except Exception as e:
                traceback.print_exc()
                print("failed to resolve {} ids".format(semanticType))
                return

