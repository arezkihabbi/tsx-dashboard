import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, TypeVar, Generic, Any, Union

from ._endpoint_data import Error
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._data_factory import BaseDataFactory
    import httpx

TypeData = TypeVar("TypeData")


@dataclass
class Response(Generic[TypeData]):
    is_success: bool
    raw: Union[List["httpx.Response"], "httpx.Response"]
    errors: List[Error]
    closure: Union[str, None]
    requests_count: int
    _data_factory: "BaseDataFactory"
    _kwargs: dict
    _raw: Any
    _request_message: Union[List["httpx.Request"], "httpx.Request"]
    _http_response: Union[List["httpx.Response"], "httpx.Response"]
    _http_headers: Union[List["httpx.Headers"], "httpx.Headers"]
    _http_status: Union[List[dict], dict]

    @property
    def request_message(self):
        warnings.warn(
            "The request_message property will be removed in future library version v2.0. "
            "Please use raw.request instead.",
            category=FutureWarning,
        )
        return self._request_message

    @property
    def http_response(self):
        warnings.warn(
            "The http_response property will be removed in future library version v2.0. " "Please use raw instead.",
            category=FutureWarning,
        )
        return self._http_response

    @property
    def http_headers(self):
        warnings.warn(
            "The http_headers property will be removed in future library version v2.0. "
            "Please use raw.headers instead.",
            category=FutureWarning,
        )
        return self._http_headers

    @property
    def http_status(self):
        warnings.warn(
            "The http_status property will be removed in future library version v2.0. "
            "Please use raw.status_code and raw.reason_phrase instead.",
            category=FutureWarning,
        )
        return self._http_status

    @cached_property
    def data(self) -> TypeData:
        return self._data_factory.create_data(self._raw, owner_=self, **self._kwargs)


def create_response(responses: List[Response], data_factory: "BaseDataFactory", kwargs: dict) -> Response:
    from ._response_factory import get_closure

    raws = []
    raw = []
    request_messages = []
    http_responses = []
    http_statuses = []
    http_headers = []
    errors = []
    is_success = False
    closure = None
    once = False

    for response in responses:
        is_success = is_success or response.is_success
        raws.append(response.data.raw)
        if response.errors:
            errors += response.errors

        raw.append(response.raw)

        # will remove
        http_responses.append(response._http_response)
        request_messages.append(response._request_message)
        http_statuses.append(response._http_status)
        http_headers.append(response._http_headers)

        if not once:
            closure = get_closure(response.raw)
            once = True

    return Response(
        is_success,
        raw,
        errors,
        closure=closure,
        requests_count=len(responses),
        _data_factory=data_factory,
        _kwargs=kwargs,
        _raw=raws,
        _request_message=request_messages,
        _http_response=http_responses,
        _http_headers=http_headers,
        _http_status=http_statuses,
    )
