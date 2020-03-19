# -*- coding: utf-8 -*-
"""
Organize BioThings Schema into networkx graphs.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

from itertools.chain import from_iterable

from biothings_schema import Schema
import networkx as nx


class SchemaExtractor():

    """Extract BioThings Schema and construct networkx graph."""

    def __init__(self, schema):
        """Load biothings schema."""
        self.se = Schema(schema)
        # get all properties which are descendants of "identifier" property
        self.all_ids = self.se.get_property('identifier',
                                            output_type="curie").descendant_properties

    def find_descendants(self, lst):
        """
        Find all descendants for a list of schemaclass classes.

        :arg list lst: a list of schemaclass classes
        """
        # if input is empty list, return an empty set
        if not lst:
            return set()
        # find descendant of each class and then merge together into a set
        dsc_lst = set(from_iterable([self.se.get_class(_cls, output_type="curie").descendant_classes for _cls in lst]))
        return dsc_lst

    def find_cls_ids(self, _cls):
        """
        Find all identifiers which belongs to a class.
    
        :arg cls _cls: a SchemaClass instance
        """
        # get all properties belong to the cls which are descendants of "identifiers"
        properties = [_prop['curie'] for _prop in self.se.get_class(_cls).list_properties(group_by_class=False) if _prop and _prop['curie'] in self.all_ids]
        return properties

    def schema2networkx(self):
        """Convert schema into a networkx graph.

        Logics
        ~~~~~~
        Each identifier represents a node
        node properties include its semantic type (class name)
        The edge is represented by non-identifier properties
        """
        G = nx.DiGraph()
        # list all properties defined in the schema
        properties = self.se.list_all_defined_properties()
        for _property in properties:
            if _property not in self.all_ids:
                # find all descendants of domain classes
                input_clses = set([_cls.name for _cls in _property.domain if _cls.uri in self.se.full_class_only_graph])
                input_clses |= self.find_descendants(input_clses)
                # find all descendants of range classes
                output_clses = set([_cls.name for _cls in _property.range if _cls.uri in self.se.full_class_only_graph])
                output_clses |= self.find_descendants(output_clses)
                if input_clses and output_clses:
                    input_ids = set(from_iterable([self.find_cls_ids(_cls) for _cls in input_clses]))
                    output_ids = set(from_iterable([self.find_cls_ids(_cls) for _cls in output_clses]))
                    if input_ids and output_ids:
                        G.add_edges_from(zip(input_ids, output_ids),
                                         label=_property.label)
                else:
                    continue
            else:
                continue
        return G
