from typing import TYPE_CHECKING

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
    This class describe parameters to retrieve the calculated concentration data
    by top 10, 20, 50, 100 fund investors.

    Parameters
    ----------
    universe: str, list of str
        The Universe parameter allows the user to define the companies for which the content is returned.

    count: int
        Number of records

    use_field_names_in_headers: bool, optional
        Return field name as column headers for data instead of title

    extended_params : ExtendedParams, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content import ownership
    >>> definition = ownership.fund.top_n_concentration.Definition("TRI.N", 30)
    >>> response = definition.get_data()
    """

    _USAGE_CLS_NAME = "Ownership.Fund.TopNConcentrationDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        count: int,
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(count, [int], "count")
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.OWNERSHIP_FUND_TOP_N_CONCENTRATION,
            universe=universe,
            count=count,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
