# -*- coding: utf-8 -*-
"""A fix for GraphML write_graphml module

Run this code only when you need to generate a metro Meta-KG graph

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

import warnings
from collections import defaultdict

try:
    from xml.etree.cElementTree import Element, ElementTree
    from xml.etree.cElementTree import tostring, fromstring
except ImportError:
    try:
        from xml.etree.ElementTree import Element, ElementTree
        from xml.etree.ElementTree import tostring, fromstring
    except ImportError:
        pass

try:
    import lxml.etree as lxmletree
except ImportError:
    lxmletree = None

import networkx as nx
from networkx.utils import open_file, make_str

__all__ = [
    "write_graphml",
    "generate_graphml",
    "write_graphml_xml",
    "write_graphml_lxml",
    "GraphMLWriter",
]


@open_file(1, mode="wb")
def write_graphml_xml(
    G, path, encoding="utf-8", prettyprint=True, infer_numeric_types=False
):
    """Write G in GraphML XML format to path

    Parameters
    ----------
    G : graph
       A networkx graph
    path : file or string
       File or filename to write.
       Filenames ending in .gz or .bz2 will be compressed.
    encoding : string (optional)
       Encoding for text data.
    prettyprint : bool (optional)
       If True use line breaks and indenting in output XML.
    infer_numeric_types : boolean
       Determine if numeric types should be generalized.
       For example, if edges have both int and float 'weight' attributes,
       we infer in GraphML that both are floats.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.write_graphml(G, "test.graphml")

    Notes
    -----
    It may be a good idea in Python2 to convert strings to unicode
    before giving the graph to write_gml. At least the strings with
    either many characters to escape.

    This implementation does not support mixed graphs (directed
    and unidirected edges together) hyperedges, nested graphs, or ports.
    """
    writer = GraphMLWriter(
        encoding=encoding,
        prettyprint=prettyprint,
        infer_numeric_types=infer_numeric_types,
    )
    writer.add_graph_element(G)
    writer.dump(path)


@open_file(1, mode="wb")
def write_graphml_lxml(
    G, path, encoding="utf-8", prettyprint=True, infer_numeric_types=False
):
    """Write G in GraphML XML format to path

    This function uses the LXML framework and should be faster than
    the version using the xml library.

    Parameters
    ----------
    G : graph
       A networkx graph
    path : file or string
       File or filename to write.
       Filenames ending in .gz or .bz2 will be compressed.
    encoding : string (optional)
       Encoding for text data.
    prettyprint : bool (optional)
       If True use line breaks and indenting in output XML.
    infer_numeric_types : boolean
       Determine if numeric types should be generalized.
       For example, if edges have both int and float 'weight' attributes,
       we infer in GraphML that both are floats.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> nx.write_graphml_lxml(G, "fourpath.graphml")  # doctest: +SKIP

    Notes
    -----
    This implementation does not support mixed graphs (directed
    and unidirected edges together) hyperedges, nested graphs, or ports.
    """
    writer = GraphMLWriterLxml(
        path,
        graph=G,
        encoding=encoding,
        prettyprint=prettyprint,
        infer_numeric_types=infer_numeric_types,
    )
    writer.dump()


def generate_graphml(G, encoding="utf-8", prettyprint=True):
    """Generate GraphML lines for G

    Parameters
    ----------
    G : graph
       A networkx graph
    encoding : string (optional)
       Encoding for text data.
    prettyprint : bool (optional)
       If True use line breaks and indenting in output XML.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> linefeed = chr(10)  # linefeed = \n
    >>> s = linefeed.join(nx.generate_graphml(G))  # doctest: +SKIP
    >>> for line in nx.generate_graphml(G):  # doctest: +SKIP
    ...    print(line)

    Notes
    -----
    This implementation does not support mixed graphs (directed and unidirected
    edges together) hyperedges, nested graphs, or ports.
    """
    writer = GraphMLWriter(encoding=encoding, prettyprint=prettyprint)
    writer.add_graph_element(G)
    for line in str(writer).splitlines():
        yield line


class GraphML(object):
    NS_GRAPHML = "http://graphml.graphdrawing.org/xmlns"
    NS_XSI = "http://www.w3.org/2001/XMLSchema-instance"
    # xmlns:y="http://www.yworks.com/xml/graphml"
    NS_Y = "http://www.yworks.com/xml/graphml"
    SCHEMALOCATION = " ".join(
        [
            "http://graphml.graphdrawing.org/xmlns",
            "http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd",
        ]
    )

    try:
        chr(12345)  # Fails on Py!=3.
        unicode = str  # Py3k's str is our unicode type
        long = int  # Py3K's int is our long type
    except ValueError:
        # Python 2.x
        pass

    types = [
        (int, "integer"),  # for Gephi GraphML bug
        (str, "yfiles"),
        (str, "string"),
        (unicode, "string"),
        (int, "int"),
        (long, "long"),
        (float, "float"),
        (float, "double"),
        (bool, "boolean"),
    ]

    # These additions to types allow writing numpy types
    try:
        import numpy as np
    except:
        pass
    else:
        # prepend so that python types are created upon read (last entry wins)
        types = [
            (np.float64, "float"),
            (np.float32, "float"),
            (np.float16, "float"),
            (np.float_, "float"),
            (np.int, "int"),
            (np.int8, "int"),
            (np.int16, "int"),
            (np.int32, "int"),
            (np.int64, "int"),
            (np.uint8, "int"),
            (np.uint16, "int"),
            (np.uint32, "int"),
            (np.uint64, "int"),
            (np.int_, "int"),
            (np.intc, "int"),
            (np.intp, "int"),
        ] + types

    xml_type = dict(types)
    python_type = dict(reversed(a) for a in types)

    # This page says that data types in GraphML follow Java(TM).
    #  http://graphml.graphdrawing.org/primer/graphml-primer.html#AttributesDefinition
    # true and false are the only boolean literals:
    #  http://en.wikibooks.org/wiki/Java_Programming/Literals#Boolean_Literals
    convert_bool = {
        # We use data.lower() in actual use.
        "true": True,
        "false": False,
        # Include integer strings for convenience.
        "0": False,
        0: False,
        "1": True,
        1: True,
    }


class GraphMLWriter(GraphML):
    def __init__(
        self, graph=None, encoding="utf-8", prettyprint=True, infer_numeric_types=False
    ):
        try:
            import xml.etree.ElementTree
        except ImportError:
            msg = "GraphML writer requires xml.elementtree.ElementTree"
            raise ImportError(msg)
        self.myElement = Element

        self.infer_numeric_types = infer_numeric_types
        self.prettyprint = prettyprint
        self.encoding = encoding
        self.xml = self.myElement(
            "graphml",
            {
                "xmlns": self.NS_GRAPHML,
                "xmlns:xsi": self.NS_XSI,
                "xsi:schemaLocation": self.SCHEMALOCATION,
            },
        )
        self.keys = {}
        self.attributes = defaultdict(list)
        self.attribute_types = defaultdict(set)

        if graph is not None:
            self.add_graph_element(graph)

    def __str__(self):
        if self.prettyprint:
            self.indent(self.xml)
        s = tostring(self.xml).decode(self.encoding)
        return s

    def attr_type(self, name, scope, value):
        """Infer the attribute type of data named name. Currently this only
        supports inference of numeric types.

        If self.infer_numeric_types is false, type is used. Otherwise, pick the
        most general of types found across all values with name and scope. This
        means edges with data named 'weight' are treated separately from nodes
        with data named 'weight'.
        """
        if self.infer_numeric_types:
            types = self.attribute_types[(name, scope)]

            try:
                chr(12345)  # Fails on Py<3.
                local_long = int  # Py3's int is Py2's long type
                local_unicode = str  # Py3's str is Py2's unicode type
            except ValueError:
                # Python 2.x
                local_long = long
                local_unicode = unicode

            if len(types) > 1:
                if str in types:
                    return str
                elif local_unicode in types:
                    return local_unicode
                elif float in types:
                    return float
                elif local_long in types:
                    return local_long
                else:
                    return int
            else:
                return list(types)[0]
        else:
            return type(value)

    def get_key(self, name, attr_type, scope, default):
        keys_key = (name, attr_type, scope)
        try:
            return self.keys[keys_key]
        except KeyError:
            new_id = "d%i" % len(list(self.keys))
            self.keys[keys_key] = new_id
            key_kwargs = {
                "id": new_id,
                "for": scope,
                "attr.name": name,
                "attr.type": attr_type,
            }
            key_element = self.myElement("key", **key_kwargs)
            # add subelement for data default value if present
            if default is not None:
                default_element = self.myElement("default")
                default_element.text = make_str(default)
                key_element.append(default_element)
            self.xml.insert(0, key_element)
        return new_id

    def add_data(self, name, element_type, value, scope="all", default=None):
        """
        Make a data element for an edge or a node. Keep a log of the
        type in the keys table.
        """
        if element_type not in self.xml_type:
            msg = "GraphML writer does not support %s as data values."
            raise nx.NetworkXError(msg % element_type)
        keyid = self.get_key(name, self.xml_type[element_type], scope, default)
        data_element = self.myElement("data", key=keyid)
        data_element.text = make_str(value)
        return data_element

    def add_attributes(self, scope, xml_obj, data, default):
        """Appends attribute data to edges or nodes, and stores type information
        to be added later. See add_graph_element.
        """
        for k, v in data.items():
            self.attribute_types[(make_str(k), scope)].add(type(v))
            self.attributes[xml_obj].append([k, v, scope, default.get(k)])

    def add_nodes(self, G, graph_element):
        default = G.graph.get("node_default", {})
        for node, data in G.nodes(data=True):
            node_element = self.myElement(
                "node", id=make_str(node), label=make_str(node)
            )
            self.add_attributes("node", node_element, data, default)
            graph_element.append(node_element)

    def add_edges(self, G, graph_element):
        if G.is_multigraph():
            cnt = 0
            for u, v, key, data in G.edges(data=True, keys=True):
                edge_element = self.myElement(
                    "edge",
                    source=make_str(u),
                    target=make_str(v),
                    label=data.get("label"),
                    id="e" + str(cnt),
                )
                cnt += 1
                default = G.graph.get("edge_default", {})
                self.add_attributes("edge", edge_element, data, default)
                graph_element.append(edge_element)
        else:
            for u, v, data in G.edges(data=True):
                edge_element = self.myElement(
                    "edge", source=make_str(u), target=make_str(v)
                )
                default = G.graph.get("edge_default", {})
                self.add_attributes("edge", edge_element, data, default)
                graph_element.append(edge_element)

    def add_graph_element(self, G):
        """
        Serialize graph G in GraphML to the stream.
        """
        if G.is_directed():
            default_edge_type = "directed"
        else:
            default_edge_type = "undirected"

        graphid = G.graph.pop("id", None)
        if graphid is None:
            graph_element = self.myElement("graph", edgedefault=default_edge_type)
        else:
            graph_element = self.myElement(
                "graph", edgedefault=default_edge_type, id=graphid
            )
        default = {}
        data = {
            k: v
            for (k, v) in G.graph.items()
            if k not in ["node_default", "edge_default"]
        }
        self.add_attributes("graph", graph_element, data, default)
        self.add_nodes(G, graph_element)
        self.add_edges(G, graph_element)

        # self.attributes contains a mapping from XML Objects to a list of
        # data that needs to be added to them.
        # We postpone processing in order to do type inference/generalization.
        # See self.attr_type
        for (xml_obj, data) in self.attributes.items():
            for (k, v, scope, default) in data:
                xml_obj.append(
                    self.add_data(
                        make_str(k),
                        self.attr_type(k, scope, v),
                        make_str(v),
                        scope,
                        default,
                    )
                )
        self.xml.append(graph_element)

    def add_graphs(self, graph_list):
        """ Add many graphs to this GraphML document. """
        for G in graph_list:
            self.add_graph_element(G)

    def dump(self, stream):
        if self.prettyprint:
            self.indent(self.xml)
        document = ElementTree(self.xml)
        document.write(stream, encoding=self.encoding, xml_declaration=True)

    def indent(self, elem, level=0):
        # in-place prettyprint formatter
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


class IncrementalElement(object):
    """Wrapper for _IncrementalWriter providing an Element like interface.

    This wrapper does not intend to be a complete implementation but rather to
    deal with those calls used in GraphMLWriter.
    """

    def __init__(self, xml, prettyprint):
        self.xml = xml
        self.prettyprint = prettyprint

    def append(self, element):
        self.xml.write(element, pretty_print=self.prettyprint)


class GraphMLWriterLxml(GraphMLWriter):
    def __init__(
        self,
        path,
        graph=None,
        encoding="utf-8",
        prettyprint=True,
        infer_numeric_types=False,
    ):
        self.myElement = lxmletree.Element

        self._encoding = encoding
        self._prettyprint = prettyprint
        self.infer_numeric_types = infer_numeric_types

        self._xml_base = lxmletree.xmlfile(path, encoding=encoding)
        self._xml = self._xml_base.__enter__()
        self._xml.write_declaration()

        # We need to have a xml variable that support insertion. This call is
        # used for adding the keys to the document.
        # We will store those keys in a plain list, and then after the graph
        # element is closed we will add them to the main graphml element.
        self.xml = []
        self._keys = self.xml
        self._graphml = self._xml.element(
            "graphml",
            {
                "xmlns": self.NS_GRAPHML,
                "xmlns:xsi": self.NS_XSI,
                "xsi:schemaLocation": self.SCHEMALOCATION,
            },
        )
        self._graphml.__enter__()
        self.keys = {}
        self.attribute_types = defaultdict(set)

        if graph is not None:
            self.add_graph_element(graph)

    def add_graph_element(self, G):
        """
        Serialize graph G in GraphML to the stream.
        """
        if G.is_directed():
            default_edge_type = "directed"
        else:
            default_edge_type = "undirected"

        graphid = G.graph.pop("id", None)
        if graphid is None:
            graph_element = self._xml.element("graph", edgedefault=default_edge_type)
        else:
            graph_element = self._xml.element(
                "graph", edgedefault=default_edge_type, id=graphid
            )

        # gather attributes types for the whole graph
        # to find the most general numeric format needed.
        # Then pass through attributes to create key_id for each.
        graphdata = {
            k: v
            for k, v in G.graph.items()
            if k not in ("node_default", "edge_default")
        }
        node_default = G.graph.get("node_default", {})
        edge_default = G.graph.get("edge_default", {})
        # Graph attributes
        for k, v in graphdata.items():
            self.attribute_types[(make_str(k), "graph")].add(type(v))
        for k, v in graphdata.items():
            element_type = self.xml_type[self.attr_type(k, "graph", v)]
            self.get_key(make_str(k), element_type, "graph", None)
        # Nodes and data
        for node, d in G.nodes(data=True):
            for k, v in d.items():
                self.attribute_types[(make_str(k), "node")].add(type(v))
        for node, d in G.nodes(data=True):
            for k, v in d.items():
                T = self.xml_type[self.attr_type(k, "node", v)]
                self.get_key(make_str(k), T, "node", node_default.get(k))
        # Edges and data
        if G.is_multigraph():
            for u, v, ekey, d in G.edges(keys=True, data=True):
                for k, v in d.items():
                    self.attribute_types[(make_str(k), "edge")].add(type(v))
            for u, v, ekey, d in G.edges(keys=True, data=True):
                for k, v in d.items():
                    T = self.xml_type[self.attr_type(k, "edge", v)]
                    self.get_key(make_str(k), T, "edge", edge_default.get(k))
        else:
            for u, v, d in G.edges(data=True):
                for k, v in d.items():
                    self.attribute_types[(make_str(k), "edge")].add(type(v))
            for u, v, d in G.edges(data=True):
                for k, v in d.items():
                    T = self.xml_type[self.attr_type(k, "edge", v)]
                    self.get_key(make_str(k), T, "edge", edge_default.get(k))

        # Now add attribute keys to the xml file
        for key in self.xml:
            self._xml.write(key, pretty_print=self._prettyprint)

        # The incremental_writer writes each node/edge as it is created
        incremental_writer = IncrementalElement(self._xml, self._prettyprint)
        with graph_element:
            self.add_attributes("graph", incremental_writer, graphdata, {})
            self.add_nodes(G, incremental_writer)  # adds attributes too
            self.add_edges(G, incremental_writer)  # adds attributes too

    def add_attributes(self, scope, xml_obj, data, default):
        """Appends attribute data."""
        for k, v in data.items():
            data_element = self.add_data(
                make_str(k),
                self.attr_type(make_str(k), scope, v),
                make_str(v),
                scope,
                default.get(k),
            )
            xml_obj.append(data_element)

    def __str__(self):
        return object.__str__(self)

    def dump(self):
        self._graphml.__exit__(None, None, None)
        self._xml_base.__exit__(None, None, None)


# Choose a writer function for default
if lxmletree is None:
    write_graphml = write_graphml_xml
else:
    write_graphml = write_graphml_lxml

# fixture for pytest
def setup_module(module):
    import pytest

    xml.etree.ElementTree = pytest.importorskip("xml.etree.ElementTree")


# fixture for pytest
def teardown_module(module):
    import os

    try:
        os.unlink("test.graphml")
    except:
        pass
