# -*- coding: utf-8 -*-

"""
biothings_explorer.utils
~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used within bioThings_explorer
that are also useful for external consumption.
"""
from os.path import commonprefix

from .config import id_ranks
        

def get_primary_id_from_equivalent_ids(equivalent_ids, _type):
    """find primary id from equivalent id dict
    
    params
    ------
    equivalent_ids: a dictionary containing all equivalent ids of a bio-entity
    _type: the type of the bio-entity
    """
    if not equivalent_ids:
        return None
    if _type in id_ranks:
        id_rank = [('bts:' + _item) for _item in id_ranks.get(_type)]
        # loop through id_rank, if the id is found in equivalent ids, return it
        for _item in id_rank:
            if equivalent_ids.get(_item):
                return (_item[4:] + ':' + str(equivalent_ids[_item][0]))
    # if no id found, return a random one from equivalent ids
    for k, v in equivalent_ids.items():
        if v:
            return (k[4:] + ':' + str(v[0]))
    
def get_name_from_equivalent_ids(equivalent_ids, input_label):
    """find name from equivalent id dict
    
    params
    ------
    equivalent_ids: a dictionary containing all equivalent ids of a bio-entity
    input_label: desginated input_label
    """
    if input_label:
        return input_label
    if not equivalent_ids:
        return "unknown"
    if equivalent_ids.get('bts:symbol'):
        return equivalent_ids.get('bts:symbol')[0]
    elif equivalent_ids.get('bts:name'):
        return equivalent_ids.get('bts:name')[0]
    else:
        for v in equivalent_ids.values():
            if v:
                if type(v) == list:
                    return v[0]
                else:
                    return v
        return "unknown"



