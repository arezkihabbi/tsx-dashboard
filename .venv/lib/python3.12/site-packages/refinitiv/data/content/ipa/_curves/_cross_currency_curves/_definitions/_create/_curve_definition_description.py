from typing import TYPE_CHECKING

from .._base_definition_mixin import BaseDefinitionMixin


if TYPE_CHECKING:
    from ..._types import OptMainConstituentAssetClass, OptRiskType
    from ......._types import OptStr, OptBool, OptDateTime


class CrossCurrencyCurveCreateDefinition(BaseDefinitionMixin):
    """
    Create a cross currency curve definition

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
    definition_expiry_date : str or date or datetime or timedelta, optional
        The date after which curvedefinitions can not be used. the value is expressed in
        iso 8601 format: yyyy-mm-dd (e.g., '2021-01-01').
    is_fallback_for_fx_curve_definition : bool, optional
        The indicator used to define the fallback logic for the fx curve definition. the
        possible values are:   * true: there's a fallback logic to use cross currency
        curve definition for fx curve definition,   * false: there's no fallback logic
        to use cross currency curve definition for fx curve definition.
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
    """

    def __init__(
        self,
        main_constituent_asset_class: "OptMainConstituentAssetClass" = None,
        risk_type: "OptRiskType" = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        definition_expiry_date: "OptDateTime" = None,
        is_fallback_for_fx_curve_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.definition_expiry_date = definition_expiry_date
        self.is_fallback_for_fx_curve_definition = is_fallback_for_fx_curve_definition
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source
