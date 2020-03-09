# -*- coding: utf-8 -*-
"""Convert the output of BTE to ReasonerAPIStd

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""
import hashlib
from collections import defaultdict


class ReasonerConverter():
    """Convert the output of BTE to ReasonerAPIStd."""

    def load_bte_query_path(self, start, intermediate, end):
        """Load bte input query in the form of path.
        
        Parameters
            * start: the input of user query
            * intermediate: the intermediate nodes connecting input and output
            * end: the output of user query
        """
        self.path = [start.get('type')]
        self.start = start
        if intermediate:
            if isinstance(intermediate, list):
                self.path += intermediate
            else:
                self.path.append(intermediate)
        if isinstance(end, str):
            self.path.append(end)
        elif isinstance(end, list):
            self.path.append(tuple(end))
        elif isinstance(end, dict):
            self.path.append(end.get('type'))

    def load_bte_output(self, G):
        """Load bte output in the format of networkx graph into class.
        
        Parameters
            * G: the networkx representation of bte output
        """
        self.G = G
        self.nodes = self.G.nodes(data=True)

    def get_curie(self, node):
        """Retrieve the curie representation of node.
        
        Parameters
            * node: the node id in networkx graph
        """
        if not node:
            return str(node)
        node_info = self.nodes[node]
        if "identifier" in node_info:
            prefix = node_info["identifier"][4:]
            curie = prefix.upper() + ':' + node
            return curie
        else:
            return node

    def hash_id(self, _id):
        """Hash an id.
        
        Parameters
            * _id: a node or edge id
        """
        hash_obj = hashlib.sha256(str(_id).encode())
        return hash_obj.hexdigest()

    def fetch_edges(self):
        """Reorganize the edges into reasonerSTd format.
        """
        self.result = defaultdict(list)
        edges = []
        for k, v, o in self.G.edges(data=True):
            source_id = self.get_curie(k)
            target_id = self.get_curie(v)
            edge_source = o['info'].get('$api')
            _type = o.get('label')[4:]
            _id = self.hash_id(source_id + target_id + edge_source + _type)
            edge = {"source_id": source_id,
                    "target_id": target_id,
                    "edge_source": edge_source,
                    "id": _id,
                    "type": _type}
            self.result[source_id + '|||' + target_id].append(_id)
            edges.append(edge)
        return edges

    def fetch_nodes(self):
        """Reorganize the nodes into reasonerSTD format.
        """
        nodes = []
        for k, v in self.nodes:
            name = v['equivalent_ids'].get("bts:name")
            if name and isinstance(name, list):
                name = str(name[0])
            else:
                name = str(self.get_curie(k))
            node = {"id": self.get_curie(k),
                    "name": name,
                    "type": v["type"],
                    "equivalent_identifiers": v['equivalent_ids']}
            nodes.append(node)
        return nodes


    def generate_knowledge_graph(self):
        """Reorganize the nodes and edges into reasonerSTD format.
        """
        if len(self.G) == 0:
            return {"nodes": [], "edges": []}
        return {"nodes": self.fetch_nodes(),
                "edges": self.fetch_edges()}

    def generate_question_graph(self):
        if not self.path:
            return {"edges": [], "nodes": []}
        node_id = 0
        edge_id = 0

        nodes = []
        edges = []

        node2idmapping = {}

        for i, node in enumerate(self.path):
            if isinstance(node, str):
                nodes.append({"id": "n" + str(node_id),
                              "type": node})
                node2idmapping[str(i) + '-' + node + '-0'] = "n" + str(node_id)
                node_id += 1
            elif isinstance(node, tuple):
                for j, _n in enumerate(node):
                    nodes.append({"id": "n" + str(node_id),
                                  "type": _n})
                    node2idmapping[str(i) + '-' + _n + '-' + str(j)] = "n" + str(node_id)
                    node_id += 1
            nodes[0]['curie'] = [self.start['primary']['identifier'] + ':' + self.start['primary']['value']]


        for i in range(0, len(self.path) - 1):
            source_node = self.path[i]
            target_node = self.path[i+1]
            if isinstance(source_node, str):
                source_node = [source_node]
            if isinstance(target_node, str):
                target_node = [target_node]
            for p, _s in enumerate(source_node):
                for q, _t in enumerate(target_node):
                    source_id = node2idmapping[str(i) + '-' + _s + '-' + str(p)]
                    target_id = node2idmapping[str(i+1) + '-' + _t + '-' + str(q)]
                    edges.append({"id": "e" + str(edge_id),
                                  "source_id": source_id,
                                  "target_id": target_id,
                                  "directed": True})
                    edge_id += 1
        return {"edges": edges,
                "nodes": nodes}
    
    def generate_result(self):
        result = {"node_bindings": [], "edge_bindings": []}
        for k, v in self.result.items():
            target_id = k.split('|||')[-1]
            result["node_bindings"].append({"qg_id": "n1", "kg_id": target_id})
            result["edge_bindings"].append({"qg_id": "e1", "kg_id": v})
        return result
    
    def generate_reasoner_response(self):
        """Generate reasoner response"""
        response = {"query_graph": self.generate_question_graph(),
                    "knowledge_graph": self.generate_knowledge_graph()}
        response['results'] = self.generate_result()
        return response
