# -*- coding: utf-8 -*-
"""
Export the output of BTE to GraphML file type.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

import copy
import networkx as nx


class GraphmlConverter():

    def load_bte_output(self, G):
        """
        Load bte output in the format of networkx graph into class.

        :param: G : the networkx representation of bte output
        """
        self.G = copy.deepcopy(G)

    def restructure_node_info(self):
        """
        Restructure node info.

        note: graphml doesn't support dict as output
        """
        for _, v in self.G.nodes(data=True):
            if 'equivalent_ids' in v:
                v.update(v['equivalent_ids'])
                del v['equivalent_ids']
        for _, v in self.G.nodes(data=True):
            for m, n in v.items():
                if isinstance(n, list):
                    v[m] = ','.join([str(_item) for _item in n])

    def restructure_edge_info(self):
        """
        Restructure edge info.

        note: graphml doesn't support dict as output
        """
        for _, _, o in self.G.edges(data=True):
            if 'info' in o:
                o.update(o['info'])
                del o['info']
            for m, n in o.items():
                if isinstance(n, list):
                    o[m] = ','.join([str(_item) for _item in n])
                if not n:
                    o[m] = 'null'

    def generate_graphml_output(self, path):
        """
        Return the graphml representation of bte output.

        :param: path (str) : the file path to store graphml file
        """
        self.restructure_edge_info()
        self.restructure_node_info()
        return nx.write_graphml(self.G, path)
