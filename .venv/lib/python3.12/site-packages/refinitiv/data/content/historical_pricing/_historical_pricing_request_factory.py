from functools import partial
from typing import Union

from ._enums import adjustments_arg_parser, market_sessions_arg_parser, event_types_arg_parser
from ..._content_type import ContentType
from .._historical_data_provider import get_fields_summaries, get_fields_events
from .._intervals import DayIntervalType, Intervals, get_day_interval_type, interval_arg_parser
from ..._tools import urljoin, ParamItem, ValueParamItem, is_date_true, hp_datetime_adapter
from ...delivery._data._data_provider import RequestFactory

content_type_by_day_interval_type = {
    DayIntervalType.INTER: ContentType.HISTORICAL_PRICING_INTERDAY_SUMMARIES,
    DayIntervalType.INTRA: ContentType.HISTORICAL_PRICING_INTRADAY_SUMMARIES,
}


def get_content_type_by_interval(interval: Union[str, Intervals, DayIntervalType]) -> ContentType:
    day_interval_type = get_day_interval_type(interval)
    return content_type_by_day_interval_type.get(day_interval_type)


def check_count(value):
    if value is not None and value < 1:
        raise ValueError("Count minimum value is 1")
    return value


hp_summaries_query_params = [
    ValueParamItem(
        "interval",
        function=interval_arg_parser.get_str,
    ),
    ValueParamItem("start", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem(
        "adjustments",
        function=partial(adjustments_arg_parser.get_str, delim=","),
    ),
    ValueParamItem(
        "sessions",
        function=partial(market_sessions_arg_parser.get_str, delim=","),
    ),
    ValueParamItem("count", function=check_count),
    ParamItem("fields", function=get_fields_summaries),
]

hp_events_query_params = [
    ValueParamItem("interval", function=interval_arg_parser.get_str),
    ValueParamItem("event_types", "eventTypes", partial(event_types_arg_parser.get_str, delim=",")),
    ValueParamItem("start", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("end", function=hp_datetime_adapter.get_str, is_true=is_date_true),
    ValueParamItem("adjustments", function=partial(adjustments_arg_parser.get_str, delim=",")),
    ValueParamItem("count", function=check_count),
    ParamItem("fields", function=get_fields_events),
]


class HistoricalPricingRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        url = args[1]
        url = urljoin(url, "/{universe}")
        return url

    def get_path_parameters(self, session=None, *, universe=None, **kwargs):
        if universe is None:
            return {}
        return {"universe": universe}

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        return None

    def extend_query_parameters(self, query_parameters, extended_params=None):
        if extended_params:
            query_parameters = dict(query_parameters)
            query_parameters.update(extended_params)
            for key in ("start", "end"):
                if key in extended_params:
                    arg_date = query_parameters[key]
                    query_parameters[key] = hp_datetime_adapter.get_str(arg_date)
            query_parameters = list(query_parameters.items())

        return query_parameters


class HistoricalPricingEventsRequestFactory(HistoricalPricingRequestFactory):
    @property
    def query_params_config(self):
        return hp_events_query_params


class HistoricalPricingSummariesRequestFactory(HistoricalPricingRequestFactory):
    @property
    def query_params_config(self):
        return hp_summaries_query_params
