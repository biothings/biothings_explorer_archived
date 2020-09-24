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
        self.saved = {
            "ENSG00000142149-CHEMBL185": {"pair": 0.0, "alone": 0.4482},
            "ENSG00000118058-CHEMBL83": {
                "pair": 0.3684210526315789,
                "alone": 0.5384615384615384,
            },
            "ENSG00000153922-CHEMBL83": {
                "pair": 0.4666666666666666,
                "alone": 0.5384615384615384,
            },
            "ENSG00000125414-CHEMBL83": {
                "pair": 0.5384615384615384,
                "alone": 0.5384615384615384,
            },
            "ENSG00000105429-CHEMBL34259": {
                "pair": 0.2903225806451613,
                "alone": 0.4285714285714286,
            },
            "ENSG00000134121-CHEMBL888": {"pair": 1, "alone": 1},
            "ENSG00000007174-CHEMBL554": {"pair": 1, "alone": 1},
            "ENSG00000075275-CHEMBL83": {"pair": 0.4375, "alone": 0.5384615384615384},
            "ENSG00000041982-CHEMBL53463": {
                "pair": 0.604651162790697,
                "alone": 0.6046511627906976,
            },
            "ENSG00000144229-CHEMBL554": {"pair": 1, "alone": 1},
            "ENSG00000171560-CHEMBL83": {
                "pair": 0.22580645161290325,
                "alone": 0.5384615384615384,
            },
            "ENSG00000138759-CHEMBL83": {
                "pair": 0.5384615384615384,
                "alone": 0.5384615384615384,
            },
            "ENSG00000206384-CHEMBL92": {"pair": 0.40625, "alone": 0.40625},
            "ENSG00000187908-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000283649-CHEMBL185": {"pair": 0.0, "alone": 0.4482758620689655},
            "ENSG00000283649-CHEMBL92": {"pair": 0.0, "alone": 0.40625},
            "ENSG00000179399-CHEMBL34259": {
                "pair": 0.4285714285714286,
                "alone": 0.4285714285714286,
            },
            "ENSG00000107611-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000168702-CHEMBL83": {
                "pair": 0.48275862068965514,
                "alone": 0.5384615384615384,
            },
            "ENSG00000187775-CHEMBL185": {
                "pair": 0.4982578397212544,
                "alone": 0.4482758620689655,
            },
            "ENSG00000274161-CHEMBL34259": {"pair": 0.0, "alone": 0.4285714285714286},
            "ENSG00000147133-CHEMBL53463": {
                "pair": 0.6408450704225351,
                "alone": 0.6046511627906976,
            },
            "ENSG00000147133-CHEMBL888": {"pair": 1.0, "alone": 1.0},
            "ENSG00000159450-CHEMBL888": {"pair": 1.0, "alone": 1.0},
            "ENSG00000159289-CHEMBL53463": {"pair": 1.0, "alone": 0.6046511627906976},
            "ENSG00000159289-CHEMBL888": {"pair": 1.0, "alone": 1.0},
            "ENSG00000074054-CHEMBL34259": {
                "pair": 0.4285714285714286,
                "alone": 0.4285714285714286,
            },
            "ENSG00000108557-CHEMBL92": {"pair": 0.5064935064935064, "alone": 0.40625},
            "ENSG00000164754-CHEMBL888": {"pair": 1.0, "alone": 1.0},
            "ENSG00000136231-CHEMBL185": {"pair": 0.0, "alone": 0.4482758620689655},
            "ENSG00000112144-CHEMBL53463": {
                "pair": 0.7536231884057971,
                "alone": 0.6046511627906976,
            },
            "ENSG00000282607-CHEMBL888": {"pair": 0.0, "alone": 1.0},
            "ENSG00000149294-CHEMBL92": {"pair": 1.0, "alone": 0.40625},
            "ENSG00000103546-CHEMBL34259": {"pair": 0.0, "alone": 0.4285714285714286},
            "ENSG00000197479-CHEMBL888": {"pair": 1.0, "alone": 1.0},
            "ENSG00000162711-CHEMBL53463": {
                "pair": 0.6046511627906976,
                "alone": 0.6046511627906976,
            },
            "ENSG00000162711-CHEMBL83": {
                "pair": 0.5384615384615384,
                "alone": 0.5384615384615384,
            },
            "ENSG00000163655-CHEMBL83": {"pair": 0.0, "alone": 0.5384615384615384},
            "ENSG00000119042-CHEMBL185": {
                "pair": 0.35135135135135137,
                "alone": 0.4482758620689655,
            },
            "ENSG00000133863-CHEMBL83": {"pair": 0.7, "alone": 0.5384615384615384},
            "ENSG00000112983-CHEMBL185": {
                "pair": 0.4482758620689655,
                "alone": 0.4482758620689655,
            },
            "ENSG00000150630-CHEMBL185": {"pair": 1.0, "alone": 0.4482758620689655},
            "ENSG00000273079-CHEMBL34259": {"pair": 0.2, "alone": 0.4285714285714286},
            "ENSG00000115355-CHEMBL83": {
                "pair": 0.5384615384615384,
                "alone": 0.5384615384615384,
            },
            "ENSG00000161040-CHEMBL83": {
                "pair": 0.6363636363636364,
                "alone": 0.5384615384615384,
            },
            "ENSG00000146592-CHEMBL92": {"pair": 0.6724137931034483, "alone": 0.40625},
            "ENSG00000001629-CHEMBL83": {"pair": 0.0, "alone": 0.5384615384615384},
            "ENSG00000251692-CHEMBL185": {"pair": 1.0, "alone": 0.4482758620689655},
            "ENSG00000198838-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000080603-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000138778-CHEMBL34259": {"pair": 0.5, "alone": 0.4285714285714286},
            "ENSG00000135837-CHEMBL185": {
                "pair": 0.30708661417322836,
                "alone": 0.4482758620689655,
            },
            "ENSG00000155085-CHEMBL185": {
                "pair": 0.5321637426900585,
                "alone": 0.4482758620689655,
            },
            "ENSG00000155085-CHEMBL34259": {
                "pair": 0.5121951219512195,
                "alone": 0.4285714285714286,
            },
            "ENSG00000151067-CHEMBL83": {
                "pair": 0.6202531645569621,
                "alone": 0.5384615384615384,
            },
            "ENSG00000147724-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000197321-CHEMBL83": {
                "pair": 0.608695652173913,
                "alone": 0.5384615384615384,
            },
            "ENSG00000119397-CHEMBL83": {"pair": 0.4375, "alone": 0.5384615384615384},
            "ENSG00000114487-CHEMBL34259": {
                "pair": 0.48387096774193544,
                "alone": 0.4285714285714286,
            },
            "ENSG00000101333-CHEMBL554": {"pair": 1.0, "alone": 1.0},
            "ENSG00000153993-CHEMBL92": {"pair": 0.5777777777777778, "alone": 0.40625},
            "ENSG00000150627-CHEMBL83": {
                "pair": 0.6712328767123288,
                "alone": 0.5384615384615384,
            },
            "ENSG00000173769-CHEMBL83": {
                "pair": 0.6363636363636365,
                "alone": 0.5384615384615384,
            },
            "ENSG00000196535-CHEMBL83": {
                "pair": 0.608695652173913,
                "alone": 0.5384615384615384,
            },
            "ENSG00000143297-CHEMBL34259": {"pair": 0.5, "alone": 0.4285714285714286},
            "ENSG00000196074-CHEMBL83": {"pair": 0.25, "alone": 0.5384615384615384},
            "ENSG00000114423-CHEMBL83": {
                "pair": 0.5932203389830509,
                "alone": 0.5384615384615384,
            },
            "ENSG00000130559-CHEMBL83": {"pair": 0.7, "alone": 0.5384615384615384},
            "ENSG00000132837-CHEMBL34259": {"pair": 0.375, "alone": 0.4285714285714286},
            "ENSG00000183023-CHEMBL34259": {
                "pair": 0.7894736842105264,
                "alone": 0.4285714285714286,
            },
            "ENSG00000106714-CHEMBL53463": {
                "pair": 0.6046511627906976,
                "alone": 0.6046511627906976,
            },
            "ENSG00000172037-CHEMBL83": {
                "pair": 0.5932203389830509,
                "alone": 0.5384615384615384,
            },
            "ENSG00000100241-CHEMBL83": {
                "pair": 0.5384615384615384,
                "alone": 0.5384615384615384,
            },
            "ENSG00000133138-CHEMBL83": {
                "pair": 0.43750000000000006,
                "alone": 0.5384615384615384,
            },
            "ENSG00000072315-CHEMBL185": {
                "pair": 0.5321637426900585,
                "alone": 0.4482758620689655,
            },
            "ENSG00000139220-CHEMBL34259": {"pair": 0.5, "alone": 0.4285714285714286},
            "ENSG00000184313-CHEMBL34259": {
                "pair": 0.36000000000000004,
                "alone": 0.4285714285714286,
            },
            "ENSG00000139618-CHEMBL553025": {"pair": 0.0, "alone": 0.33333333333333337},
            "ENSG00000039068-CHEMBL185": {
                "pair": 0.6666666666666666,
                "alone": 0.5517241379310345,
            },
            "ENSG00000170558-CHEMBL185": {"pair": 0.0, "alone": 0.5517241379310345},
            "ENSG00000005810-CHEMBL53463": {"pair": 1.0, "alone": 0.3953488372093023},
            "ENSG00000005810-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000071894-CHEMBL53463": {
                "pair": 0.6666666666666666,
                "alone": 0.3953488372093023,
            },
            "ENSG00000071894-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000132470-CHEMBL185": {"pair": -1, "alone": 0.5517241379310345},
            "ENSG00000134982-CHEMBL553025": {"pair": -1, "alone": 0.33333333333333337},
            "ENSG00000134982-CHEMBL185": {"pair": 0.5, "alone": 0.5517241379310345},
            "ENSG00000178568-CHEMBL53463": {"pair": 0.0, "alone": 0.3953488372093023},
            "ENSG00000178568-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000124126-CHEMBL34259": {"pair": 0.0, "alone": 0.5714285714285714},
            "ENSG00000124126-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000181143-CHEMBL553025": {"pair": -1, "alone": 0.33333333333333337},
            "ENSG00000163659-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000066468-CHEMBL34259": {"pair": -1, "alone": 0.5714285714285714},
            "ENSG00000066468-CHEMBL92": {"pair": 0.5, "alone": 0.5937499999999999},
            "ENSG00000074181-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000188158-CHEMBL83": {"pair": 0.0, "alone": 0.4615384615384615},
            "ENSG00000188158-CHEMBL553025": {"pair": 0.0, "alone": 0.33333333333333337},
            "ENSG00000128512-CHEMBL185": {"pair": -1, "alone": 0.5517241379310345},
            "ENSG00000105877-CHEMBL34259": {"pair": -1, "alone": 0.5714285714285714},
            "ENSG00000105877-CHEMBL53463": {"pair": 0.625, "alone": 0.3953488372093023},
            "ENSG00000145242-CHEMBL888": {"pair": 0.0, "alone": 0.0},
            "ENSG00000141867-CHEMBL185": {"pair": -1, "alone": 0.5517241379310345},
            "ENSG00000138119-CHEMBL185": {"pair": 1.0, "alone": 0.5517241379310345},
            "ENSG00000117713-CHEMBL83": {
                "pair": 0.45454545454545453,
                "alone": 0.4615384615384615,
            },
            "ENSG00000168769-CHEMBL185": {"pair": -1, "alone": 0.5517241379310345},
            "ENSG00000184384-CHEMBL553025": {"pair": 0.0, "alone": 0.33333333333333337},
        }
        self.saved_drug_alone = {}

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
        if not ensembl:
            query = self.buildQuery(genes=[], drugs=[("BBB", "CHEMBL:" + chembl)],)
        else:
            query = self.buildQuery(
                genes=[("AAA", "ENSEMBL:" + ensembl)],
                drugs=[("BBB", "CHEMBL:" + chembl)],
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
        cnt = 0
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
            pair = ensembl + "-" + chembl
            if pair in self.saved:
                if self.saved[pair]["pair"] != 0.0:
                    rec["$survival_prob_change"] = (
                        self.saved[pair]["pair"] - self.saved[pair]["alone"]
                    ) / self.saved[pair]["alone"]
                    cnt += 1
                else:
                    rec["$survival_prob_change"] = 0
                    cnt += 1
                continue
            # query1 = self.queryOnePair(ensembl, chembl)
            # rec["$survival_probability"] = query1
            # if chembl in self.saved_drug_alone:
            #     query2 = self.saved_drug_alone[chembl]
            # else:
            #     query2 = self.queryOnePair(None, chembl)
            #     self.saved_drug_alone[chembl] = query2
            # self.saved[pair] = {"pair": query1, "alone": query2}
            # if self.saved[pair]["pair"] != 0.0:
            #     rec["$survival_prob_change"] = (
            #         self.saved[pair]["pair"] - self.saved[pair]["alone"]
            #     ) / self.saved[pair]["alone"]
            #     cnt += 1
        if cnt > 0:
            print(
                "Number of output edges sent to Connection Hypothesis KP for scoring is {}. Number of output edges annotated is {}".format(
                    len(self.stepResult), cnt
                )
            )
        return

    def filter(self):
        return
