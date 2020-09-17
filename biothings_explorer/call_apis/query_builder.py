from copy import deepcopy

from ..config_new import ALWAYS_PREFIXED


class QueryBuilder:
    def __init__(self, edge):
        self.POST_HEADER = {"content-type": "application/x-www-form-urlencoded"}
        self.edge = edge
        self.server = edge["query_operation"]["server"]
        if edge["query_operation"]["server"].endswith("/"):
            self.server = self.server.strip("/")
        self.url = self.server + edge["query_operation"]["path"]
        self.method = edge["query_operation"]["method"]
        self.supportBatch = edge["query_operation"].get("supportBatch")
        self.input = edge.get("input")
        self.inputSeparator = edge["query_operation"].get("inputSeparator")
        self.params = deepcopy(edge["query_operation"].get("params"))
        self.data = ""
        if "reasoner" in edge["query_operation"].get("tags"):
            self.constructRequestConfigForReasonerAPI()
        else:
            self.constructInput()
            self.constructRequestBody()
            self.constructParams()
            self.constructRequestConfig()

    def constructInput(self):
        """Construct input based on method and inputSeparator"""
        if self.supportBatch:
            if not isinstance(self.input, list):
                self.input = [self.input]
            self.input = self.inputSeparator.join(self.input)

    def constructParams(self):
        """Construct parameters for API calls"""
        if self.edge["query_operation"].get("path_params"):
            for param in self.edge["query_operation"].get("path_params"):
                self.url = self.url.replace(
                    "{" + param + "}", self.params.pop(param)
                ).replace("{inputs[0]}", self.input)
        for param, val in self.params.items():
            if isinstance(val, bool):
                self.params[param] = str(val)
            if isinstance(val, str):
                self.params[param] = val.replace("{inputs[0]}", self.input)

    def constructRequestBody(self):
        """Construct request body for API calls"""
        if self.edge["query_operation"].get("request_body") and "body" in self.edge[
            "query_operation"
        ].get("request_body"):
            body = self.edge["query_operation"]["request_body"]["body"]
            self.data = ""
            for k, v in body.items():
                self.data = (
                    self.data + k + "=" + v.replace("{inputs[0]}", self.input) + "&"
                )
            self.data = self.data.strip("&")

    def constructRequestConfig(self):
        """Construct the request config for python reqeust library."""
        self.config = {
            "url": self.url,
            "params": self.params,
            "data": self.data,
            "method": self.method,
            "timeout": 5000,
        }

    def constructRequestConfigForReasonerAPI(self):
        """Construct the ReasonerStdAPI request config for python reqeust library."""

        def id2curie(prefix, val):
            if prefix in ALWAYS_PREFIXED:
                return val
            return prefix + ":" + val

        predicate = self.edge["association"]["predicate"]
        input_type = self.edge["association"]["input_type"].lower()
        output_type = self.edge["association"]["output_type"].lower()
        _input = id2curie(self.edge["association"]["input_id"], self.input)
        if self.edge["association"]["api_name"] == "Genetics Provider API":
            predicate = "associated"
            if input_type == "phenotypicfeature":
                input_type = "phenotype"
            if output_type == "phenotypicfeature":
                output_type = "phenotype"
        self.config = {
            "url": self.url,
            "json": {
                "message": {
                    "query_graph": {
                        "edges": [
                            {
                                "id": "e00",
                                "source_id": "n00",
                                "target_id": "n01",
                                "type": predicate,
                            }
                        ],
                        "nodes": [
                            {"curie": _input, "id": "n00", "type": input_type},
                            {"id": "n01", "type": output_type},
                        ],
                    }
                }
            },
        }
