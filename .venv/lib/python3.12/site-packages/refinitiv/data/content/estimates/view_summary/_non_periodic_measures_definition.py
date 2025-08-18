from typing import Union, TYPE_CHECKING

from .._enums import Package
from ..._content_data import Data
from ..._content_provider_layer import ContentUsageLoggerMixin
from ...._content_type import ContentType
from ...._tools import validate_types, validate_bool_value, try_copy_to_list
from ....delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ...._types import StrStrings, ExtendedParams


class Definition(
    ContentUsageLoggerMixin[Response[Data]],
    DataProviderLayer[Response[Data]],
):
    """
    Describes the parameters used to retrieve the estimates summary for all non-periodic estimates measures.

    Parameters
    ----------
    universe: str, list of str
        Single instrument or list of instruments.
    package: str, Package
        Packages of the content that are subsets in terms of breadth (number of fields) and depth (amount of history)
        of the overall content set.
    use_field_names_in_headers: bool, optional
        Boolean that indicates whether or not to display field names in the headers.
    extended_params: ExtendedParams, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.content import estimates
    >>> definition = estimates.view_summary.non_periodic_measures.Definition(universe="IBM.N", package=estimates.Package.BASIC)
    >>> response = definition.get_data()
    """

    _USAGE_CLS_NAME = "Estimates.Summary.NonPeriodicMeasuresDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        package: Union[str, Package],
        use_field_names_in_headers: bool = False,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(package, [str, Package], "package")
        validate_bool_value(use_field_names_in_headers)
        universe = try_copy_to_list(universe)

        super().__init__(
            ContentType.ESTIMATES_VIEW_SUMMARY_NON_PERIODIC_MEASURES,
            universe=universe,
            package=package,
            use_field_names_in_headers=use_field_names_in_headers,
            extended_params=extended_params,
        )
