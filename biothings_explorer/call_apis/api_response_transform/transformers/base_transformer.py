from copy import deepcopy

from .utils import generateCurie, process_publications
from .json_transformer import Transformer


class BaseTransformer:
    def __init__(self, data):
        self.data = data
        self.edge = data.get("edge")

    def pairInputWithAPIResponse(self):
        """Create an object with key representing input, and value representing the output of API"""
        _input = generateCurie(self.edge["association"]["input_id"], self.edge["input"])
        return {_input: [self.data["response"]]}

    def wrap(self, res):
        """Wrapper functions to transform API response before passing to JSON Transformer"""
        if isinstance(res, list):
            res = {"data": res}
        return res

    def jsonTransform(self, res):
        """Transform Individual JSON response into Biolink compatible format
        :param: res: JSON response representing an output
        """
        return Transformer(res, self.edge["response_mapping"]).transform()

    def extractOutputIDs(self, res):
        """Retrieve all output IDs from response.
        :param: res: JSON response representing an output.
        """
        output_id_type = self.edge["association"]["output_id"]
        if output_id_type not in res:
            return []
        if isinstance(res[output_id_type], list):
            return [generateCurie(output_id_type, item) for item in res[output_id_type]]
        return [generateCurie(output_id_type, res[output_id_type])]

    def addEdgeInfo(self, _input, res):
        """Add edge information into individual output JSON.
        :param: res: JSON response representing an output.
        """
        if not res:
            return []
        output_ids = self.extractOutputIDs(res)
        result = []
        for item in output_ids:
            copy_item = deepcopy(item)
            copy_res = deepcopy(res)
            copy_res.update(
                {
                    "$reasoner_edge": self.edge.get("reasoner_edge", None),
                    "$association": self.edge.get("association", None),
                    "$input": _input,
                    "$output": copy_item,
                    "$original_input": self.edge.get("original_input", None),
                    "$input_resolved_identifiers": self.edge.get(
                        "input_resolved_identifiers", None
                    ),
                    "api": self.edge["association"]["api_name"],
                    "provided_by": res.get("source")
                    if res.get("source")
                    else [self.edge["association"].get("source", None)],
                }
            )
            copy_res = process_publications(copy_res)
            result.append(copy_res)
        return result

    def transform(self):
        """Main function to transform API response"""
        result = []
        responses = self.pairInputWithAPIResponse()
        for curie, res in responses.items():
            if isinstance(res, list) and len(res) > 0:
                for item in res:
                    item = self.wrap(item)
                    item = self.jsonTransform(item)
                    for val in item.values():
                        if isinstance(val, list) and len(val) > 0:
                            for v in val:
                                result += self.addEdgeInfo(curie, v)
                        else:
                            result += self.addEdgeInfo(curie, val)
        return result
