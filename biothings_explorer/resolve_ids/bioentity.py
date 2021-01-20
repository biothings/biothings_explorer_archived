from ..config_new import ID_RESOLVING_APIS
from ..utils.common import getCurieFromVal


class BioEntity:
    def __init__(self, semantic_type, id_dict):
        self._semantic_type = semantic_type
        self._id_dict = id_dict

    def __repr__(self):
        return self._id_dict

    def get_primary_id(self):
        ranks = ID_RESOLVING_APIS.get(self._semantic_type, {}).get("id_ranks")
        for prefix in ranks:
            if self._id_dict.get(prefix):
                return getCurieFromVal(self._id_dict.get(prefix)[0], prefix)
        return None

    def get_label(self):
        if self._id_dict.get("SYMBOL"):
            return self._id_dict["SYMBOL"][0]
        if self._id_dict.get("name"):
            return self._id_dict["name"][0]
        return self.get_primary_id()

    def get_curies(self):
        res = []
        for prefix, ids in self._id_dict.items():
            for _id in ids:
                res.append(getCurieFromVal(_id, prefix))
        return res
