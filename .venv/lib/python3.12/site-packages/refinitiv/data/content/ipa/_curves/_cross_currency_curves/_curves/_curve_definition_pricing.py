from typing import Optional, TYPE_CHECKING

from ._enums import ConstituentOverrideMode
from .._enums import MainConstituentAssetClass, RiskType
from ...._param_item import enum_param_item, param_item
from ...._serializable import Serializable

if TYPE_CHECKING:
    from ......_types import OptStr, OptBool


class CrossCurrencyCurveDefinitionPricing(Serializable):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    constituent_override_mode : ConstituentOverrideMode, optional
        A method to use the default constituents. the possible values are:   *
        replacedefinition: replace the default constituents by the user constituents
        from the input request,   * mergewithdefinition: merge the default constituents
        and the user constituents from the input request, the default value is
        'replacedefinition'.  if the ignoreexistingdefinition is true, the
        constituentoverridemode is set to replacedefinition.
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
    id : str, optional
        The identifier of the cross currency definitions.
    ignore_existing_definition : bool, optional
        An indicator whether default definitions are used to get curve parameters and
        constituents. the possible values are:   * true: default definitions are not
        used (definitions and constituents must be set in the request),   * false:
        default definitions are used.
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
        constituent_override_mode: Optional[ConstituentOverrideMode] = None,
        main_constituent_asset_class: Optional[MainConstituentAssetClass] = None,
        risk_type: Optional[RiskType] = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        id: "OptStr" = None,
        ignore_existing_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.constituent_override_mode = constituent_override_mode
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.id = id
        self.ignore_existing_definition = ignore_existing_definition
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source

    def _get_items(self):
        return [
            enum_param_item.to_kv("constituentOverrideMode", self.constituent_override_mode),
            enum_param_item.to_kv("mainConstituentAssetClass", self.main_constituent_asset_class),
            enum_param_item.to_kv("riskType", self.risk_type),
            param_item.to_kv("baseCurrency", self.base_currency),
            param_item.to_kv("baseIndexName", self.base_index_name),
            param_item.to_kv("id", self.id),
            param_item.to_kv("ignoreExistingDefinition", self.ignore_existing_definition),
            param_item.to_kv("isNonDeliverable", self.is_non_deliverable),
            param_item.to_kv("name", self.name),
            param_item.to_kv("quotedCurrency", self.quoted_currency),
            param_item.to_kv("quotedIndexName", self.quoted_index_name),
            param_item.to_kv("source", self.source),
        ]
