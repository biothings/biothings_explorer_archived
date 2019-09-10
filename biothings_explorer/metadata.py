from .registry import Registry


class Metadata():
    def __init__(self, reg=None):
        if not reg:
            self.registry = Registry()
        else:
            self.registry = reg

    def list_all_semantic_types(self):
        semmantic_types = set()
        for p, o, info in self.registry.G.edges(data=True):
            semmantic_types.add(info['input_type'])
            semmantic_types.add(info['output_type'])
        return list(semmantic_types)

    def list_all_predicates(self):
        predicates = set()
        for p, o, info in self.registry.G.edges(data=True):
            predicates.add(info['label'])
        return list(predicates)

    def list_all_id_types(self):
        return list(set(self.registry.G.nodes()))

    def list_all_associations(self):
        associations = set()
        for p, o, info in self.registry.G.edges(data=True):
            _assoc = info['input_type'] + '|' + info['label'] + '|' + info['output_type']
            associations.add(_assoc)
        results = []
        for _assoc in associations:
            s, p, o = _assoc.split('|')
            results.append((s, p, o))
        return results
