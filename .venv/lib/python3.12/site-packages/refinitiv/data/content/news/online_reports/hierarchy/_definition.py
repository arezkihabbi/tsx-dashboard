from ._data_provider import HierarchyData
from ....._content_type import ContentType
from ....._types import ExtendedParams
from .....delivery._data._data_provider_layer import DataProviderLayer
from .....delivery._data._response import Response


class Definition(DataProviderLayer[Response[HierarchyData]]):
    """
    This class describes parameters to retrieve data for news online-reports.

    Parameters
    ----------
    extended_params: dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.online_reports.hierarchy.Definition()
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_ONLINE_REPORTS_HIERARCHY,
            extended_params=extended_params,
        )
