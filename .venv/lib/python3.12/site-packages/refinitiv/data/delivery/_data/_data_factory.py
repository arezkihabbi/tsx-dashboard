from typing import Any, Generic, TYPE_CHECKING, Type, TypeVar

from ._endpoint_data import EndpointData

if TYPE_CHECKING:
    from ._response import Response

TypeData = TypeVar("TypeData")


class BaseDataFactory(Generic[TypeData]):
    data_class: Type[TypeData]

    def create_data(self, raw: Any, owner_: "Response", **kwargs) -> TypeData:
        if owner_.is_success:
            return self.create_data_success(raw, owner_=owner_, **kwargs)
        else:
            return self.create_data_fail(raw, owner_=owner_, **kwargs)

    def create_data_success(self, raw: Any, owner_: "Response", **kwargs) -> TypeData:
        return self.data_class(raw=raw, _owner=owner_, _kwargs=kwargs)

    def create_data_fail(self, raw: Any, owner_: "Response", **kwargs) -> TypeData:
        return self.data_class(raw=raw or {}, _owner=owner_, _kwargs=kwargs)


class DataFactory(BaseDataFactory[EndpointData]):
    def __init__(self, data_class: Type[EndpointData] = None):
        self.data_class = data_class or EndpointData
