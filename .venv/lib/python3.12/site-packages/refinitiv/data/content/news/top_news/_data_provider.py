from dataclasses import dataclass
from typing import List

from ._top_news_headline import TopNewsHeadline
from ..._content_data import Data
from ..._content_data_provider import ContentDataProvider
from ..._content_response_factory import ContentResponseFactory
from ...._tools import cached_property, ParamItem, extend_params
from ....delivery._data._request_factory import RequestFactory


@dataclass
class TopNewsData(Data):
    @cached_property
    def headlines(self) -> "List[TopNewsHeadline]":
        return [TopNewsHeadline.from_dict(headline_data) for headline_data in self.raw.get("data", [])]


query_params = [ParamItem("revision_id", "revisionId")]


class TopNewsRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    def get_path_parameters(self, session=None, *, top_news_id=None, **kwargs):
        return {"topNewsId": top_news_id}

    def get_url(self, *args, **kwargs):
        return f"{super().get_url(*args, **kwargs)}/{{topNewsId}}"

    @property
    def query_params_config(self):
        return query_params


news_top_news_data_provider = ContentDataProvider(
    request=TopNewsRequestFactory(),
    response=ContentResponseFactory(data_class=TopNewsData),
)
