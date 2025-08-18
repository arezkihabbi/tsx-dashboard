from typing import TYPE_CHECKING

from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from ..._content_type import ContentType
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import ExtendedParams


class Definition(ContentUsageLoggerMixin[Response[Data]], DataProviderLayer[Response[Data]]):
    """
    This class describe parameters to retrieve data for search custom instrument

    Parameters
    ----------
    access : str
        The search based on relationship to the custom instrument, for now only "owner" is supported. Can be omitted, default value is "owner"
    extended_params : dict, optional
        If necessary other parameters

    Examples
    --------
    >>> from refinitiv.data.content.custom_instruments import search
    >>> definition_search = search.Definition("S)My.CustomInstrument")
    >>> response = definition_search.get_data()
    """

    _USAGE_CLS_NAME = "CustomInstruments.SearchDefinition"

    def __init__(
        self,
        access: str = "owner",
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.CUSTOM_INSTRUMENTS_SEARCH,
            access=access,
            extended_params=extended_params,
        )
