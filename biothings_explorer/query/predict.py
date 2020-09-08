import pandas as pd

from .utils import *
from ..smartapi_kg import MetaKG
from ..call_apis import APIQueryDispatcher


class Predict:
    def __init__(self, input_objs, intermediate_nodes, output_types, config=None):
        self.input_objs = input_objs
        self.intermediate_nodes = intermediate_nodes
        if isinstance(intermediate_nodes, str):
            intermediate_nodes = [intermediate_nodes]
        if isinstance(intermediate_nodes, list) and len(intermediate_nodes) > 2:
            print(
                "Max number of intermediate nodes is 2. You specify {}. Please refine your query".format(
                    len(intermediate_nodes)
                )
            )
        self.output_types = output_types
        self.intermediate_nodes.append(self.output_types)
        self.steps_results = {}
        self.steps_nodes = {}
        self.kg = MetaKG()
        self.kg.constructMetaKG(source="local")
        self.query_completes = False
        self.config = config

    def connect(self, filter=None, verbose=True):
        if (
            isinstance(self.intermediate_nodes, list)
            and len(self.intermediate_nodes) > 3
        ):
            print(
                "Max number of intermediate nodes is 2. You specify {}. We can not proceed your query. Please refine your query".format(
                    len(self.intermediate_nodes) - 1
                )
            )
            return
        self.query_completes = False
        inputs = restructureHintOutput(self.input_objs)
        if verbose:
            print(
                "==========\n========== QUERY PARAMETER SUMMARY ==========\n==========\n"
            )
            print(
                "Your query have {} input nodes {}. And BTE will find paths that connect your input nodes to your output types {}. Paths will contain {} intermediate nodes.\n".format(
                    len(inputs),
                    ",".join([item["id"]["label"] for item in inputs.values()]),
                    self.intermediate_nodes[-1],
                    len(self.intermediate_nodes) - 1,
                )
            )
            for i, node in enumerate(self.intermediate_nodes[0:-1]):
                print(
                    "Intermediate node #{} will have these type constraints: {}".format(
                        i + 1, node
                    )
                )
        for i, node in enumerate(self.intermediate_nodes):
            if verbose:
                print("\n========== Query # {} ==========\n".format(i + 1))
                print("==== Step #1: Query Path Planning ====\n")
            inputs = groupsIDsbySemanticType(inputs)
            if (
                self.config.get("predicates")
                and isinstance(self.config["predicates"], list)
                and i < len(self.config["predicates"])
            ):
                predicates = self.config["predicates"][i]
            else:
                predicates = None
            edges = getEdges(inputs, node, predicates, self.kg)
            if len(edges) > 0:
                annotatedEdges = []
                for e in edges:
                    annotatedEdges += annotateEdgesWithInput(
                        e.get("edges"), e.get("inputs")
                    )
            else:
                print(
                    "No APIs found to perform Query # {}. Your query ends.".format(
                        i + 1
                    )
                )
                return
            if annotatedEdges:
                if (
                    self.config.get("filters")
                    and isinstance(self.config["filters"], list)
                    and i < len(self.config["filters"])
                ):
                    for edge in annotatedEdges:
                        edge["filter"] = self.config["filters"][i]
                dp = APIQueryDispatcher(annotatedEdges, verbose=verbose)
                self.steps_results[i] = dp.syncQuery()
                if not self.steps_results[i] or len(self.steps_results[i]) == 0:
                    print(
                        "Unfortunately, no results were found for Query # {}. Your query fails. Please try refine your query".format(
                            i + 1
                        )
                    )
                    return
                inputs = self.steps_nodes[i] = extractAllResolvedOutputIDs(
                    self.steps_results[i]
                )
                print(
                    "After id-to-object translation, BTE retrieved {} unique outputs".format(
                        len(inputs)
                    )
                )
            else:
                print(
                    "No APIs found to perform the query in step {}. Your query ends.".format(
                        i + 1
                    )
                )
                return
        self.query_completes = True
        if verbose:
            print(
                "\n==========\n========== Final assembly of results ==========\n==========\n"
            )
            for k, j in self.steps_nodes.items():
                print(
                    "In the #{} query, BTE found {} unique nodes.".format(k + 1, len(j))
                )

    def display_table_view(self):
        if not self.query_completes:
            print("Your query fails. Unable to display results!")
            return

        for step, step_result in self.steps_results.items():
            df = stepResult2PandasTable(step_result, step, len(self.steps_results))
            if step == 0:
                result = df
                continue
            join_columns = [
                "node" + str(step) + item for item in ["_id", "_type", "_label"]
            ]
            result = pd.merge(result, df, on=join_columns, how="inner")
        return result
