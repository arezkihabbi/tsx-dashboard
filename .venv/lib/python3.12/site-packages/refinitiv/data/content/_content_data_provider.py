from typing import Union, TYPE_CHECKING

from ._content_response_factory import ContentResponseFactory
from ..delivery._data._data_provider import DataProvider

if TYPE_CHECKING:
    from ..delivery._data._response_factory import BaseResponseFactory
    from ..delivery._data._request_factory import RequestFactory
    from ..delivery._data._validators import ValidatorContainer, BaseValidator
    from ..delivery._data._connection import HttpSessionConnection
    from ..delivery._data._raw_data_parser import Parser


class ContentDataProvider(DataProvider):
    def __init__(
        self,
        connection: "HttpSessionConnection" = None,
        request: "RequestFactory" = None,
        response: "BaseResponseFactory" = None,
        parser: "Parser" = None,
        validator: Union["BaseValidator", "ValidatorContainer"] = None,
    ):
        response = response or ContentResponseFactory()
        super().__init__(
            connection=connection,
            request=request,
            response=response,
            parser=parser,
            validator=validator,
        )
