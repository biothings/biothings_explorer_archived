from functools import reduce
from collections import defaultdict

from ..utils.common import getCurieFromVal, dict_set2list
from .bioentity import BioEntity


class BioThingsAPI:
    MAX_BATCH_SIZE = 1000

    def __init__(self, metadata):
        self._process_metadata(metadata)

    def _process_metadata(self, metadata):
        self.url = metadata.get("url")
        self.mapping = metadata.get("mapping")
        self.rank = metadata.get("id_ranks")

    def _get_all_fields(self):
        return reduce(lambda x, y: x + y, self.mapping.values(), [])

    def _get_scope(self, prefix):
        return self.mapping.get(prefix)

    def build_query(self, prefix, ids):
        query = "q={inputs}&scopes={scopes}&fields={fields}&dotfield=true&species=human"
        for i in range(0, len(ids), self.MAX_BATCH_SIZE):
            yield (
                query.replace("{inputs}", ",".join(ids[i : i + self.MAX_BATCH_SIZE]))
                .replace("{scopes}", ",".join(self._get_scope(prefix)))
                .replace("{fields}", ",".join(self._get_all_fields()))
            )

    def __get_db_ids_helper(self, record):
        res = defaultdict(set)
        for k, v in self.mapping.items():
            for field_name in v:
                if field_name in record:
                    if isinstance(record[field_name], list):
                        for val in record[field_name]:
                            res[k].add(str(val))
                    else:
                        res[k].add(str(record[field_name]))
        return dict_set2list(res)

    def get_db_ids(self, prefix, semantic_type, response):
        result = {}
        for rec in response:
            if "notfound" not in rec:
                curie = getCurieFromVal(rec.get("query"), prefix)
                result[curie] = BioEntity(semantic_type, self.__get_db_ids_helper(rec))
        return result
