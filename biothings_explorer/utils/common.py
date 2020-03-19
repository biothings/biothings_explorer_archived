"""This file covers some common utils functions for BioThings Explorer"""

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
    """Convert a list of tuples back to a single dictionary"""
    return dict(tuple_list)