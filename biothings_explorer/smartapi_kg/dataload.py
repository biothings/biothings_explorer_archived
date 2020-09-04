import requests
from copy import deepcopy

from .config import SMARTAPI_URL
from .smartapi_local_specs import SPECS


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
        specs = SPECS
    new_specs = []
    for spec in specs.get("hits"):
        tags = [item.get("name") for item in spec.get("tags")]
        if tag in tags:
            new_specs.append(restructure_specs(spec))
    return new_specs

