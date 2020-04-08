"""Generate a json file containing semmed relationships

The python script takes two arguments:
1. DATA_FOLDER: the folder storing neo4j_nodes.csv and neo4j_edges.csv files
2. OUTPUT_FILE_PATH: the file path storing the output
"""
from collections import defaultdict
import csv
import os
import sys
import json

maxInt = sys.maxsize


SEMMED_SEMANTIC_TYPE_MAPPING = {
    "chemical_substance": "ChemicalSubstance",
    "activity_and_behavior": None,
    "anatomical_entity": "AnatomicalEntity",
    "biological_entity": None,
    "biological_process_or_activity": "BiologicalProcess",
    "cell": "Cell",
    "cell_component": "CellularComponent",
    "disease_or_phenotypic_feature": "DiseaseOrPhenotypicFeature",
    "gene": "Gene",
    "genomic_entity": None,
    "gross_anatomical_structure": None,
    "phenotypic_feature": "PhenotypicFeature",
    "protein": "Gene"
}
SEMMED_PRED_MAPPING = {
    "ASSOCIATED_WITH": {
        "self": "related_to",
        "reverse": "related_to"
    },
    "INTERACTS_WITH": {
        "self": "physically_interacts_with",
        "reverse": "physically_interacts_with"
    },
    "AFFECTS": {
        "self": "affects",
        "reverse": "affected_by"
    },
    "STIMULATES": {
        "self": "positively_regulates",
        "reverse": "positively_regulated_by"
    },
    "INHIBITS": {
        "self": "negatively_regulates",
        "reverse": "negatively_regulated_by"
    },
    "DISRUPTS": {
        "self": "disrupts",
        "reverse": "disrupted_by"
    },
    "COEXISTS_WITH": {
        "self": "coexists_with",
        "reverse": "coexists_with"
    },
    "PREDISPOSES": {
        "self": "predisposes",
        "reverse": "predisposed_by"
    },
    "CAUSES": {
        "self": "causes",
        "reverse": "caused_by"
    },
    "TREATS": {
        "self": "treats",
        "reverse": "treated_by"
    },
    "PREVENTS": {
        "self": "prevents",
        "reverse": "prevented_by"
    },
    "OCCURS_IN": {
        "self": "occurs_in",
        "reverse": "in_which_occured"
    },
    "PROCESS_OF": {
        "self": "occurs_in",
        "reverse": "in_which_occured"
    },
    "LOCATION_OF": {
        "self": "location_of",
        "reverse": "located_in"
    },
    "PART_OF": {
        "self": "part_of",
        "reverse": "has_part"
    },
    "USES": {
        "self": "has_input",
        "reverse": "is_input_of"
    },
    "CONVERTS_TO": {
        "self": "derives_info",
        "reverse": "derives_from"
    },
    "MANIFESTATION_OF": {
        "self": "manifestation_of",
        "reverse": "manifested_by"
    },
    "PRODUCES": {
        "self": "produces",
        "reverse": "produced_by",
    },
    "PRECEDES": {
        "self": "precedes",
        "reverse": "preceded_by"
    },
    "ISA": {
        "self": "subclass_of",
        "reverse": "has_subclass"
    }
}

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def load_data(data_folder):
    edges_dict = {v: defaultdict(set) for k, v in SEMMED_SEMANTIC_TYPE_MAPPING.items() if v != None}
    nodes_path = os.path.join(data_folder, "nodes_neo4j.csv")
    edges_path = os.path.join(data_folder, "edges_neo4j.csv")
    group_by_semmantic_dict = defaultdict(list)
    id_type_mapping = {}
    with open(nodes_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            group_by_semmantic_dict[_item[-2]].append(_item[-1])
            id_type_mapping[_item[-1]] = {'type': _item[-2], 'name': _item[1]}
    gene_related = {}
    with open(edges_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            source_type = SEMMED_SEMANTIC_TYPE_MAPPING[id_type_mapping[_item[4]]['type']]
            pred = SEMMED_PRED_MAPPING[_item[0]]['self']
            pred_reverse = SEMMED_PRED_MAPPING[_item[0]]['reverse']
            target_type = SEMMED_SEMANTIC_TYPE_MAPPING[id_type_mapping[_item[5]]['type']]
            if source_type in edges_dict and target_type in edges_dict:
                edges_dict[source_type][pred].add(target_type)
                edges_dict[target_type][pred_reverse].add(source_type)
    for k, v in edges_dict.items():
        for m, n in v.items():
             v[m] = list(n)
    return dict(edges_dict)


if __name__ == '__main__':
    DATA_FOLDER = sys.argv[1]
    print("DATA_FOLDER", DATA_FOLDER)
    OUTPUT_FILE_PATH = sys.argv[2]
    print("OUTPUT_FILE_PATH", OUTPUT_FILE_PATH)

    a = load_data(DATA_FOLDER)
    with open(OUTPUT_FILE_PATH, 'w') as outfile:
        json.dump(a, outfile, indent=4, sort_keys=True)
