from enum import Enum
from typing import Callable, Union, Tuple

from ._serializable import Serializable
from ..._tools import ipa_date_adapter, ipa_datetime_adapter
from ..._types import DateTime


class IPAParamItem:
    def __init__(self, converter: Callable = None) -> None:
        self._converter = converter

    def to_kv(
        self,
        query_param_name: str,
        value: Union[DateTime, Serializable, Enum, None, bool, float, int, str],
    ) -> Tuple[str, Union[None, bool, dict, float, int, str]]:
        if self._converter:
            return query_param_name, self._converter(value)
        return query_param_name, value


param_item = IPAParamItem()
enum_param_item = IPAParamItem(lambda value: str(value) if value is not None else value)
serializable_param_item = IPAParamItem(lambda value: dict(value) if value is not None else value)
definition_param_item = IPAParamItem(
    lambda value: value._kwargs["definition"].get_dict() if value is not None else value
)
datetime_param_item = IPAParamItem(lambda value: ipa_datetime_adapter.get_str(value) if value is not None else value)
date_param_item = IPAParamItem(lambda value: ipa_date_adapter.get_str(value) if value is not None else value)
list_serializable_param_item = IPAParamItem(lambda value: [dict(v) for v in value if v] if value is not None else value)
