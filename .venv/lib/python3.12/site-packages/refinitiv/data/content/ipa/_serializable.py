from abc import abstractmethod, ABC
from typing import List, Tuple, Union


class ObjectDefinition(ABC):
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

    def _set_parameter(self, name, value):
        if value or isinstance(value, int):
            self._dict[name] = value

        elif self._dict.get(name):
            self._dict.pop(name)


class Serializable:
    def _to_dict(self) -> dict:
        return dict(self)

    @abstractmethod
    def _get_items(self) -> List[Tuple[str, Union[str, float, int, None]]]:
        pass

    def __iter__(self):
        return iter(((key, value) for key, value in self._get_items() if value is not None))

    def get_dict(self) -> dict:
        return self._to_dict()

    @classmethod
    def from_json(cls, json_params):
        return ObjectDefinition().from_json(json_params)
