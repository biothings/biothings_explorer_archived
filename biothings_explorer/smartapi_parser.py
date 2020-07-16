import hashlib
from copy import deepcopy

from .utils.dataload import load_json_or_yaml


class SmartAPIParser:
    """Parse SmartAPI specifications."""

    def load_spec(self, spec=None):
        self.spec = load_json_or_yaml(spec)

    @staticmethod
    def determine_api_type(tags):
        """Determine the type of API
        
        note: API type will be used in the api_preprocess module
        """
        types = ["biothings", "biolink", "reasoner", "ctd", "opentarget"]
        for _type in types:
            if _type in tags:
                return _type
        return "other"

    def fetch_api_name(self):
        """Fetch the name of the API.
        """
        return self.spec["info"]["title"]

    def fetch_api_tags(self):
        """Fetch the tags of the API.
        """
        tags = self.spec["tags"]
        return [_item["name"] for _item in tags]

    def fetch_server_url(self):
        """fetch the server url of the API.
        """
        return self.spec["servers"][0]["url"]

    @staticmethod
    def fetch_path_params(endpoint_spec: dict):
        params = []
        if "parameters" in endpoint_spec:
            for param in endpoint_spec["parameters"]:
                if param.get("in") == "path":
                    params.append(param.get("name"))
        return params

    @staticmethod
    def fetch_response_mapping_path(endpoint_spec):
        """Fetch the path of semantic mapping json doc.
        """
        return endpoint_spec["x-bte-semanticmapping"]["$ref"]

    def fetch_response_mapping(self, ref):
        """Fetch the semantic mapping json file based on the path in $ref.
        """
        path = ref.split("/")
        return self.spec["components"]["x-bte-response-mapping"][path[-1]]

    @staticmethod
    def fetch_param(endpoint_spec):
        """fetch the parameter name of the endpoint

        params
        ======
        endpoint_spec: the smartAPI spec related to the endpoint
        """
        if "parameters" in endpoint_spec:
            return endpoint_spec["parameters"][0].get("name")
        return None

    def fetch_single_x_bte_kgs_operation(self, ref):
        path = ref.split("/")
        return self.spec["components"]["x-bte-kgs-operations"][path[-1]]

    def fetch_x_bte_kgs_operations(self, endpoint_spec):
        """fetch the x-bte-kgs-operations information of the endpoint

        params
        ======
        endpoint_spec: the smartAPI spec related to the endpoint
        """
        operations = endpoint_spec["x-bte-kgs-operations"]
        for op in operations:
            yield self.fetch_single_x_bte_kgs_operation(op["$ref"])

    @staticmethod
    def get_unique_edge_id(operation):
        _id = "-".join(
            [
                operation["server"],
                operation["method"],
                operation["path"],
                operation["output_type"],
                operation["output_id"],
            ]
        )
        request_body = operation.get("requestBody")
        if request_body and request_body.get("body"):
            for k in sorted(request_body.get("body").keys()):
                _id += "-" + k + "-" + str(request_body.get("body")[k])
        parameters = operation.get("parameters")
        if parameters:
            for k in sorted(parameters.keys()):
                _id += "-" + k + "-" + str(parameters[k])
        return hashlib.sha224(_id.encode()).hexdigest()

    def parse_individual_operation(self, op, path, method, path_params):
        res = []
        for _input in op["inputs"]:
            for _output in op["outputs"]:
                tmp = deepcopy(op)
                tags = self.fetch_api_tags()
                api_type = self.determine_api_type(tags)
                tmp.update(
                    {
                        "path": path,
                        "path_params": path_params,
                        "method": method,
                        "server": self.fetch_server_url(),
                        "api_name": self.fetch_api_name(),
                        "api_type": api_type,
                        "input_id": _input["id"],
                        "input_type": _input["semantic"],
                        "output_id": _output["id"],
                        "output_type": _output["semantic"],
                        "response_mapping": {
                            op["predicate"]: self.fetch_response_mapping(
                                op["response_mapping"]["$ref"]
                            )
                        },
                    }
                )
                tmp["id"] = self.get_unique_edge_id(tmp)
                res.append(tmp)
        return res

    def fetch_endpoint_info(self):
        res = []
        for path, path_info in self.spec["paths"].items():
            for method, method_info in path_info.items():
                path_params = self.fetch_path_params(method_info)
                if "x-bte-kgs-operations" in method_info:
                    for op in self.fetch_x_bte_kgs_operations(method_info):
                        for _op in op:
                            tmp = self.parse_individual_operation(
                                _op, path, method, path_params
                            )
                            res += tmp
        return res
