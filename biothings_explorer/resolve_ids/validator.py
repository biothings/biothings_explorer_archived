from collections import defaultdict

from ..config_new import ID_RESOLVING_APIS
from ..exceptions.id_resolver import InvalidIDResolverInputError
from ..utils.common import getPrefixFromCurie


class Validator:
    def __init__(self, user_input):
        self.__user_input = user_input
        self.__valid = defaultdict(list)
        self.__invalid = defaultdict(list)

    def get_valid_inputs(self):
        return self.__valid

    def get_invalid_inputs(self):
        return self.__invalid

    def _validate_if_input_is_dict(self, user_input):
        if not isinstance(user_input, dict):
            raise InvalidIDResolverInputError(
                user_input,
                message="Your Input to ID Resolver is Invalid. It should be a dictionary!",
            )

    def _validate_if_values_of_input_is_list(self, user_input):
        for k, v in user_input.items():
            if not isinstance(v, list):
                raise InvalidIDResolverInputError(
                    user_input,
                    message="Your Input to ID Resolver is Invalid. All values of your input dictionary should be a list!",
                )

    def _validate_if_each_item_in_input_values_is_curie(self, user_input):
        for k, v in user_input.items():
            for _v in v:
                if not isinstance(_v, str) or ":" not in _v:
                    raise InvalidIDResolverInputError(
                        user_input,
                        message="Your Input to ID Resolver is Invalid. Each item in the values of your input dictionary should be a curie. Spotted {} is not a curie".format(
                            _v
                        ),
                    )

    def _check_if_semantic_type_can_be_resolved(self, user_input):
        res = {}
        for k, v in user_input.items():
            if k not in ID_RESOLVING_APIS:
                self.__invalid[k] = v
            else:
                res[k] = v
        return res

    def _check_if_prefix_can_be_resolved(self, user_input):
        for k, v in user_input.items():
            for _v in v:
                if getPrefixFromCurie(_v) not in ID_RESOLVING_APIS[k]["mapping"]:
                    self.__invalid[k].append(_v)
                else:
                    self.__valid[k].append(_v)

    def validate(self):
        self._validate_if_input_is_dict(self.__user_input)
        self._validate_if_values_of_input_is_list(self.__user_input)
        self._validate_if_each_item_in_input_values_is_curie(self.__user_input)
        tmp_valid_res = self._check_if_semantic_type_can_be_resolved(self.__user_input)
        self._check_if_prefix_can_be_resolved(tmp_valid_res)
