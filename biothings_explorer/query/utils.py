from collections import defaultdict
from copy import deepcopy
import pandas as pd

from ..config_new import ALWAYS_PREFIXED
from ..smartapi_kg import MetaKG


def id2curie(prefix, val):
    if prefix in ALWAYS_PREFIXED:
        return val
    return prefix + ":" + val


def annotateEdgesWithInput(edges, inputs):
    if isinstance(inputs, dict):
        inputs = [inputs]
    annotatedEdges = []
    for edge in edges:
        if edge["query_operation"].get("supportBatch"):
            copy_edge = deepcopy(edge)
            input_ids = set()
            original_input = {}
            for _input in inputs:
                prefix = copy_edge["association"]["input_id"]
                if prefix in _input["db_ids"]:
                    for val in _input["db_ids"][prefix]:
                        input_ids.add(val)
                        original_input[id2curie(prefix, val)] = _input
            input_ids = list(input_ids)
            for i in range(0, len(input_ids), 1000):
                copy_edge["input"] = input_ids[i : i + 1000]
                copy_edge["original_input"] = original_input
                annotatedEdges.append(copy_edge)
        else:
            for _input in inputs:
                prefix = edge["association"]["input_id"]
                if prefix in _input["db_ids"]:
                    if not isinstance(_input["db_ids"][prefix], list):
                        _input["db_ids"][prefix] = [_input["db_ids"][prefix]]
                    for _id in _input["db_ids"][prefix]:
                        copy_edge = deepcopy(edge)
                        copy_edge["input"] = _id
                        copy_edge["original_input"] = {id2curie(prefix, _id): _input}
                        annotatedEdges.append(copy_edge)
    return annotatedEdges


def getEdges(inputs, outputs, predicates, knowledgegraph=None):
    result = []
    if not knowledgegraph:
        kg = MetaKG()
        kg.constructMetaKG(source="local")
    else:
        kg = knowledgegraph
    for semantic_type, ids in inputs.items():
        edges = kg.filter(
            {
                "input_type": semantic_type,
                "output_type": outputs,
                "predicate": predicates,
            }
        )
        if not edges or not ids:
            continue
        result.append({"edges": edges, "inputs": ids})
    return result


def extractAllResolvedOutputIDs(res):
    output_ids = {}
    if res and len(res) > 0:
        for item in res:
            if "resolved_ids" in item["$output_id_mapping"]:
                output_ids[
                    item["$output_id_mapping"]["resolved_ids"]["id"]["identifier"]
                ] = item["$output_id_mapping"]["resolved_ids"]
    return output_ids


def groupsIDsbySemanticType(output_ids):
    result = defaultdict(list)
    for resolved_ids in output_ids.values():
        result[resolved_ids.get("type")].append(resolved_ids)
    return result


def restructureHintOutput(outputs):
    result = {}
    for output in outputs:
        copy_output = deepcopy(output)
        output_id = {}
        for k, v in copy_output.items():
            if k not in ["primary", "type"] and not isinstance(v, list):
                copy_output[k] = [v]
        if copy_output["primary"]["identifier"] in ALWAYS_PREFIXED:
            curie = copy_output["primary"]["value"]
        else:
            curie = (
                copy_output["primary"]["identifier"]
                + ":"
                + copy_output["primary"]["value"]
            )
        if "name" in copy_output:
            output_id["label"] = copy_output["name"][0]
        else:
            output_id["label"] = curie
        output_id["identifier"] = curie
        copy_output.pop("display")
        copy_output.pop("primary")
        result.update(
            {
                curie: {
                    "type": copy_output.pop("type"),
                    "db_ids": copy_output,
                    "id": output_id,
                }
            }
        )
    return result


def stepResult2PandasTable(result, step, total_steps):
    if step == 0:
        node1 = "input"
    else:
        node1 = "node" + str(step)
    if step == total_steps - 1:
        node2 = "output"
    else:
        node2 = "node" + str(step + 1)
    if isinstance(result, list) and len(result) > 1:
        table_dict = []
        for rec in result:
            table_dict.append(
                {
                    node1
                    + "_id": rec["$original_input"][rec["$input"]]["id"]["identifier"],
                    node1
                    + "_label": rec["$original_input"][rec["$input"]]["id"]["label"],
                    node1 + "_type": rec["$original_input"][rec["$input"]]["type"],
                    "pred" + str(step + 1): rec["$association"]["predicate"],
                    "pred" + str(step + 1) + "_source": ",".join(rec.get("provided_by"))
                    if rec.get("provided_by") != [None]
                    else None,
                    "pred" + str(step + 1) + "_api": rec.get("api"),
                    "pred"
                    + str(step + 1)
                    + "_publications": ",".join(rec.get("publications"))
                    if rec.get("publications")
                    else None,
                    node2
                    + "_id": rec["$output_id_mapping"]["resolved_ids"]["id"][
                        "identifier"
                    ],
                    node2
                    + "_label": rec["$output_id_mapping"]["resolved_ids"]["id"][
                        "label"
                    ],
                    node2 + "_type": rec["$output_id_mapping"]["resolved_ids"]["type"],
                    node2 + "_degree": rec.get("$nodeDegree"),
                }
            )
        return pd.DataFrame(table_dict)
