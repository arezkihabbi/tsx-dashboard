from ._data import NewsStoryData
from ._request_factory import StoryRequestFactory
from ._response import NewsStoryResponse
from ._response_factory import NewsStoryResponseFactory
from ....delivery._data._data_provider import DataProvider

news_story_data_provider = DataProvider(
    response=NewsStoryResponseFactory(
        response_class=NewsStoryResponse,
        data_class=NewsStoryData,
    ),
    request=StoryRequestFactory(),
)
