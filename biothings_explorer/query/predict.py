import pandas as pd

from .utils import *
from ..smartapi_kg import MetaKG
from ..call_apis import APIQueryDispatcher
from ..config_new import BTE_FILTERS
from .filter.nodeDegree import NodeDegreeFilter
from .filter import Filter
from ..expand import Expander
from .printer import Print


class Predict:
    def __init__(self, input_objs, intermediate_nodes, output_types, config=None):
        self.input_objs = input_objs
        self.intermediate_nodes = intermediate_nodes
        if isinstance(intermediate_nodes, str):
            intermediate_nodes = [intermediate_nodes]
        self.output_types = output_types
        self.intermediate_nodes.append(self.output_types)
        validate_max_intermediate_nodes(self.intermediate_nodes)
        self.steps_results = {}
        self.steps_nodes = {}
        self.kg = MetaKG()
        self.kg.constructMetaKG(source="local")
        self.query_completes = False
        self.config = config
        self.ep = Expander()
        self.pt = Print()

    def _expand_inputs(self, inputs, verbose=True):
        """
        Expand inputs to its descendants.
        :param inputs: list of input bioentities with resolved ids.
        :param verbose: verbose
        """
        if (
            self.config
            and self.config.get("expand")
            and self.config.get("expand") is True
        ):
            if verbose:
                self.pt.print_expand_begin_message()
            expandedInputs = self.ep.expand(inputs.values())
            if verbose:
                self.pt.print_expand_summary_message(expandedInputs)
            if expandedInputs:
                inputs.update(expandedInputs)
        return inputs

    def _annotate_edges_with_filters(self, edges, step):
        """
        Add filter information to each edge.
        :param edges: list of edges.
        """
        if (
            self.config
            and self.config.get("filters")
            and isinstance(self.config["filters"], list)
            and step < len(self.config["filters"])
            and isinstance(self.config["filters"][step], dict)
            and self.config["filters"][step]
        ):
            if len(set(self.config["filters"][step].keys()) - set(BTE_FILTERS)) == 0:
                return
            for edge in edges:
                output_nodes = self.intermediate_nodes[step]
                if isinstance(output_nodes, str):
                    edge["filter"] = self.config["filters"][step]
                if isinstance(output_nodes, list):
                    for i, node in enumerate(output_nodes):
                        if node == edge["association"]["output_type"]:
                            if isinstance(self.config["filters"][step], list):
                                edge["filter"] = self.config["filters"][step][i]
                            else:
                                edge["filter"] = self.config["filters"][step]

    def _get_predicates_from_config(self, path):
        """
        Get information on predicates from config.
        """
        if (
            self.config
            and self.config.get("predicates")
            and isinstance(self.config["predicates"], list)
            and path < len(self.config["predicates"])
        ):
            predicates = self.config["predicates"][path]
        else:
            predicates = None
        return predicates

    def _annotate_results(self, step, source_types):
        # print("annotating results with NodeDegree!")
        # ft = NodeDegreeFilter(self.steps_results[step], {})
        # ft.annotateNodeDegree()
        # self.steps_results[step] = ft.stepResult
        if "annotate" in self.config and isinstance(self.config["annotate"], list):
            ft = Filter(self.steps_results[step], self.config["annotate"], source_types)
            ft.annotate()
            self.steps_results[step] = ft.stepResult
            return ft
        return None

    def _filter_results(self, step, ft=None):
        if (
            self.config
            and self.config.get("filters")
            and step < len(self.config["filters"])
        ):
            if not ft:
                ft = Filter(self.steps_results[step], self.config["filters"][step])
            else:
                ft.criteria = self.config["filters"][step]
            self.steps_results[step] = ft.filter_response()
            self.steps_nodes[step] = extractAllResolvedOutputIDs(
                self.steps_results[step]
            )
            print(
                "\nAfter applying post-query filter, BTE retrieved {} unique output nodes.".format(
                    len(self.steps_nodes[step])
                )
            )
        return self.steps_nodes[step]

    def connect(self, verbose=True):
        if not validate_max_intermediate_nodes(self.intermediate_nodes):
            return
        self.query_completes = False
        inputs = restructureHintOutput(self.input_objs)
        inputs = self._expand_inputs(inputs, verbose=verbose)
        if verbose:
            self.pt.print_query_parameter_summary(inputs, self.intermediate_nodes)
        for i, node in enumerate(self.intermediate_nodes):
            if verbose:
                self.pt.print_query_plan_begin_message(i + 1)
            inputs = groupsIDsbySemanticType(inputs)
            source_types = list(inputs.keys())
            predicates = self._get_predicates_from_config(i)
            if verbose:
                print(
                    "Input Types: {}\nOutput Types: {}\nPredicates: {}\n".format(
                        ",".join(list(inputs.keys())), node, predicates
                    )
                )
            edges = getEdges(inputs, node, predicates, self.kg)
            if len(edges) == 0:
                self.pt.print_query_failure_message("APIs", i + 1)
                return
            annotatedEdges = []
            for e in edges:
                annotatedEdges += annotateEdgesWithInput(
                    e.get("edges"), e.get("inputs")
                )
            if not annotatedEdges:
                self.pt.print_query_failure_message("APIs", i + 1)
                return
            self._annotate_edges_with_filters(annotatedEdges, i)
            dp = APIQueryDispatcher(annotatedEdges, verbose=verbose)
            self.steps_results[i] = dp.syncQuery()
            if not self.steps_results[i] or len(self.steps_results[i]) == 0:
                self.pt.print_query_failure_message("results", i + 1)
                return
            inputs = self.steps_nodes[i] = extractAllResolvedOutputIDs(
                self.steps_results[i]
            )
            if verbose:
                self.pt.print_individual_query_step_summary(inputs)
            ft = self._annotate_results(i, source_types)
            inputs = self._filter_results(i, ft)
        self.query_completes = True
        if verbose:
            self.pt.print_final_result_summary(self.steps_nodes)

    def annotate(self, step=0, criteria=[]):
        ft = Filter(self.steps_results[step], criteria=criteria)
        self.steps_results[step] = ft.annotate()

    def display_table_view(self, extra_fields=[]):
        if not self.query_completes:
            print("Your query fails. Unable to display results!")
            return

        for step, step_result in self.steps_results.items():
            df = stepResult2PandasTable(
                step_result, step, len(self.steps_results), extra_fields
            )
            if step == 0:
                result = df
                continue
            join_columns = [
                "node" + str(step) + item for item in ["_id", "_type", "_label"]
            ]
            result = pd.merge(result, df, on=join_columns, how="inner")
        return result
