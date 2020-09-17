import sys

from .dataload import load_specs
from .smartapi_parser import SmartAPIParser
from .filter import filterOps
import traceback


class MetaKG:
    def __init__(self):
        self.ops = []
        self.parser = SmartAPIParser()

    def populateOpsFromSpecs(self, specs, verbose=False):
        """Populate meta-kg operations based on SmartAPI specifications"""
        self.ops = []
        for spec in specs:
            try:
                self.parser.load_spec(spec)
                self.ops += self.parser.fetch_endpoint_info()
            except:
                if verbose:
                    print("Unexpected error:", sys.exc_info()[0])
                    print(
                        "failed to load the following spec {}".format(spec.get("info"))
                    )

    def constructMetaKG(self, source="remote", tag="translator"):
        """Construct API Meta Knowledge Graph based on SmartAPI Specifications."""
        specs = load_specs(source=source, tag=tag)
        self.populateOpsFromSpecs(specs)

    def filter(self, criteria):
        return filterOps(self.ops, criteria)
