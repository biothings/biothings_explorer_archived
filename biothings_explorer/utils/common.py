"""This file covers some common utils functions for BioThings Explorer"""

from os.path import commonprefix
from ..config import id_ranks


def add_s(num: int) -> str:
    """Add 's' if num is more than one.

    :param: num: An integer representing count
    """
    if not isinstance(num, int):
        return ''
    if num <= 1:
        return ''
    else:
        return 's'


def dict2listoftuples(py_dict: dict) -> list:
    """Convert a single python dictionary into a list of tuples.

    :param: py_dict: a single python dictionary
    """
    return [(k, v) for k, v in py_dict.items()]


def listoftuples2dict(tuple_list: list) -> dict:
    """Convert a list of tuples back to a single dictionary.

    :param: tuple_list: a list of tuples
    """
    try:
        return dict(tuple_list)
    except ValueError:
        raise ValueError("The input must a list of tuples \
                         with each tuple of length 2")


def unlist(d: dict) -> dict:
    """Find all appearance of single element list in a dictionary and unlist it.

    :param: d: a python dictionary to be unlisted
    """
    if type(d) == list:
        if len(d) == 1:
            return d[0]
        else:
            return d
    elif type(d) == dict:
        for key, val in d.items():
            if isinstance(val, list):
                if len(val) == 1:
                    d[key] = unlist(val[0])
            elif isinstance(val, dict):
                unlist(val)
        return d
    else:
        return d


def find_longest_common_path(paths) -> str:
    """Find longest common path among a list of paths.

    :param: paths: a list of paths, with '.' as the separator
    """
    return commonprefix(paths).rsplit('.', 1)[0]


def get_dict_values(py_dict: dict,
                    excluded_keys: list = ["@type", "@input",
                                           "$source"]) -> list:
    """Retrieve the values of a python dictionary.

    :param: py_dict: a python dictionary
    :param: excluded_keys: a list of keys to be excluded, \
        meaning the values of these keys should be excluded
    """
    return [v for k, v in py_dict.items() if k not in excluded_keys]


def get_primary_id_from_equivalent_ids(equivalent_ids: dict, _type: str):
    """find primary id from equivalent id dict

    :param: equivalent_ids: a dictionary containing all equivalent ids of a bio-entity
    :param: _type: the type of the bio-entity
    """
    if not equivalent_ids:
        return None
    if _type in id_ranks:
        id_rank = id_ranks.get(_type)
        # loop through id_rank, return the first found id
        for _item in id_rank:
            if equivalent_ids.get(_item):
                return (_item + ':' + str(equivalent_ids[_item][0]))
    # if no id from id_rank found, return a random one from equivalent ids
    for k, v in equivalent_ids.items():
        if v:
            return (k[4:] + ':' + str(v[0]))


def get_name_from_equivalent_ids(equivalent_ids, input_label):
    """Find name from equivalent id dict.

    :param: equivalent_ids: a dictionary containing all equivalent ids of a bio-entity.
    :param: input_label: desginated input_label
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
