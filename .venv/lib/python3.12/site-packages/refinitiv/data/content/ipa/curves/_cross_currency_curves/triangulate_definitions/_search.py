from typing import TYPE_CHECKING

from ...._curves._cross_currency_curves._triangulate_definitions import RequestItem
from ......_content_type import ContentType
from ......_tools import create_repr
from ....._content_provider_layer import ContentProviderLayer, PosArgsWarnMixin


if TYPE_CHECKING:
    from ......_types import OptStr, ExtendedParams


class Definition(ContentProviderLayer, PosArgsWarnMixin):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    base_currency : str, optional
        The base currency pair. It is expressed in ISO 4217 alphabetical format
        (e.g., 'EUR').
    base_index_name : str, optional
        The name of the floating rate index (e.g., 'ESTR') applied to the base currency.
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    quoted_currency : str, optional
        The quoted currency pair. It is expressed in ISO 4217 alphabetical
        format (e.g., 'USD').
    quoted_index_name : str, optional
        The name of the floating rate index (e.g., 'SOFR') applied to the
        quoted currency.
    valuation_date : str, optional
        The valuation date.
    extended_params : dict, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import triangulate_definitions
    ... definition = triangulate_definitions.search.Definition(
    ...     base_currency="EUR",
    ...     quoted_currency="CHF"
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        curve_tag: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        valuation_date: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        request_item = RequestItem(
            base_currency=base_currency,
            base_index_name=base_index_name,
            curve_tag=curve_tag,
            quoted_currency=quoted_currency,
            quoted_index_name=quoted_index_name,
            valuation_date=valuation_date,
        )
        super().__init__(
            content_type=ContentType.CROSS_CURRENCY_CURVES_TRIANGULATE_DEFINITIONS_SEARCH,
            universe=request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self, middle_path="_cross_currency_curves.triangulate_definitions.search")
