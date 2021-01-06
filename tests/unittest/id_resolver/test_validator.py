import unittest
from biothings_explorer.resolve_ids.validator import Validator
from biothings_explorer.exceptions.id_resolver import InvalidIDResolverInputError


class TestValidatorClass(unittest.TestCase):
    def test_error_should_raise_if_input_is_not_dict(self):
        input_ids = ["123"]
        validator = Validator(input_ids)
        self.assertRaises(InvalidIDResolverInputError, validator.validate)

    def test_error_should_raise_if_values_of_input_is_not_list(self):
        input_ids = {"Gene": "123"}
        validator = Validator(input_ids)
        self.assertRaises(InvalidIDResolverInputError, validator.validate)

    def test_error_should_raise_if_items_of_the_values_of_input_is_not_str(self):
        input_ids = {"Gene": [123]}
        validator = Validator(input_ids)
        self.assertRaises(InvalidIDResolverInputError, validator.validate)

    def test_error_should_raise_if_items_of_the_values_of_input_is_not_curie(self):
        input_ids = {"Gene": ["123"]}
        validator = Validator(input_ids)
        self.assertRaises(InvalidIDResolverInputError, validator.validate)

    def test_pass_if_items_of_the_values_of_input_is_curie(self):
        input_ids = {"Gene": ["NCBIGene:123"]}
        validator = Validator(input_ids)
        try:
            validator.validate()
        except InvalidIDResolverInputError:
            self.fail("validator raised execption unexpectedly")

    def test_invalid_prefix_should_be_classified_as_invalid(self):
        input_ids = {"Gene": ["NCBIGene:123", "ncbigene:123"]}
        validator = Validator(input_ids)
        validator.validate()
        self.assertEqual(validator.get_invalid_inputs(), {"Gene": ["ncbigene:123"]})

    def test_invalid_semantic_type_should_be_classified_as_invalid(self):
        input_ids = {"Gene1": ["NCBIGene:123"]}
        validator = Validator(input_ids)
        validator.validate()
        self.assertEqual(validator.get_invalid_inputs(), input_ids)

    def test_valid_inputs_should_be_classified_as_valid(self):
        input_ids = {"Gene": ["NCBIGene:123", "ncbigene:123"]}
        validator = Validator(input_ids)
        validator.validate()
        self.assertEqual(validator.get_valid_inputs(), {"Gene": ["NCBIGene:123"]})

