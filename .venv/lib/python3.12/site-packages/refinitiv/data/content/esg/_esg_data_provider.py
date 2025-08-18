from functools import partial

from .._content_data_provider import ContentDataProvider
from .._error_parser import ErrorParser
from .._universe_content_validator import UniverseContentValidator
from ..._tools import universe_arg_parser, ValueParamItem, ParamItem
from ...delivery._data._data_provider import RequestFactory, ValidatorContainer


# ---------------------------------------------------------------------------
#   Request
# ---------------------------------------------------------------------------

esg_query_params = [
    ValueParamItem("universe", function=partial(universe_arg_parser.get_str, delim=",")),
    ParamItem("start"),
    ParamItem("end"),
]


class ESGRequestFactory(RequestFactory):
    @property
    def query_params_config(self):
        return esg_query_params


# ---------------------------------------------------------------------------
#   Provider
# ---------------------------------------------------------------------------

esg_data_provider = ContentDataProvider(
    request=ESGRequestFactory(),
    validator=ValidatorContainer(content_validator=UniverseContentValidator()),
    parser=ErrorParser(),
)
