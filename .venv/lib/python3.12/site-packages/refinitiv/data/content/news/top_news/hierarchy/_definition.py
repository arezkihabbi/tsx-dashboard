from typing import TYPE_CHECKING

from ._data_provider import HierarchyData
from ....._content_type import ContentType
from ....._types import ExtendedParams
from .....delivery._data._data_provider_layer import DataProviderLayer
from .....delivery._data._response import Response

if TYPE_CHECKING:
    from typing import Optional, Union
    from ._top_news_id import TopNewsId


class Definition(DataProviderLayer[Response[HierarchyData]]):
    """
    This class describes parameters to retrieve data for top news hierarchy.

    Parameters
    ----------
    id: str or Enum, optional
        The id of the package[current, test, next]

    extended_params: dict, optional
        Other parameters can be provided if necessary


    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.top_news.hierarchy.Definition()
    >>> response = definition.get_data()
    >>> response.data.hierarchy['Commodities']
    """

    def __init__(
        self,
        id: "Optional[Union[TopNewsId, str]]" = None,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_TOP_NEWS_HIERARCHY,
            id=id,
            extended_params=extended_params,
        )
