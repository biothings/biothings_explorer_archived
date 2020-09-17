import requests
import json

ACCEPTED_CHEMBL_LIST = [
    "CHEMBL1201247",
    "CHEMBL88",
    "CHEMBL53463",
    "CHEMBL1201585",
    "CHEMBL1201585",
    "CHEMBL1351",
    "CHEMBL3545252",
    "CHEMBL185",
    "CHEMBL83",
    "CHEMBL1444",
    "CHEMBL53463",
    "CHEMBL88",
    "CHEMBL306601",
    "CHEMBL1399",
    "CHEMBL1200374",
    "CHEMBL888",
    "CHEMBL92",
    "CHEMBL1773",
    "CHEMBL1399",
    "CHEMBL924",
    "CHEMBL888",
    "CHEMBL428647",
    "CHEMBL428647",
    "CHEMBL1237023",
    "CHEMBL1358",
    "CHEMBL924",
    "CHEMBL1200775",
    "CHEMBL554",
    "CHEMBL1444",
    "CHEMBL1200374",
    "CHEMBL1201247",
    "CHEMBL1201583",
    "CHEMBL417",
    "CHEMBL34259",
    "CHEMBL553025",
    "CHEMBL676",
    "CHEMBL1201583",
    "CHEMBL1201334",
    "CHEMBL1200796",
    "CHEMBL1520188",
    "CHEMBL1358",
    "CHEMBL1201568",
]


class HypothesisFilter:
    def __init__(self, stepResult, criteria):
        self.stepResult = stepResult
        self.criteria = criteria

    @staticmethod
    def buildQuery(genes=[], drugs=[]):

        # empty response
        reasoner_std = {"query_graph": dict()}

        # empty query graph
        reasoner_std["query_graph"] = {"edges": [], "nodes": []}

        node_count = 0
        edge_count = 0

        # add genes
        for gene in genes:
            reasoner_std["query_graph"]["nodes"].append(
                {
                    "id": "n{}".format(node_count),
                    "type": "Gene",
                    "curie": "{}".format(gene[1]),
                }
            )
            node_count += 1

        # add drugs
        for drug in drugs:
            reasoner_std["query_graph"]["nodes"].append(
                {
                    "id": "n{}".format(node_count),
                    "type": "Drug",
                    "curie": "{}".format(drug[1]),
                }
            )
            node_count += 1

        # add in disease node
        disease = ("Breast_Cancer", "MONDO:0007254")
        reasoner_std["query_graph"]["nodes"].append(
            {
                "id": "n{}".format(node_count),
                "type": "disease",
                "curie": "{}".format(disease[1]),
            }
        )
        node_count += 1

        # link all evidence to disease
        for node in reasoner_std["query_graph"]["nodes"]:
            if node["type"] == "Gene":
                id = node["id"]
                reasoner_std["query_graph"]["edges"].append(
                    {
                        "id": "e{}".format(edge_count),
                        "type": "gene_to_disease_association",
                        "source_id": "{}".format(id),
                        "target_id": "n{}".format(node_count - 1),
                    }
                )
                edge_count += 1
            elif node["type"] == "Drug":
                id = node["id"]
                reasoner_std["query_graph"]["edges"].append(
                    {
                        "id": "e{}".format(edge_count),
                        "type": "chemical_to_disease_or_phenotypic_feature_association",
                        "source_id": "{}".format(id),
                        "target_id": "n{}".format(node_count - 1),
                    }
                )
                edge_count += 1

        # add target survival node
        phenotype = ("Survival_Time", "EFO:0000714")
        reasoner_std["query_graph"]["nodes"].append(
            {
                "id": "n{}".format(node_count),
                "type": "PhenotypicFeature",
                "curie": "{}".format(phenotype[1]),
            }
        )
        node_count += 1

        # link disease to target
        reasoner_std["query_graph"]["edges"].append(
            {
                "id": "e{}".format(edge_count),
                "type": "disease_to_phenotype_association",
                "value": 970,
                "source_id": "n{}".format(node_count - 2),
                "target_id": "n{}".format(node_count - 1),
            }
        )
        return reasoner_std

    def queryOnePair(self, ensembl, chembl):
        query = self.buildQuery(
            genes=[("AAA", "ENSEMBL:" + ensembl)], drugs=[("BBB", "CHEMBL:" + chembl)]
        )
        query["reasoner_id"] = "exploring"
        payload = {"query": query}
        try:
            p_survival = 0.0
            r = requests.post(
                "http://chp.thayer.dartmouth.edu/submitQuery/", json=payload
            )
            chp_res = json.loads(r.content)
            for edge in chp_res["knowledge_graph"]["edges"]:
                if edge["type"] == "disease_to_phenotype_association":
                    p_survival = edge["has_confidence_level"]
            return p_survival
        except json.JSONDecodeError:
            return 0.0

    def annotate(self):
        """
        Add node degree info to each edge.
        :param stepResult: a list of returned result from query.
        """
        if not self.stepResult:
            return
        for rec in self.stepResult:
            if "ENSEMBL" in rec["$original_input"][rec["$input"]]["db_ids"]:
                ensembl = rec["$original_input"][rec["$input"]]["db_ids"]["ENSEMBL"][0]
            else:
                rec["$survival_probability"] = 0
                continue
            if "CHEMBL.COMPOUND" in rec["$output_id_mapping"]["resolved_ids"]["db_ids"]:
                intersect = set(
                    rec["$output_id_mapping"]["resolved_ids"]["db_ids"][
                        "CHEMBL.COMPOUND"
                    ]
                ).intersection(set(ACCEPTED_CHEMBL_LIST))
                if len(intersect) > 0:
                    chembl = list(intersect)[0]
                else:
                    rec["$survival_probability"] = 0
                    continue
            else:
                rec["$survival_probability"] = 0
                continue
            print("found one pair", ensembl, chembl)
            query = self.queryOnePair(ensembl, chembl)
            print("probability", query)
            rec["$survival_probability"] = query
        return

    def filter(self):
        return
