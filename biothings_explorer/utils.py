# -*- coding: utf-8 -*-

"""
biothings_explorer.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used within bioThings_explorer
that are also useful for external consumption.
"""
import json
import yaml
from os.path import commonprefix

import requests
import graphviz


def visualize(edges, size=None):
    if size:
        d = graphviz.Digraph(graph_attr=[('size', size)])    # pylint: disable=undefined-variable
    else:
        d = graphviz.Digraph()                               # pylint: disable=undefined-variable
    for _item in edges:
        d.edge(_item[0], _item[1])
    return d


def load_json_or_yaml(file_path):
    """Load either json or yaml document from file path or url or JSON doc

    :arg str file_path: The path of the url doc, could be url or file path
    """
    # handle json doc
    if isinstance(file_path, dict):
        return file_path
    # handle url
    elif file_path.startswith("http"):
        with requests.get(file_path) as url:
            # check if http requests returns a success status code
            if url.status_code != 200:
                raise ValueError("Invalid URL!")
            else:
                _data = url.content
    # handle file path
    else:
        try:
            with open(file_path) as f:
                _data = f.read()
        except FileNotFoundError:
            raise ValueError("Invalid File Path!")
    try:
        data = json.loads(_data)
    except json.JSONDecodeError:   # for py>=3.5
    # except ValueError:               # for py<3.5
        try:
            data = yaml.load(_data, Loader=yaml.SafeLoader)
        except (yaml.scanner.ScannerError,
                yaml.parser.ParserError):
            raise ValueError("Not a valid JSON or YAML format.")
    return data


def find_common_path(dict_values):
    return commonprefix(dict_values).rsplit('.', 1)[0]


def get_dict_values(python_dict):
    return [v for k, v in python_dict.items() if k not in ["@type", "$input", "$source"]]


def unlist(d):
    for key, val in d.items():
        if isinstance(val, list):
            if len(val) == 1:
                d[key] = val[0]
        elif isinstance(val, dict):
            unlist(val)
    return d

def restructure_equivalent_ids_dict(id_dict):
    result = []
    for k, v in id_dict.items():
        if type(v) == list:
            for _v in v:
                result.append(k + ':' + _v)
        else:
            result.append(k + ':' + v)
    return result

# Python porgram to find common elements in 
# both sets using intersection function in 
# sets 
# function  
def common_member(a, b): 
    """Python porgram to find common elements in both sets/lists
    """
    a = [(i[0], restructure_equivalent_ids_dict(i[1])) for i in a]
    b = [(i[0], restructure_equivalent_ids_dict(i[1])) for i in b]
    matched = []
    for i in a:
        for j in b:
            a_set = set(i[1])
            b_set = set(j[1])
            if len(a_set.intersection(b_set)) > 0:
                matched.append((i[0], j[0]))
    return matched