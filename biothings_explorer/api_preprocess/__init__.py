# -*- coding: utf-8 -*-
"""
API-specific JSON response restructure.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

from .biolink import restructure_biolink_response
from .reasoner import restructure_reasoner_response
from .stanford import restructure_stanford_response
from .ctd import restructure_ctd_response
from .opentarget import restructure_opentarget_response
from .semmed import restructure_semmed_response
from .cord import restructure_cord_response
from .scibite import restructure_scibite_response

class APIPreprocess():

    """
    Restructure the output of specific APIs.
    
    This is to make sure the JSON output from these APIs could be uniformly consumed by the jsontransform module
    """

    def __init__(self, json_doc, api_type, api_name=None, output_types=None):
        """
        Load json doc and api info.

        :param: json_doc: the json_doc to be preprocessed
        :param: api_type: the type of api, e.g. biothings
        :param: api_name: optional, the name of api
        :param: output_types: specific for semmed api

        """
        self.api_type = api_type
        self.api_name = api_name
        self.json_doc = json_doc
        self.output_types = output_types

    def restructure(self):
        """Restructue API response."""
        # if input is empty, do not restructure
        if not self.json_doc:
            return self.json_doc
        # if input is a list, turn it into a dictionary
        if isinstance(self.json_doc, list) and self.api_type != "biothings":
            self.json_doc = {"data": self.json_doc}
        if self.api_type == 'biolink':
            return restructure_biolink_response(self.json_doc)
        if self.api_type == 'reasoner':
            return restructure_reasoner_response(self.json_doc)
        if self.api_type == 'stanford':
            return restructure_stanford_response(self.json_doc)
        if self.api_type == 'ctd':
            return restructure_ctd_response(self.json_doc)
        if self.api_type == 'opentarget':
            return restructure_opentarget_response(self.json_doc)
        if self.api_name[:4] == 'semm':
            return restructure_semmed_response(self.json_doc, self.output_types)
        if self.api_name[:4] == 'cord':
            return restructure_cord_response(self.json_doc, self.output_types)
        if self.api_name in ['scibite', 'scigraph', 'pharos', 'hmdb', 'hetio', 'chembio']:
            return restructure_scibite_response(self.json_doc)
        return self.json_doc

