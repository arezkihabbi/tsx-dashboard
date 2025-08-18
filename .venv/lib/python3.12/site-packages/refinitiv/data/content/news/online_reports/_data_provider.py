from dataclasses import dataclass
from typing import List

from ._report import Report
from ..._content_data import Data
from ..._content_response_factory import ContentResponseFactory
from ...._tools import ParamItem, extend_params
from ....delivery._data._data_provider import DataProvider
from ....delivery._data._request_factory import RequestFactory


@dataclass
class NewsOnlineReportsData(Data):
    @property
    def reports(self) -> List[Report]:
        return [Report.from_dict(i) for i in self.raw.get("data", [])]


query_params = [ParamItem("full_content", "fullContent", is_true=lambda param: param is not None)]


class OnlineReportsRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def get_path_parameters(self, session=None, *, report_id=None, **kwargs):
        return {"reportId": report_id}

    def get_url(self, *args, **kwargs):
        return f"{super().get_url(*args, **kwargs)}/{{reportId}}"

    @property
    def query_params_config(self):
        return query_params


news_online_reports_data_provider = DataProvider(
    response=ContentResponseFactory(data_class=NewsOnlineReportsData),
    request=OnlineReportsRequestFactory(),
)
