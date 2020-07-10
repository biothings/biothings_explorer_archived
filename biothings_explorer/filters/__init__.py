# main class

from co_occurs import filter_co_occur
from labels import filter_label
from edges import filter_node_degree
from apis import filter_api

class Filter():

    def __init__(self, G, filt=None, count=50, label=None):
        self.G = G
        self.filter = filt
        self.count = count
        self.label = label

    def filter_results(self):
        if not self.filter:
            return self.G
        if self.filter == 'NodeDegree':
            return filter_node_degree(self.G, self.count)
        if self.filter == 'EdgeLabel':
            if not self.label:
                print('Please include a label for this filter')
            else:
                return filter_label(self.G, self.label, self.count)
        if self.filter == 'CoOccurrence':
            return filter_co_occur(self.G, self.count)
        if self.filter == 'UniqueAPIs':
            return filter_api(self.G, self.count)
        return self.G
