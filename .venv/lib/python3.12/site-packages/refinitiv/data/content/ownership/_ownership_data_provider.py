from typing import List

from ._df_builder import concat_ownership_dfs
from ._enums import StatTypes, Frequency, SortOrder
from .._content_data_factory import ContentDataFactory
from .._content_data_provider import ContentDataProvider
from .._error_parser import ErrorParser
from .._universe_content_validator import UniverseContentValidator
from ..._tools import (
    ArgsParser,
    extend_params,
    ValueParamItem,
    ParamItem,
    universe_arg_parser,
    make_enum_arg_parser,
    ownership_datetime_adapter,
)
from ...delivery._data._data_provider import RequestFactory, ValidatorContainer
from ...delivery._data._response import create_response, Response

MAX_LIMIT = 100


def parse_str(param):
    if isinstance(param, str):
        return param
    raise ValueError(f"Invalid type, expected str: {type(param)} is given")


universe_ownership_arg_parser = ArgsParser(parse_str)


def get_unique_universe(universe):
    if isinstance(universe, list):
        universe = list(dict.fromkeys(universe))
    return universe_arg_parser.get_str(universe, delim=",")


class OwnershipRequestFactory(RequestFactory):
    query_params_config = [
        ValueParamItem(
            "universe",
            function=get_unique_universe,
            is_true=lambda universe: universe is not None,
        ),
        ValueParamItem("stat_type", "statType", function=make_enum_arg_parser(StatTypes).get_str),
        ParamItem("offset"),
        ParamItem("limit"),
        ValueParamItem("sort_order", "sortOrder", make_enum_arg_parser(SortOrder).get_str),
        ValueParamItem("frequency", function=make_enum_arg_parser(Frequency).get_str),
        ValueParamItem("start", function=ownership_datetime_adapter.get_str),
        ValueParamItem("end", function=ownership_datetime_adapter.get_str),
        ParamItem("count"),
    ]

    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)


class OwnershipDataFactoryMultiResponse(ContentDataFactory):
    def get_dfbuilder(self, **__):
        return concat_ownership_dfs


class OwnershipDataProvider(ContentDataProvider):
    data_factory_multi_response = OwnershipDataFactoryMultiResponse()

    def create_response(self, responses: List[Response], kwargs: dict) -> Response:
        if len(responses) == 1:
            return responses[0]

        kwargs["responses"] = responses
        return create_response(responses, self.data_factory_multi_response, kwargs)

    def get_data(self, *args, **kwargs):
        limit = kwargs.get("limit")

        if limit is None:
            response = super().get_data(*args, **kwargs)

        else:
            responses = []
            for offset in range(0, limit, MAX_LIMIT):
                kwargs["limit"] = MAX_LIMIT if offset < limit - MAX_LIMIT else limit - offset
                kwargs["offset"] = offset if offset else None
                response = super().get_data(*args, **kwargs)
                responses.append(response)

            response = self.create_response(responses, kwargs)

        return response

    async def get_data_async(self, *args, **kwargs):
        limit = kwargs.get("limit")

        if limit is None:
            response = await super().get_data_async(*args, **kwargs)

        else:
            responses = []
            for offset in range(0, limit, MAX_LIMIT):
                kwargs["limit"] = MAX_LIMIT if offset < limit - MAX_LIMIT else limit - offset
                kwargs["offset"] = offset if offset else None
                response = await super().get_data_async(*args, **kwargs)
                responses.append(response)

            response = self.create_response(responses, kwargs)

        return response


ownership_data_provider = OwnershipDataProvider(
    request=OwnershipRequestFactory(),
    validator=ValidatorContainer(content_validator=UniverseContentValidator()),
    parser=ErrorParser(),
)
