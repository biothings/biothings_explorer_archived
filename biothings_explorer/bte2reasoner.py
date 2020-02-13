import hashlib


class ReasonerConverter():

    def load_bte_query_path(self, start, intermediate, end):
        """Load bte input query in the form of path
        
        params
        ======
        start: the input of user query
        intermediate: the intermediate nodes connecting input and output
        end: the output of user query
        """
        self.path = [start.get('type')]
        if intermediate:
            if type(intermediate) == list:
                self.path += intermediate
            else:
                self.path.append(intermediate)
        if type(end) == str:
            self.path.append(end)
        elif type(end) == list:
            self.path.append(tuple(end))
        elif type(end) == dict:
            self.path.append(end.get('type'))

    def load_bte_output(self, G):
        """Load bte output in the format of networkx graph into class
        
        params
        ======
        G: the networkx representation of bte output
        """
        self.G = G
        self.nodes = self.G.nodes(data=True)

    def get_curie(self, node):
        """retrieve the curie representation of node
        
        params
        ======
        node: the node id in networkx graph
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
        """hash an id
        
        params
        ======
        _id: a node or edge id
        """
        hash_obj = hashlib.sha1(str(_id).encode())
        return hash_obj.hexdigest()

    def fetch_edges(self):
        """reorganize the edges into reasonerSTd format
        """
        edges = []
        for k, v, o in self.G.edges(data=True):
            edge = {"source_id": self.get_curie(k),
                    "target_id": self.get_curie(v),
                    "edge_source": o['info'].get('$api'),
                    "id": self.hash_id(self.get_curie(k) + self.get_curie(v)),
                    "type": o.get('label')[4:]}
            edges.append(edge)
        return edges

    def fetch_nodes(self):
        """reorganize the nodes into reasonerSTD format
        """
        nodes = []
        for k, v in self.nodes:
            node = {"id": self.get_curie(k),
                    "name": v['equivalent_ids'].get("bts:name"),
                    "type": v["type"],
                    "equivalent_identifiers": v['equivalent_ids']}
            nodes.append(node)
        return nodes


    def generate_knowledge_graph(self):
        """reorganize the nodes and edges into reasonerSTD format
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
            if type(node) == str:
                nodes.append({"id": "n" + str(node_id),
                              "type": node})
                node2idmapping[str(i) + '-' + node + '-0'] = "n" + str(node_id)
                node_id += 1
            elif type(node) == tuple:
                for j, _n in enumerate(node):
                    nodes.append({"id": "n" + str(node_id),
                                  "type": _n})
                    node2idmapping[str(i) + '-' + _n + '-' + str(j)] = "n" + str(node_id)
                    node_id += 1


        for i in range(0, len(self.path) - 1):
            source_node = self.path[i]
            target_node = self.path[i+1]
            if type(source_node) == str:
                source_node = [source_node]
            if type(target_node) == str:
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
    
    def generate_reasoner_response(self):
        """generate reasoner response"""
        return {"question_graph": self.generate_question_graph(),
                "knowledge_graph": self.generate_knowledge_graph()}