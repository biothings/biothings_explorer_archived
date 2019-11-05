from .registry import Registry
from .config import metadata
from collections import defaultdict


class Metadata():
    """ Metadata Info for the Meta Knowledge Graph stored in BTE
    """
    def __init__(self, reg=None):
        if not reg:
            self.registry = Registry()
        else:
            self.registry = reg

    def list_all_semantic_types(self):
        """List all semantic types used in BTE"""
        semmantic_types = set()
        for p, o, info in self.registry.G.edges(data=True):
            semmantic_types.add(info['input_type'])
            semmantic_types.add(info['output_type'])
        return list(semmantic_types)

    def list_all_predicates(self):
        """List all predicates used in BTE"""
        predicates = set()
        for p, o, info in self.registry.G.edges(data=True):
            predicates.add(info['label'])
        return list(predicates)

    def list_all_id_types(self):
        """List all identifiers used in BTE"""
        return list(set(self.registry.G.nodes()))

    def list_all_associations(self):
        """List all associations used in BTE
        Each association is a triple with subject, predicate and object
        """
        associations = set()
        for p, o, info in self.registry.G.edges(data=True):
            _assoc = info['input_type'] + '|' + info['label'] + '|' + info['output_type']
            associations.add(_assoc)
        results = []
        for _assoc in associations:
            s, p, o = _assoc.split('|')
            results.append((s, p, o))
        return results

    def semantic_network_graph(self, edge="pred"):
        """Convert the meta knowledge graph into a semantic graph"""
        _id = 1
        id_dict = {}
        edges = set()
        edges_dict = defaultdict(list)
        result = {'nodes': [], 'edges': []}
        for p, o, info in self.registry.G.edges(data=True):
            input_type = info['input_type']
            output_type = info['output_type']
            predicate = info['label'][4:]
            if input_type not in id_dict:
                id_dict[input_type] = _id
                result['nodes'].append({'id': _id,
                                        'group': _id,
                                        'label': input_type})
                _id += 1
            if output_type not in id_dict:
                id_dict[output_type] = _id
                result['nodes'].append({'id': _id,
                                        'group': _id,
                                        'label': output_type})
                _id += 1
            if edge == 'pred':
                _edge = str(id_dict[input_type]) + predicate + str(id_dict[output_type])
                if _edge not in edges:
                    result['edges'].append({'from': id_dict[input_type],
                                        'to': id_dict[output_type],
                                        'label': predicate})
                    edges.add(_edge)
            else:
                edge_key = [id_dict[input_type], id_dict[output_type]]
                edge_key.sort()
                edge_key = '|'.join([str(i) for i in edge_key])
                edges_dict[edge_key].append(metadata[info['api']]['api_name'])
        if edge != 'pred':
            for k, v in edges_dict.items():
                _input_type, _output_type = k.split('|')
                v = list(set(v))
                result['edges'].append({'from': int(_input_type),
                                        'to': int(_output_type),
                                        'label': '\n'.join(v)})
        return result

    def id_network_graph(self, edge="pred"):
        _id = 1
        id_dict = {}
        edges = set()
        result = {'nodes': [], 'edges': []}
        for p, o, info in self.registry.G.edges(data=True):
            input_type = info['input_id'][4:]
            output_type = info['output_id'][4:]
            predicate = info['label'][4:]
            if input_type not in id_dict:
                id_dict[input_type] = _id
                result['nodes'].append({'id': _id,
                                        'group': _id,
                                        'label': input_type})
                _id += 1
            if output_type not in id_dict:
                id_dict[output_type] = _id
                result['nodes'].append({'id': _id,
                                        'group': _id,
                                        'label': output_type})
                _id += 1
            if edge == 'pred':
                _edge = str(id_dict[input_type]) + predicate + str(id_dict[output_type])
                if _edge not in edges:
                    result['edges'].append({'from': id_dict[input_type],
                                        'to': id_dict[output_type],
                                        'label': predicate})
                    edges.add(_edge)
            else:
                _edge = str(id_dict[input_type]) + metadata[info['api']]['api_name'] + str(id_dict[output_type])
                if _edge not in edges:
                    result['edges'].append({'from': id_dict[input_type],
                                            'to': id_dict[output_type],
                                            'label': metadata[info['api']]['api_name']})
                    edges.add(_edge)
        return result
