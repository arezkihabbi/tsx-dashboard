from itertools import zip_longest
from typing import Generic, List, TYPE_CHECKING, Type, TypeVar, Union

from ._data_factory import BaseDataFactory
from ._endpoint_data import EndpointData, Error
from ._response import Response

if TYPE_CHECKING:
    from ._parsed_data import ParsedData
    import httpx

TypeResponse = TypeVar("TypeResponse")


def get_closure(response: Union[List["httpx.Response"], "httpx.Response"]) -> Union[str, List[str]]:
    if isinstance(response, list):
        return [resp.request.headers.get("closure") for resp in response]
    return response.request.headers.get("closure")


class BaseResponseFactory(Generic[TypeResponse]):
    response_class: Type[TypeResponse]

    @staticmethod
    def get_raw(parsed_data: "ParsedData") -> Union[dict, list, str]:
        return parsed_data.content_data

    def create_response(self, is_success: bool, parsed_data: "ParsedData", **kwargs) -> TypeResponse:
        if is_success:
            return self.create_success(parsed_data, **kwargs)
        else:
            return self.create_fail(parsed_data, **kwargs)

    def create_success(self, parsed_data: "ParsedData", **kwargs) -> TypeResponse:
        return self._do_create_response(True, self.get_raw(parsed_data), parsed_data, **kwargs)

    def create_fail(self, parsed_data: "ParsedData", **kwargs) -> TypeResponse:
        return self._do_create_response(False, parsed_data.content_data or {}, parsed_data, **kwargs)

    def _do_create_response(
        self,
        is_success: bool,
        raw: Union[dict, list, str],
        parsed_data: "ParsedData",
        **kwargs,
    ) -> TypeResponse:
        http_response = parsed_data.raw_response
        return self.response_class(
            is_success,
            raw=http_response,
            errors=[Error(code, msg) for code, msg in zip_longest(parsed_data.error_codes, parsed_data.error_messages)],
            closure=get_closure(http_response),
            requests_count=1,
            _data_factory=self,
            _kwargs=kwargs,
            _raw=raw,
            _request_message=http_response.request,
            _http_response=http_response,
            _http_headers=http_response.headers,
            _http_status=parsed_data.status,
        )


class ResponseFactory(BaseDataFactory[EndpointData], BaseResponseFactory[Response]):
    def __init__(
        self,
        response_class: Type[Response] = None,
        data_class: Type[EndpointData] = None,
    ):
        self.response_class = response_class or Response
        self.data_class = data_class or EndpointData
