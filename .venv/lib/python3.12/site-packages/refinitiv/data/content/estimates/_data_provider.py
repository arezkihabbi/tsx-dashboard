from functools import partial

from ._enums import Package
from .._content_data_provider import ContentDataProvider
from .._error_parser import ErrorParser
from .._universe_content_validator import UniverseContentValidator
from ..._tools import (
    universe_arg_parser,
    make_enum_arg_parser,
    extend_params,
    ValueParamItem,
)
from ...delivery._data._data_provider import (
    RequestFactory,
    ValidatorContainer,
)

package_estimates_arg_parser = make_enum_arg_parser(Package)

estimates_query_params = [
    ValueParamItem(
        "universe",
        function=partial(universe_arg_parser.get_str, delim=","),
        is_true=lambda universe: universe is not None,
    ),
    ValueParamItem("package", function=package_estimates_arg_parser.get_str),
]


class EstimatesRequestFactory(RequestFactory):
    @property
    def query_params_config(self):
        return estimates_query_params

    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)


estimates_data_provider = ContentDataProvider(
    request=EstimatesRequestFactory(),
    validator=ValidatorContainer(content_validator=UniverseContentValidator()),
    parser=ErrorParser(),
)
