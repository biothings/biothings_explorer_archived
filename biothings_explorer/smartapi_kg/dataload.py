import requests
from copy import deepcopy
import json
import os
import pkg_resources

from .config import SMARTAPI_URL


def restructure_specs(spec):
    """SmartAPI API restructure each spec when storing them. This function converts them back to the original smartapi specification"""
    copy_spec = deepcopy(spec)
    new_paths = {}
    if isinstance(copy_spec.get("paths"), list) and len(copy_spec.get("paths")) > 0:
        for path in copy_spec.get("paths"):
            new_paths[path.get("path")] = path.get("pathitem")
    copy_spec["paths"] = new_paths
    return copy_spec


def load_specs(source="remote", tag="translator"):
    """Load SmartAPI specs."""
    if source == "remote":
        try:
            specs = requests.get(SMARTAPI_URL).json()
        except:
            raise Exception(
                "Unable to retrieve smartapi specs from {}".format(SMARTAPI_URL)
            )
    else:
        DATA_PATH = pkg_resources.resource_filename("biothings_explorer", "data/")
        DB_FILE = pkg_resources.resource_filename(
            "biothings_explorer", "data/smartapi_local_specs.json"
        )
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path, "smartapi_local_specs.json")
        with open(DB_FILE) as f:
            specs = json.load(f)
    new_specs = []
    for spec in specs.get("hits"):
        tags = [item.get("name") for item in spec.get("tags")]
        if tag in tags:
            new_specs.append(restructure_specs(spec))
    return new_specs

