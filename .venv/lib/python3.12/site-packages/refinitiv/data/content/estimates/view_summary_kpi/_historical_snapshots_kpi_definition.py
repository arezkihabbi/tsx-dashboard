from typing import TYPE_CHECKING

from ..._content_data import Data
from ..._content_provider_layer import ContentUsageLoggerMixin
from ...._content_type import ContentType
from ...._tools import validate_bool_value, try_copy_to_list
from ....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ...._types import StrStrings, ExtendedParams


class Definition(
    ContentUsageLoggerMixin[Response[Data]],
    DataProviderLayer[Response[Data]],
):
    """
    Describes the parameters used to retrieve the estimated monthly historical snapshot value for all KPI measures for the last 12 months.

    Parameters
    ----------
    universe: str, list of str
        Single instrument or list of instruments.
    use_field_names_in_headers: bool, optional
        Boolean that indicates whether or not to display field names in the headers.
    extended_params: ExtendedParams, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.content import estimates
    >>> definition = estimates.view_summary_kpi.historical_snapshots_kpi.Definition(universe="BNPP.PA")
    >>> response = definition.get_data()
    """

    _USAGE_CLS_NAME = "Estimates.SummaryKPI.HistoricalSnapshotsKPIDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.ESTIMATES_VIEW_SUMMARY_KPI_HISTORICAL_SNAPSHOTS_KPI,
            universe=universe,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
