from typing import List

from ._data import NewsHeadlinesData
from ._request_factory import NewsHeadlinesRequestFactory
from .._df_builder import concat_news_dfs
from ..._content_data_factory import ContentDataFactory
from ..._content_data_provider import ContentDataProvider
from ..._content_response_factory import ContentResponseFactory
from ..._error_parser import ErrorParser
from ....delivery._data._response import create_response, Response

MAX_LIMIT = 100


class NewsDataFactoryMultiResponse(ContentDataFactory):
    def get_dfbuilder(self, **__):
        return concat_news_dfs


class NewsHeadlinesDataProvider(ContentDataProvider):
    data_factory_multi_response = NewsDataFactoryMultiResponse(NewsHeadlinesData)

    @classmethod
    def create_response(cls, responses: List[Response], limit: int, kwargs: dict) -> Response:
        if len(responses) == 1:
            response = responses[0]
            response.data._limit = limit
            return response

        kwargs["responses"] = responses
        kwargs["limit"] = limit
        response = create_response(responses, cls.data_factory_multi_response, kwargs)
        response.data._limit = limit
        return response

    def get_data(self, *args, **kwargs):
        on_page_response = kwargs.get("on_page_response")
        limit = kwargs.get("count")
        responses = []
        cursor = True
        count = 0
        once = False

        if limit > MAX_LIMIT:
            kwargs["count"] = MAX_LIMIT

        while (count < limit and cursor) or not once:
            if not once:
                once = True
            response = super().get_data(*args, **kwargs)
            responses.append(response)

            if on_page_response:
                on_page_response(self, response)

            meta = response.data.raw.get("meta", {})
            count += meta.get("count", 0)
            cursor = meta.get("next")
            kwargs = {
                "cursor": cursor,
                "__content_type__": kwargs.get("__content_type__"),
            }

        return self.create_response(responses, limit, kwargs)

    async def get_data_async(self, *args, **kwargs):
        on_page_response = kwargs.get("on_page_response")
        limit = kwargs.get("count")
        responses = []
        cursor = True
        count = 0
        once = False

        if limit > MAX_LIMIT:
            kwargs["count"] = MAX_LIMIT

        while (count < limit and cursor) or not once:
            if not once:
                once = True
            response = await super().get_data_async(*args, **kwargs)
            responses.append(response)

            if on_page_response:
                on_page_response(self, response)

            meta = response.data.raw.get("meta", {})
            count += meta.get("count", 0)
            cursor = meta.get("next")
            kwargs = {
                "cursor": cursor,
                "__content_type__": kwargs.get("__content_type__"),
            }

        return self.create_response(responses, limit, kwargs)


news_headlines_data_provider = NewsHeadlinesDataProvider(
    response=ContentResponseFactory(data_class=NewsHeadlinesData),
    request=NewsHeadlinesRequestFactory(),
    parser=ErrorParser(),
)
