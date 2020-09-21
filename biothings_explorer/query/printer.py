class Print:
    def print_final_result_summary(self, stepsNodes):
        """
        Print the summary of final results.
        :param: stepsNodes: Unique node objects retrieved from each query step
        """
        print(
            "\n==========\n========== Final assembly of results ==========\n==========\n"
        )
        for k, j in stepsNodes.items():
            print("In the #{} query, BTE found {} unique nodes.".format(k + 1, len(j)))

    def print_query_failure_message(self, reason, query_id):
        """
        Print message regarding why the query fails.
        :param reason: Reason for query failure
        """
        print(
            "Unfortunately, no {} were found for Query # {}. Your query fails. Please try refine your query!".format(
                reason, query_id
            )
        )

    def print_expand_begin_message(self):
        print("\n==========\n========== QUERY EXPANSION ==========\n==========\n")
        print("You have selected to expand your inputs.")

    def print_query_plan_begin_message(self, query_id):
        print("\n========== Query # {} ==========\n".format(query_id))
        print("==== Step #1: Query Path Planning ====\n")

    def print_expand_summary_message(self, expandedInputs):
        """
        Print a summary of the expansion results.
        :param expandedInputs: A list of results from expansion.
        """
        if expandedInputs:
            print(
                "{} unique bioentities have been found as subclass of your inputs.\n".format(
                    len(expandedInputs)
                )
            )
        else:
            print("No bioentity was found to be subclass of your inputs.\n")

    def print_query_parameter_summary(self, inputs, intermediate_nodes):
        """
        Print a summary of query parameters.
        :param inputs: list of input nodes.
        :param intermediate_nodes: list of intermediate nodes.
        """
        print("==========\n========== QUERY PARAMETER SUMMARY ==========\n==========\n")
        print(
            "Your query have {} input nodes, including {} .... And BTE will find paths that connect your input nodes to your output types {}. \
Paths will contain {} intermediate nodes.\n".format(
                len(inputs),
                ",".join([item["id"]["label"] for item in inputs.values()][0:5]),
                intermediate_nodes[-1],
                len(intermediate_nodes) - 1,
            )
        )
        for i, node in enumerate(intermediate_nodes[0:-1]):
            print(
                "Intermediate node #{} will have these type constraints: {}".format(
                    i + 1, node
                )
            )

    def print_individual_query_step_summary(self, outputs):
        """
        Print summary of each query steps.
        :param outputs: outputs from the query step.
        """
        print(
            "After id-to-object translation, BTE retrieved {} unique output nodes.\n\n".format(
                len(outputs)
            )
        )

