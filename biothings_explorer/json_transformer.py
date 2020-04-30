from collections import defaultdict
from jsonpath_rw import parse
from .utils.common import find_longest_common_path


class Transformer():
    """Transform the JSON output from API response into schema format."""

    def __init__(self, json_doc, mapping):
        """
        Load json doc and transform mapping file.
        
        :param: json_doc: dict, the json document
        :param: mapping: dict, the schema mapping file which the transformation will be based on
        """
        self.json_doc = json_doc
        self.mapping = mapping

    @staticmethod
    def generate_parser(path):
        """
        Create path for jsonpath_rw.

        :param: path: jsonpath_rw path

        example: ensembl.gene -> ensembl[*].gene[*]
        """
        return parse(('.').join([(i + '[*]') for i in path.split('.')]))

    @staticmethod
    def fetch_all_paths_from_mapping_file(mapping_file):
        """Fetch all paths from schema mapping file."""
        paths = []
        if not mapping_file or not isinstance(mapping_file, dict):
            return []
        for v in mapping_file.values():
            if isinstance(v, list):
                paths += v
            elif isinstance(v, str):
                paths.append(v)
            else:
                raise ValueError("The data type of each path should be either list or str")
        return paths

    @staticmethod
    def group_jsonpaths(commonprefix, jsonpath_dict):
        result = defaultdict(list)
        # find the last common element, e.g. if 'go.BP' is common prefix, then 'BP' is the last common element
        lst_common_elem = commonprefix.rpartition('.')[2]
        for k, v in jsonpath_dict.items():
            for _path in v:
                splitted_path = _path.split('.')
                lst_common_element_idx = splitted_path.index(lst_common_elem)
                result['.'.join(splitted_path[0:lst_common_element_idx + 2])].append((k, _path))
        return dict(result)

    @staticmethod
    def fetch_value_by_jsonpath(json_dict, json_path):
        path_elements = json_path.split('.')
        result = json_dict
        for _ele in path_elements:
            if not _ele.startswith('['):
                result = result[_ele]
            else:
                if isinstance(result, list):
                    result = result[_ele]
        return result

    @staticmethod
    def find_key_by_value(json_dict, value):
        """Retrieve the key of a python dict based on the value"""
        for k, v in json_dict.items():
            if isinstance(v, list):
                if value in v:
                    return k
            else:
                if v == value:
                    return k

    def parse_dict(self, mapping_dict):
        """
        mapping: {"dd": "a.b.c", "ee": "a.b.d"}
        case 1: {"a": {"b": {"c": 1, "d": 2}}}
        result 1: {"dd": 1, "ee": 2}
        case 2: {"a": [{"b": {"c": 1, "d": 2}}, {"b": {"c": 3, "d": 4}}]}
        result 2: [{"dd": 1, "ee": 2}]
        case 3: {"a": }
        """
        all_paths = self.fetch_all_paths_from_mapping_file(mapping_dict)
        common_path = find_longest_common_path(all_paths)
        # Handle cases where a common prefix could be found among all paths
        if common_path:
            paths_jsonpaths_dict = {}
            jsonpaths_values_dict = {}
            for path in all_paths:
                parser = self.generate_parser(path)
                parsing_result = parser.find(self.json_doc)
                jsonpaths = [str(match.full_path) for match in parsing_result]
                values = [match.value for match in parsing_result]
                jsonpaths_values_dict.update(dict(zip(jsonpaths, values)))
                paths_jsonpaths_dict.update({path: jsonpaths})
            grouped_jsonpaths = self.group_jsonpaths(common_path,
                                                     paths_jsonpaths_dict)
            result = []
            for v in grouped_jsonpaths.values():
                _result = defaultdict(list)
                for _tuple in v:
                    schema_prop = self.find_key_by_value(mapping_dict,
                                                         _tuple[0])
                    _result[schema_prop].append(jsonpaths_values_dict[_tuple[1]])
                result.append(dict(_result))
            return result
        # Handle cases where all paths doesn't share a common prefix
        result = {}
        for k, v in mapping_dict.items():
            if isinstance(v, str):
                parser = self.generate_parser(v)
                result[k] = self.fetch_value_from_single_path(parser)
            elif isinstance(v, list):
                _res = []
                for path in v:
                    parser = self.generate_parser(path)
                    _res += self.fetch_value_from_single_path(parser)
                result[k] = _res
        return result

    def fetch_value_from_single_path(self, parser):
        return [match.value for match in parser.find(self.json_doc)]

    def fetch_value(self, key, paths):
        """Fetch value from API response.
        
        :param: key: the biolink property name.
        :param: paths: the path to the field in API response.
        """
        # Handle only one field path correspond to the key.
        if isinstance(paths, str):
            parser = self.generate_parser(paths)
            return self.fetch_value_from_single_path(parser)
        # Handle more than one field paths correspond to the key.
        if isinstance(paths, list):
            result = []
            for path in paths:
                if isinstance(path, dict):
                    _res = self.parse_dict(path)          
                elif isinstance(path, str):
                    parser = self.generate_parser(path)
                    _res = self.fetch_value_from_single_path(parser)
                else:
                    raise ValueError('{} is not valid'.format(path))
                if isinstance(_res, list):
                    result += _res
                else:
                    result.append(_res)
            return result
        if isinstance(paths, dict):
            return self.parse_dict(paths)
        return None

    def transform(self):
        new_json_doc = {k: self.fetch_value(k, v) for k,v in self.mapping.items()}
        return new_json_doc
