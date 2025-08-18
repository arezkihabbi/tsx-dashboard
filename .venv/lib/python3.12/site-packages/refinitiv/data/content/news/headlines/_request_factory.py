from . import SortOrder
from ...._tools import ParamItem, ValueParamItem, extend_params, make_enum_arg_parser, to_iso_format
from ....delivery._data._request_factory import RequestFactory

sort_order_news_arg_parser = make_enum_arg_parser(SortOrder)
news_headlines_query_parameters = [
    ParamItem("query"),
    ParamItem("count", "limit", is_true=lambda value: value is not None),
    ValueParamItem("date_from", "dateFrom", to_iso_format),
    ValueParamItem("date_to", "dateTo", to_iso_format),
    ValueParamItem("sort_order", "sort", sort_order_news_arg_parser.get_str),
    ParamItem("cursor"),
]


class NewsHeadlinesRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        return body_parameters

    @property
    def query_params_config(self):
        return news_headlines_query_parameters
