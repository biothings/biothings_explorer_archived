import copy
import networkx as nx

class GraphmlConverter():

    def load_bte_output(self, G):
        """Load bte output in the format of networkx graph into class
        
        params
        ======
        G: the networkx representation of bte output
        """
        self.G = copy.deepcopy(G)

    def restructure_node_info(self):
        """restructure node info
        note: graphml doesn't support dict as output
        """
        for k, v in self.G.nodes(data=True):
            if 'equivalent_ids' in v:
                v.update(v['equivalent_ids'])
                del v['equivalent_ids']
        for k, v in self.G.nodes(data=True):
            for m, n in v.items():
                if type(n) == list:
                    v[m] = ','.join(str(n))
    
    def restructure_edge_info(self):
        """restructure edge info
        note: graphml doesn't support dict as output
        """
        for k, v, o in self.G.edges(data=True):
            if 'info' in o:
                o.update(o['info'])
                del o['info']
            for m, n in o.items():
                if type(n) == list:
                    o[m] = ','.join(str(n))        
    def generate_graphml_output(self, path):
        """return the graphml representation of bte output
        
        params
        ======
        path: the file path to store graphml file
        """
        self.restructure_edge_info()
        self.restructure_node_info()
        return nx.write_graphml(self.G, path)