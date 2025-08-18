from typing import TYPE_CHECKING

from ._data_provider import TopNewsData
from ...._content_type import ContentType
from ....delivery._data._data_provider_layer import DataProviderLayer
from ....delivery._data._response import Response

if TYPE_CHECKING:
    from ...._types import OptInt, ExtendedParams


class Definition(DataProviderLayer[Response[TopNewsData]]):
    """
    This class describes parameters to retrieve data for top news headlines.

    Parameters
    ----------
    top_news_id: str
        The id of the package

    revision_id: int, optional
        The package known version

    extended_params: dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.top_news.Definition("top_news_id")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        top_news_id: str,
        revision_id: "OptInt" = None,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_TOP_NEWS,
            top_news_id=top_news_id,
            revision_id=revision_id,
            extended_params=extended_params,
        )
