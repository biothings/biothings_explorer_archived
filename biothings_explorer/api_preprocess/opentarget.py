# -*- coding: utf-8 -*-
"""
Restructure the output from OpenTarget API.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>

"""


def restructure_opentarget_response(json_doc):
    """
    Restructure the API output from opentarget API.

    :param: json_doc: json output from opentarget API
    """
    if not json_doc.get("data"):
        return json_doc
    for _doc in json_doc['data']:
        if "drug" in _doc:
            if "CHEMBL" in _doc['drug']['id']:
                _doc['drug']['id'] = _doc['drug']['id'].split('/')[-1]
    return json_doc
