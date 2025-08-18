from typing import Union, TYPE_CHECKING

from .._enums import StatTypes
from ..._content_data import Data
from ..._content_provider_layer import ContentUsageLoggerMixin
from ...._content_type import ContentType
from ...._tools import validate_types, validate_bool_value, try_copy_to_list
from ....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ...._types import ExtendedParams, StrStrings


class Definition(
    ContentUsageLoggerMixin[Response[Data]],
    DataProviderLayer[Response[Data]],
):
    """
    This class describe parameters to retrieve holdings data breakdown by Investors Types,
    Styles, Region, Countries, Rotations and Turnovers.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    stat_type: int, StatTypes
        The statType parameter specifies which statistics type to be returned.
        The types available are:
            - Investor Type (1)
            - Investment Style (2)
            - Region (3)
            - Rotation (4)
            - Country (5)
            - Metro Area (6)
            - Investor Type Parent (7)
            - Invest Style Parent (8)

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.fund.breakdown.Definition("TRI.N", ownership.StatTypes.INVESTOR_TYPE)
    >>> response = definition.get_data()
    """

    _USAGE_CLS_NAME = "Ownership.Fund.BreakdownDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        stat_type: Union[int, StatTypes],
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(stat_type, [int, StatTypes], "stat_type")
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.OWNERSHIP_FUND_BREAKDOWN,
            universe=universe,
            stat_type=stat_type,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
