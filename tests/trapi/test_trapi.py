import unittest
from biothings_explorer.trapi import TRAPI


class TestTRAPIClass(unittest.TestCase):
    def test_if_url_not_string_raise_exception(self):
        tp = TRAPI()
        with self.assertRaises(Exception):
            tp.url = {"a": "b"}
