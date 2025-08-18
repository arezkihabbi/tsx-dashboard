from typing import Any, TYPE_CHECKING, Type

from ._content_data import Data
from ._df_builder import build_empty_df
from ..delivery._data._data_factory import BaseDataFactory

if TYPE_CHECKING:
    from ..delivery._data._endpoint_data import EndpointData


class ContentDataFactory(BaseDataFactory[Data]):
    def __init__(self, data_class: Type["EndpointData"] = None):
        self.data_class = data_class or Data

    def get_dfbuilder(self, content_type=None, dfbuild_type=None, **kwargs):
        from ._df_builder_factory import get_dfbuilder, DFBuildType
        from .._content_type import ContentType

        content_type = content_type or kwargs.get("__content_type__", ContentType.DEFAULT)
        dfbuild_type = dfbuild_type or kwargs.get("__dfbuild_type__", DFBuildType.DATE_AS_INDEX)
        return get_dfbuilder(content_type, dfbuild_type)

    def create_data_success(self, raw: Any, **kwargs) -> Data:
        return self.data_class(raw=raw, _dfbuilder=self.get_dfbuilder(**kwargs), _kwargs=kwargs)

    def create_data_fail(self, raw: Any, **kwargs) -> Data:
        raw = raw if raw else {}
        return self.data_class(raw=raw, _dfbuilder=build_empty_df, _kwargs=kwargs)
