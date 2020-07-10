# main class

from .co_occurs import filter_co_occur
from .labels import filter_label
from .edges import filter_node_degree
from .apis import filter_api

class Filter():

    def __init__(self, G, filter=None, count=50):
        self.G = G
        self.filter = filter
        self.count = count

    def filter_results(self):
        if not self.filter:
            return self.G
        if self.filter == 'NodeDegree':
            return filter_node_degree(self.G, self.count)
        if self.filter == 'EdgeLabel':
            return filter_label(self.G, self.count)
        if self.filter == 'CoOccurrence':
            return filter_co_occur(self.G, self.count)
        if self.filter == 'UniqueAPIs':
            return filter_api(self.G, self.count)
        return self.G
