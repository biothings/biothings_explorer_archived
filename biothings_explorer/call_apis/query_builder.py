from copy import deepcopy


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
