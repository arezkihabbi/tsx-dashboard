from dataclasses import dataclass

from ._report import Report
from ...._content_data import Data
from ...._content_response_factory import ContentResponseFactory
from ....._tools import extend_params
from .....delivery._data._data_provider import DataProvider
from .....delivery._data._request_factory import RequestFactory


@dataclass
class HierarchyData(Data):
    @property
    def hierarchy(self) -> dict:
        return {
            region.get("name"): {report.get("reportId"): Report.from_dict(report) for report in region.get("reports")}
            for region in self.raw.get("data", {})
        }


class OnlineReportsRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)


news_online_reports_hierarchy_data_provider = DataProvider(
    response=ContentResponseFactory(data_class=HierarchyData),
    request=OnlineReportsRequestFactory(),
)
