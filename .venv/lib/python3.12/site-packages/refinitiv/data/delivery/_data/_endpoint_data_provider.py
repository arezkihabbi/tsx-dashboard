from typing import List, Callable, TYPE_CHECKING

from ._data_provider import (
    DataProvider,
    ContentValidator,
    ValidatorContainer,
    RequestFactory,
)
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._parsed_data import ParsedData


class EndpointValidator(ContentValidator):
    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return []


class EndpointRequestFactory(RequestFactory):
    def get_body_parameters(self, *args, **kwargs):
        return kwargs.get("body_parameters") or {}

    def get_query_parameters(self, *args, **kwargs):
        return kwargs.get("query_parameters") or []

    def extend_body_parameters(self, body_params, **kwargs):
        return body_params


endpoint_data_provider = DataProvider(
    validator=ValidatorContainer(content_validator=EndpointValidator()),
    request=EndpointRequestFactory(),
)
