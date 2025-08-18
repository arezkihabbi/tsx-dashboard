import re
from dataclasses import dataclass
from json import JSONDecodeError
from typing import TYPE_CHECKING, Tuple, Union, List, Callable

import pandas as pd
import requests

from ._enums import CustomInstrumentTypes
from ._instrument_prop_classes import Serializable
from .._content_data_provider import ContentDataProvider
from .._historical_content_validator import HistoricalContentValidator
from .._historical_data_provider import EventsDataProvider, SummariesDataProvider
from .._historical_response_factory import HistoricalResponseFactory
from .._intervals import DayIntervalType, get_day_interval_type, Intervals
from ..ipa.dates_and_calendars.holidays._holidays_data_provider import Holiday
from ..._content_type import ContentType
from ..._errors import RDError
from ..._tools import (
    get_response_reason,
    make_enum_arg_parser,
    custom_inst_datetime_adapter,
    ParamItem,
    ValueParamItem,
    EnumArgsParser,
    make_parse_enum,
    make_convert_to_enum,
    is_date_true,
    cached_property,
    extend_params,
    convert_df_columns_to_datetime,
    convert_dtypes,
)
from ...delivery._data._data_provider import (
    RequestFactory,
    Parser,
    success_http_codes,
    ContentValidator,
    ContentTypeValidator,
    ValidatorContainer,
    ParsedData,
)
from ...delivery._data._endpoint_data import RequestMethod

if TYPE_CHECKING:
    import httpx

content_type_by_day_interval_type = {
    DayIntervalType.INTER: ContentType.CUSTOM_INSTRUMENTS_INTERDAY_SUMMARIES,
    DayIntervalType.INTRA: ContentType.CUSTOM_INSTRUMENTS_INTRADAY_SUMMARIES,
}

# a20140be-3648-4892-9d1b-ce78ee8617fd
is_instrument_id = re.compile(r"[a-z0-9]{8}(-[a-z0-9]{4}){3}-[a-z0-9]{12}")

# S)INST.GESG1-0000
symbol_with_user_id = re.compile(r".*\.[A-Z0-9]+-[A-Z0-9]+")


def provide_session(func):
    def _func(value, session, *args, **kwargs):
        return func(value, session)

    return _func


def get_content_type_by_interval(interval) -> ContentType:
    day_interval_type = get_day_interval_type(interval)
    return content_type_by_day_interval_type.get(day_interval_type)


# --------------------------------------------------------------------------------------
#   Response factory
# --------------------------------------------------------------------------------------


def custom_instruments_build_df(content_data: dict, **kwargs) -> pd.DataFrame:
    if isinstance(content_data, dict):
        content_data = [content_data]
    dataframe = pd.DataFrame(content_data)
    dataframe = convert_dtypes(dataframe)
    return dataframe


def custom_instruments_search_build_df(content_data: dict, **kwargs) -> pd.DataFrame:
    if "data" in content_data:
        content_data = content_data["data"]
    dataframe = pd.DataFrame(content_data)
    dataframe = convert_dtypes(dataframe)
    return dataframe


def custom_instruments_intervals_build_df(content_data: dict, **kwargs) -> pd.DataFrame:
    data = content_data.get("data")
    headers = content_data.get("headers", [])
    columns = [header.get("name") for header in headers]
    dataframe = pd.DataFrame(data, columns=columns)
    convert_df_columns_to_datetime(dataframe, entry="DATE", utc=True, delete_tz=True)
    dataframe.fillna(pd.NA, inplace=True)
    return dataframe


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------


def convert_to_symbol(symbol, session=None, uuid=""):
    # "MyNewInstrument"
    retval = symbol
    if not retval.startswith("S)"):
        retval = f"S){retval}"
    # "S)MyNewInstrument"
    if not symbol_with_user_id.match(retval) and uuid:
        retval = f"{retval}.{uuid}"
    # "S)MyNewInstrument.GE-1234"
    return retval


