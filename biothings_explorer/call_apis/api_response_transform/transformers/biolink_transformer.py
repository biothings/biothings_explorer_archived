from .base_transformer import BaseTransformer


class BioLinkTransformer(BaseTransformer):
    def wrap(self, res):
        """ restructure API response from biolink API before extracting data

        parameters
        ----------
        json_doc: the API response from biolink API

        notes: list of prefixes used in biolink API for different semantic types

            * ANATOMY: UBERON, CL, FBbt
            * DISEASE: MONDO
            * GENE: HGNC, NCBIGene, MGI， ZFIN，FlyBase
            * PHENOTYPE: EFO, HP, MONDO
        """
        if res and "associations" in res:
            for _doc in res["associations"]:
                # remove prefix
                if "object" in _doc and "id" in _doc["object"]:
                    object_id = _doc["object"]["id"]
                    try:
                        prefix, value = object_id.split(":")
                        # these IDs have prefix by nature
                        if prefix in ["HGNC", "NCBIGene", "REACT", "dbSNP"]:
                            _doc["object"][prefix] = value
                        else:
                            _doc["object"][prefix] = object_id
                    except ValueError:
                        pass
                # remove empty value
                if "publications" not in _doc:
                    continue
                if not _doc.get("publications"):
                    _doc.pop("publications")
                elif not _doc["publications"][0]["id"].startswith("PMID"):
                    _doc.pop("publications")
                else:
                    for _item in _doc["publications"]:
                        if _item["id"].startswith("PMID"):
                            _item["id"] = _item["id"].split(":")[-1]
                        else:
                            _item.pop("id")
                if not _doc["provided_by"]:
                    _doc.pop("provided_by")
                else:
                    if not isinstance(_doc["provided_by"], list):
                        _doc["provided_by"] = [_doc["provided_by"]]
                    source_list = []
                    for item in _doc["provided_by"]:
                        if item.startswith("https://data.monarchinitiative.org/ttl"):
                            source_name = item.split("/")[-1].strip(".nt")
                            source_list.append(source_name)
                        else:
                            source_name = item.split("/")[-1].strip("#")
                            source_list.append(source_name)
                    _doc["provided_by"] = source_list
        return res
