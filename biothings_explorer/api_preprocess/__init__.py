from .biolink import restructure_biolink_response
from .reasoner import restructure_reasoner_response
from .stanford import restructure_stanford_response

class APIPreprocess():

    def __init__(self, json_doc, api_type, api_name=None):
        self.api_type = api_type
        self.api_name = api_name
        self.json_doc = json_doc

    def restructure(self):
        if self.api_type == 'biolink':
            return restructure_biolink_response(self.json_doc)
        elif self.api_type == 'reasoner':
            return restructure_reasoner_response(self.json_doc)
        elif self.api_type == 'stanford':
            return restructure_stanford_response(self.json_doc)
        else:
            return self.json_doc

