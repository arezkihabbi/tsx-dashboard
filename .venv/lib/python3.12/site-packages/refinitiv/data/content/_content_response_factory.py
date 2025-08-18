from typing import TYPE_CHECKING, Type

from ._content_data_factory import ContentDataFactory
from ..delivery._data._response import Response
from ..delivery._data._response_factory import BaseResponseFactory

if TYPE_CHECKING:
    from ..delivery._data._endpoint_data import EndpointData


class ContentResponseFactory(ContentDataFactory, BaseResponseFactory[Response]):
    def __init__(
        self,
        response_class: Type["Response"] = None,
        data_class: Type["EndpointData"] = None,
    ):
        self.response_class = response_class or Response
        ContentDataFactory.__init__(self, data_class)
