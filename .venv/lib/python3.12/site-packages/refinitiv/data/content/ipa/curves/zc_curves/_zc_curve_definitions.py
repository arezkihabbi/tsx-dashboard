from typing import Optional, Iterable, TYPE_CHECKING

from .._enums import ConstituentOverrideMode
from ..zc_curve_definitions._zc_curve_definition import ZcCurveDefinition
from ..._curves._cross_currency_curves import CrossCurrencyCurveDefinitionPricing
from ..._enums import AssetClass, RiskType
from ..._param_item import enum_param_item, param_item, serializable_param_item, list_serializable_param_item
from ..._serializable import Serializable
from ....._tools import create_repr, try_copy_to_list

if TYPE_CHECKING:
    from ....._types import OptStr, OptStrings, OptBool


class ZcCurveDefinitions(Serializable):
    """
    Parameters
    ----------
    index_name : str, optional

    index_tenors : string, optional
        Defines expected rate surface tenor/slices Defaults to the tenors available,
        based on provided market data
    main_constituent_asset_class : AssetClass, optional

    pivot_curve_definition : ZcCurveDefinition, optional

    reference_curve_definition : ZcCurveDefinition, optional

    risk_type : RiskType, optional

    currency : str, optional
        The currency code of the interest rate curve
    discounting_tenor : str, optional
        Mono currency discounting tenor
    id : str, optional
        Id of the curve definition
    name : str, optional
        The name of the interest rate curve
    source : str, optional
    constituent_override_mode : ConstituentOverrideMode, optional
        The possible values are:
          * replacedefinition: replace the default constituents by the user
              constituents from the input request,
          * mergewithdefinition: merge the default constituents and the user
              constituents from the input request, the default value is 'replacedefinition'.
        If the ignore_existing_definition is true, the constituent_override_mode
        is set to 'replacedefinition'.
    cross_currency_definitions : CrossCurrencyCurveDefinitionPricing, optional
        The list of the cross currency definition attributes used for pricing the
        adjusted interest rate curve. if not set in the request the definition matching
        the currencies, index names and the isnondeliverable flag are retrieved.
    curve_tenors : string, optional
        The list of user-defined tenors or dates for which curvepoints to be computed.
        The values are expressed in:
            * time period code for tenors (e.g., '1m', '6m', '4y'),
            * iso 8601 format 'yyyy-mm-dd' for dates (e.g., '2021-01-01').
    ignore_existing_definition : bool, optional
        An indicator whether default definitions are used to get curve parameters and
        constituents.
        The possible values are:
        * True: default definitions are not used (definitions and constituents must
            be set in the request),
        * False: default definitions are used.
    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable.
        The possible values are:
            * True: the instrument is non-deliverable,
            * False: the instrument is not non-deliverable.
        This parameter may be used to specify the use of crosscurrencydefinitions made
        of non-deliverable or deliverable instruments. When this parameters isn't
        specified, the default crosscurrencydefinitions is used. this definition with
        'isfallbackforfxcurvedefinition'=True is returned by the
        crosscurrencydefinitions curve search.
    """

    def __init__(
        self,
        index_name: "OptStr" = None,
        index_tenors: "OptStrings" = None,
        main_constituent_asset_class: Optional[AssetClass] = None,
        pivot_curve_definition: Optional[ZcCurveDefinition] = None,
        reference_curve_definition: Optional[ZcCurveDefinition] = None,
        risk_type: Optional[RiskType] = None,
        currency: "OptStr" = None,
        discounting_tenor: "OptStr" = None,
        id: "OptStr" = None,
        name: "OptStr" = None,
        source: "OptStr" = None,
        constituent_override_mode: Optional[ConstituentOverrideMode] = None,
        cross_currency_definitions: Optional[Iterable[CrossCurrencyCurveDefinitionPricing]] = None,
        curve_tenors: "OptStrings" = None,
        ignore_existing_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        market_data_location: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.index_name = index_name
        self.index_tenors = try_copy_to_list(index_tenors)
        self.main_constituent_asset_class = main_constituent_asset_class
        self.pivot_curve_definition = pivot_curve_definition
        self.reference_curve_definition = reference_curve_definition
        self.risk_type = risk_type
        self.currency = currency
        self.discounting_tenor = discounting_tenor
        self.id = id
        self.name = name
        self.source = source
        self.constituent_override_mode = constituent_override_mode
        self.cross_currency_definitions = try_copy_to_list(cross_currency_definitions)
        self.curve_tenors = try_copy_to_list(curve_tenors)
        self.ignore_existing_definition = ignore_existing_definition
        self.is_non_deliverable = is_non_deliverable
        self.market_data_location = market_data_location

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)

    def _get_items(self):
        return [
            param_item.to_kv("indexTenors", self.index_tenors),
            enum_param_item.to_kv("mainConstituentAssetClass", self.main_constituent_asset_class),
            serializable_param_item.to_kv("pivotCurveDefinition", self.pivot_curve_definition),
            serializable_param_item.to_kv("referenceCurveDefinition", self.reference_curve_definition),
            enum_param_item.to_kv("riskType", self.risk_type),
            param_item.to_kv("currency", self.currency),
            param_item.to_kv("discountingTenor", self.discounting_tenor),
            param_item.to_kv("id", self.id),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("name", self.name),
            param_item.to_kv("source", self.source),
            enum_param_item.to_kv("constituentOverrideMode", self.constituent_override_mode),
            list_serializable_param_item.to_kv("crossCurrencyDefinitions", self.cross_currency_definitions),
            param_item.to_kv("curveTenors", self.curve_tenors),
            param_item.to_kv("ignoreExistingDefinition", self.ignore_existing_definition),
            param_item.to_kv("isNonDeliverable", self.is_non_deliverable),
            param_item.to_kv("marketDataLocation", self.market_data_location),
        ]
