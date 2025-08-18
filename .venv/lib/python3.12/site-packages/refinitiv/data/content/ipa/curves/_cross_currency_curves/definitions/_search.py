from typing import TYPE_CHECKING

from ...._curves._cross_currency_curves._definitions._search import CrossCurrencyCurveGetDefinitionItem
from ......_content_type import ContentType
from ......_tools import create_repr
from ....._content_provider_layer import ContentProviderLayer, PosArgsWarnMixin


if TYPE_CHECKING:
    from ...._curves._cross_currency_curves._types import (
        OptMainConstituentAssetClass,
        OptRiskType,
    )
    from ......_types import OptStr, OptBool, ExtendedParams


class Definition(ContentProviderLayer, PosArgsWarnMixin):
    """
    Returns the definitions of the available Commodities curves for the filters
    selected (e.g. sector, subSector...).

    Parameters
    ----------
    main_constituent_asset_class : MainConstituentAssetClass, optional
        The asset class used to generate the zero coupon curve. the possible values are:
        * fxforward   * swap
    risk_type : RiskType, optional
        The risk type to which the generated cross currency curve is sensitive. the
        possible value is:   * 'crosscurrency'
    base_currency : str, optional
        The base currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'eur').
    base_index_name : str, optional
        The name of the floating rate index (e.g., 'estr') applied to the base currency.
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    id : str, optional
        The identifier of the cross currency definitions.
    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable:   * true: the instrument
        is non-deliverable,   * false: the instrument is not non-deliverable. the
        property can be used to retrieve cross currency definition for the adjusted
        interest rate curve.
    name : str, optional
        The fxcross currency pair applied to the reference or pivot currency. it is
        expressed in iso 4217 alphabetical format (e.g., 'eur usd fxcross').
    quoted_currency : str, optional
        The quoted currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'usd').
    quoted_index_name : str, optional
        The name of the floating rate index (e.g., 'sofr') applied to the quoted
        currency.
    source : str, optional
        A user-defined string that is provided by the creator of a curve. curves created
        by refinitiv have the 'refinitiv' source.
    valuation_date : str or date or datetime or timedelta, optional
        The date used to define a list of curves or a unique cross currency curve that
        can be priced at this date. the value is expressed in iso 8601 format:
        yyyy-mm-dd (e.g., '2021-01-01').
    extended_params : dict, optional
        If necessary other parameters.

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
    >>> definition = definitions.search.Definition(
    ...     base_currency="EUR",
    ...     quoted_currency="CHF"
    >>> )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        main_constituent_asset_class: "OptMainConstituentAssetClass" = None,
        risk_type: "OptRiskType" = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        curve_tag: "OptStr" = None,
        id: "OptStr" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
        valuation_date: "OptDateTime" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        request_item = CrossCurrencyCurveGetDefinitionItem(
            main_constituent_asset_class=main_constituent_asset_class,
            risk_type=risk_type,
            base_currency=base_currency,
            base_index_name=base_index_name,
            curve_tag=curve_tag,
            id=id,
            is_non_deliverable=is_non_deliverable,
            name=name,
            quoted_currency=quoted_currency,
            quoted_index_name=quoted_index_name,
            source=source,
            valuation_date=valuation_date,
        )
        super().__init__(
            content_type=ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_SEARCH,
            universe=request_item,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self, middle_path="_cross_currency_curves.definitions.search")
