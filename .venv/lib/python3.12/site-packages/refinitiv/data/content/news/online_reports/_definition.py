from typing import TYPE_CHECKING

from ._data_provider import NewsOnlineReportsData
from ...._content_type import ContentType
from ....delivery._data._data_provider_layer import DataProviderLayer
from ....delivery._data._response import Response

if TYPE_CHECKING:
    from ...._types import OptStr, ExtendedParams


class Definition(DataProviderLayer[Response[NewsOnlineReportsData]]):
    """
    This class describes parameters to retrieve data for news online-reports.

    Parameters
    ----------
    report_id: str, optional
        The report code

    full_content: boolean, optional
        The value indicating whether TOP 10 full documents must be retrieved

    extended_params: dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import news
    >>> definition = news.online_reports.Definition("OLUSTOPNEWS")
    >>> response = definition.get_data()
    """

    def __init__(
        self,
        report_id: "OptStr" = None,
        full_content: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_ONLINE_REPORTS,
            report_id=report_id,
            full_content=full_content,
            extended_params=extended_params,
        )