def convert_to_holidays(array: List[Union[dict, Holiday]]) -> List:
    converted_holidays = []
    for holiday in array:
        if isinstance(holiday, dict):
            if "date" in holiday and "reason" in holiday:
                converted_holidays.append(holiday)
            else:
                raise ValueError("Holiday object should have 'date' and 'reason'")
        elif isinstance(holiday, Holiday):
            converted_holidays.append({"date": holiday.date, "reason": holiday.name})
        else:
            raise TypeError("holidays parameter can take only dict or Holiday objects")
    return converted_holidays


def convert_to_dict(obj: Union[dict, dataclass]) -> dict:
    if isinstance(obj, Serializable):
        return obj._to_dict()
    elif isinstance(obj, dict):
        return obj
    raise TypeError(f"Parameter can take only dict or UDC/Basket object")


def get_valid_symbol(symbol, uuid):
    return convert_to_symbol(symbol, uuid=uuid)


def get_valid_symbol_request(symbol, session):
    return convert_to_symbol(symbol, session)


class BaseRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = super().get_url(*args, **kwargs)
        if self.get_request_method(**kwargs) != RequestMethod.POST:
            url += "/{universe}"
        return url

    def get_path_parameters(self, session, *, universe=None, **kwargs):
        if self.get_request_method(**kwargs) == RequestMethod.POST:
            return {}

        if universe is None:
            raise RDError(-1, "universe can't be None")

        if not is_instrument_id.match(universe):
            universe = get_valid_symbol_request(universe, session)

        return {"universe": universe}

    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def extend_body_parameters(self, body_parameters, **kwargs):
        return body_parameters


custom_inst_type_arg_parser = EnumArgsParser(
    parse=make_parse_enum(CustomInstrumentTypes),
    parse_to_enum=make_convert_to_enum(CustomInstrumentTypes),
)


class CustomInstsRequestFactory(BaseRequestFactory):
    @property
    def body_params_config(self):
        return custom_insts_body_params

    def get_body_parameters(self, session, *args, **kwargs):
        body_parameters = {}
        if self.get_request_method(**kwargs) not in {
            RequestMethod.POST,
            RequestMethod.PUT,
        }:
            return body_parameters

        return super().get_body_parameters(session, *args, **kwargs)

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            result = dict(body_parameters)
            result.update(extended_params)
            return result
        return body_parameters


# --------------------------------------------------------------------------------------
#   Raw data parser
# --------------------------------------------------------------------------------------


class CustomInstsParser(Parser):
    def parse_raw_response(self, raw_response: "httpx.Response") -> Tuple[bool, ParsedData]:
        is_success = False

        if raw_response is None:
            return is_success, ParsedData({}, {})

        is_success = raw_response.status_code in success_http_codes + [requests.codes.no_content]

        if is_success:
            parsed_data = self.process_successful_response(raw_response)

        else:
            parsed_data = self.process_failed_response(raw_response)

        return is_success, parsed_data

    def process_failed_response(self, raw_response: "httpx.Response") -> ParsedData:
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }

        try:
            content_data = raw_response.json()
            if isinstance(content_data, list):
                content_data = content_data[0]
            content_error = content_data.get("error")

            if content_error:
                status["error"] = content_error
                error_code = content_error.get("code")
                if isinstance(error_code, str) and not error_code.isdigit():
                    error_code = raw_response.status_code
                error_message = content_error.get("message")
                errors = content_error.get("errors", {})
                errors = [error.get("reason") for error in errors if error]
                if errors:
                    errors = "\n".join(errors)
                    error_message = f"{error_message}: {errors}"
            elif "state" in content_data:
                state = content_data.get("state", {})
                error_code = state.get("code")
                data = content_data.get("data", [])
                reasons = [_data.get("reason", "") for _data in data]
                reason = "\n".join(reasons)
                error_message = f"{state.get('message')}: {reason}"
            else:
                error_code = raw_response.status_code
                error_message = raw_response.text

        except (TypeError, JSONDecodeError):
            error_code = raw_response.status_code
            error_message = raw_response.text

        if error_code == 403:
            if not error_message.endswith("."):
                error_message += ". "
            error_message += "Contact Refinitiv to check your permissions."

        return ParsedData(status, raw_response, error_codes=error_code, error_messages=error_message)


