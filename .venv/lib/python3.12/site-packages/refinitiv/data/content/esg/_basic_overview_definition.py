from typing import TYPE_CHECKING

from .._content_data import Data
from .._content_provider_layer import ContentUsageLoggerMixin
from ..._content_type import ContentType
from ..._tools import create_repr, validate_bool_value, try_copy_to_list
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import StrStrings


class Definition(
    ContentUsageLoggerMixin[Response[Data]],
    DataProviderLayer[Response[Data]],
):
    """
    Defines the basic ESG data to retrieve.

    Parameters
    ----------
    universe : str, list of str
        Single instrument or list of instruments.
    use_field_names_in_headers: bool, optional
        Boolean that indicates whether or not to display field names in the headers.

    Examples
    --------
    >>> import asyncio
    >>> from refinitiv.data.content import esg
    >>> definition = esg.basic_overview.Definition("IBM.N")
    >>> response = definition.get_data()

    >>> response = asyncio.run(definition.get_data_async())
    """

    _USAGE_CLS_NAME = "ESG.BasicOverviewDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        use_field_names_in_headers: bool = False,
    ):
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.ESG_BASIC_OVERVIEW,
            universe=universe,
            use_field_names_in_headers=use_field_names_in_headers,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="basic_overview",
            content=f"{{universe='{self._kwargs.get('universe')}'}}",
        )
