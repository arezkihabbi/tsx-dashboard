"""Base for templates namespaces"""
from collections import deque
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .base import TargetTemplate


class Namespace:
    def __init__(self, target=None, **kwargs):
        # Don't have an idea yet how to it better without need to pass TargetTemplate
        # to Namespace each time or creating circular dependencies
        if target is None:
            from .base import TargetTemplate

            self.target = TargetTemplate
        for key, value in kwargs.items():
            if "." in key:
                raise ValueError(f"Name in namespace can't contain dot. Value with dot encountered: {value}")
            if not isinstance(value, (Namespace, self.target)):
                raise TypeError(
                    f"Value in namespace must be either SearchTemplate or other Namespace. {type(value)} encountered"
                )

        self._data = kwargs

    def __iter__(self):
        return self._data.__iter__()

    def __getitem__(self, name: str):
        return self._data.__getitem__(name)

    def __setitem__(self, key: str, value: Union["Namespace", "TargetTemplate"]):
        self._data[key] = value

    def get(self, path: str):
        """Get namespace or key by path"""
        keys = deque(path.split("."))
        result = self
        while keys:
            result = result[keys.popleft()]
            if isinstance(result, self.target) and keys:
                return None
        return result

    def keys(self):
        return self._data.keys()