# --------------------------------------------------------------------------------------
#   Content data validator
# --------------------------------------------------------------------------------------


class CustomInstsContentValidator(ContentValidator):
    @classmethod
    def content_data_is_not_none(cls, data: ParsedData) -> bool:
        if data.content_data is None and data.status.get("http_status_code") != 204:
            data.error_codes = 1
            data.error_messages = "Content data is None"
            return False
        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [self.content_data_is_not_none]


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------

interval_arg_parser = make_enum_arg_parser(Intervals, can_be_lower=True)


class CustomInstsSearchRequestFactory(RequestFactory):
    def get_query_parameters(self, *args, **kwargs):
        access = kwargs.get("access")
        return [
            ("access", access),
        ]

    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def extend_body_parameters(self, body_parameters, **kwargs):
        return body_parameters


def check_count(value):
    if value is not None and value < 1:
        raise ValueError("Count minimum value is 1")
    return value


custom_insts_events_query_params = [
    ValueParamItem("start", function=custom_inst_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=custom_inst_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("count", function=check_count),
]
custom_insts_summaries_query_params = [
    ValueParamItem("interval", function=interval_arg_parser.get_str),
    ValueParamItem("start", function=custom_inst_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=custom_inst_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("count", function=check_count),
]

custom_insts_body_params = [
    ParamItem("exchange_name", "exchangeName"),
    ParamItem("instrument_name", "instrumentName"),
    ParamItem("time_zone", "timeZone"),
    ValueParamItem("type_", "type", custom_inst_type_arg_parser.parse),
    ParamItem("symbol", function=provide_session(convert_to_symbol)),
    ParamItem("currency"),
    ParamItem("description"),
    ParamItem("formula"),
    ValueParamItem("holidays", function=convert_to_holidays),
    ValueParamItem("basket", function=convert_to_dict),
    ValueParamItem("udc", function=convert_to_dict),
]

simple_custom_insts_body_params_config = [
    ParamItem("exchangeName"),
    ParamItem("instrumentName"),
    ParamItem("timeZone"),
    ParamItem("type"),
    ParamItem("symbol", function=provide_session(convert_to_symbol)),
    ParamItem("currency"),
    ParamItem("description"),
    ParamItem("formula"),
    ValueParamItem("udc", function=convert_to_dict),
    ValueParamItem("basket", function=convert_to_dict),
    ValueParamItem("holidays", function=convert_to_holidays),
]


class CustomInstsEventsRequestFactory(BaseRequestFactory):
    @property
    def query_params_config(self):
        return custom_insts_events_query_params


class CustomInstsSummariesRequestFactory(BaseRequestFactory):
    @property
    def query_params_config(self):
        return custom_insts_summaries_query_params


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------

custom_instrument_data_provider = ContentDataProvider(
    request=CustomInstsRequestFactory(),
    parser=CustomInstsParser(),
    validator=ValidatorContainer(
        content_validator=CustomInstsContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", ""}),
    ),
)

custom_instrument_search_data_provider = ContentDataProvider(
    request=CustomInstsSearchRequestFactory(),
    parser=CustomInstsParser(),
    validator=ValidatorContainer(
        content_validator=CustomInstsContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", ""}),
    ),
)

custom_instruments_events_data_provider = EventsDataProvider(
    request=CustomInstsEventsRequestFactory(),
    parser=CustomInstsParser(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)

custom_instruments_intraday_summaries_data_provider = SummariesDataProvider(
    request=CustomInstsSummariesRequestFactory(),
    parser=CustomInstsParser(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)

custom_instruments_interday_summaries_data_provider = SummariesDataProvider(
    request=CustomInstsSummariesRequestFactory(),
    parser=CustomInstsParser(),
    response=HistoricalResponseFactory(),
    validator=HistoricalContentValidator(),
)
