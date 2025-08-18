import abc

from ..._tools import ipa_datetime_adapter, ipa_date_adapter, is_all_same_type


class ObjectDefinition(abc.ABC):
    """
    This class is designed to represent the instrument definition templates for QPS request.
    """

    @classmethod
    def from_json(cls, json_params):
        o = ObjectDefinition()
        for key, value in json_params.items():
            o._set_parameter(key, value)

        return o

    def __init__(self):
        self._dict = {}

    def __eq__(self, other):
        if hasattr(other, "_kwargs"):
            other = getattr(other, "_kwargs").get("definition")

        return self._dict == other

    def get_dict(self):
        return self._dict

    ####################################################
    # Get parameter values
    ####################################################
    def _get_parameter(self, name):
        return self._dict.get(name, None)

    def _get_enum_parameter(self, enum_type, name):
        value = self._dict.get(name, None)
        return enum_type(value) if value is not None else None

    def _get_object_parameter(self, object_type, name):
        value = self._dict.get(name, None)
        return object_type.from_json(value) if value is not None else None

    def _set_list_of_enums(self, enum_type, name, values):
        values = values or []
        self._dict[name] = []

        for item in values:
            if item is None:
                self._dict.pop(name, False)

            elif isinstance(item, enum_type):
                self._dict[name].append(item.value)

            elif item in [v.value for v in enum_type]:
                self._dict[name].append(item)

            else:
                values = [v.value for v in enum_type]
                raise TypeError(f"{name} : {values}, must be in {enum_type}{values}")

    def _get_list_of_enums(self, enum_type, name):
        enum_value = self._dict.get(name, None)
        response = []
        for item in enum_value:
            if item is not None:
                response.append(enum_type(item))

        return response

    def _get_list_parameter(self, item_type, name):
        value = self._dict.get(name, None)
        return (
            [item_type.from_json(item) if hasattr(item_type, "from_json") else item for item in value]
            if value is not None
            else None
        )

    ####################################################
    # Set parameter values
    ####################################################

    def _set_parameter(self, name, value):
        if value or isinstance(value, int):
            self._dict[name] = value

        elif self._dict.get(name):
            self._dict.pop(name)

    def _set_datetime_parameter(self, name, value):
        if value is not None:
            value = ipa_datetime_adapter.get_str(value)
        self._set_parameter(name, value)

    def _set_date_parameter(self, name, value):
        if value is not None:
            value = ipa_date_adapter.get_str(value)
        self._set_parameter(name, value)

    def _set_enum_parameter(self, enum_type, name, value):
        if value is None:
            self._dict.pop(name, False)
            return None

        result = None
        if isinstance(value, enum_type):
            result = value.value

        elif isinstance(value, str):
            value_upper = value.upper()
            upper_enum_values = {value.value.upper(): value for value in enum_type}
            if value_upper in upper_enum_values:
                result = upper_enum_values[value_upper].value

        if result:
            self._dict[name] = result
        else:
            values = [v.value for v in enum_type]
            raise TypeError(f"Parameter '{name}' of invalid type provided:'{type(value).__name__}', expected: {values}")

    def _set_object_parameter(self, object_type, name, value):
        if value is None:
            self._dict.pop(name, False)

        elif isinstance(value, object_type):
            self._dict[name] = value.get_dict()

        elif hasattr(value, "_kwargs"):
            attr = getattr(value, "_kwargs")
            self._dict[name] = attr.get("definition").get_dict()

        else:
            self._dict[name] = value

    def _set_list_parameter(self, item_type, name, value):
        if value is None:
            self._dict.pop(name, False)

        elif isinstance(value, list):
            if is_all_same_type(item_type, value):
                self._dict[name] = [item.get_dict() if hasattr(item, "get_dict") else item for item in value]

            else:
                raise TypeError(f"Not all values are type of {item_type}")

        else:
            raise TypeError(f"{name} value must be a list of {item_type}")
