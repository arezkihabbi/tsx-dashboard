from typing import Optional

from .._enums import ConstituentOverrideMode
from ..._enums import AssetClass, RiskType
from ..._param_item import enum_param_item, param_item
from ..._serializable import Serializable
from ....._tools import create_repr, try_copy_to_list
from ....._types import Strings, OptStr, OptStrings, OptBool


class SwapZcCurveDefinition(Serializable):
    """
    Parameters
    ----------
    index_name : str, optional

    main_constituent_asset_class : MainConstituentAssetClass, optional

    risk_type : RiskType, optional

    currency : str, optional

    discounting_tenor : str, optional

    id : str, optional
        Id of the curve definition to get

    market_data_location : str, optional

    name : str, optional

    source : str, optional

    available_discounting_tenors : string, optional
        The list of discounting tenors available when using a given interest rate curve.
        the values come from availabletenors list (e.g., '[ois, 1m, 3m, 6m, 1y]').

    available_tenors : string, optional
        The list of tenors which can be priced with curvedefinitions (e.g., '[ois, 1m,
        3m, 6m, 1y]'

    constituent_override_mode : ConstituentOverrideMode, optional
        The possible values are:
        * replacedefinition: replace the default constituents by the user constituents
            from the input request,
        * mergewithdefinition: merge the default constituents and the user constituents
            from the input request, the default value is 'replacedefinition'.
        If the ignoreexistingdefinition is true, the constituentoverridemode is set
        to replacedefinition.

    ignore_existing_definition : bool, optional
        An indicator whether default definitions are used to get curve parameters and
        constituents.
        The possible values are:
        * True: default definitions are not used (definitions and constituents must
            be set in the request),
        * False: default definitions are used.

    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable:
        * True: the instrument is non-deliverable,
        * False: the instrument is not non-deliverable.
        This parameter may be used to specify the use of crosscurrencydefinitions made
        of non-deliverable or deliverable instruments. When this parameters isn't
        specified, the default crosscurrencydefinitions is used. This definition with
        'isfallbackforfxcurvedefinition'=True is returned by the
        crosscurrencydefinitions curve search.

    owner : str, optional
        Uuid of the curve definition owner for none refinitiv curve
    """

    def __init__(
        self,
        index_name: OptStr = None,
        index_tenors: Strings = None,
        main_constituent_asset_class: Optional[AssetClass] = None,
        risk_type: Optional[RiskType] = None,
        currency: OptStr = None,
        discounting_tenor: OptStr = None,
        id: OptStr = None,
        market_data_location: OptStr = None,
        name: OptStr = None,
        source: OptStr = None,
        available_discounting_tenors: OptStrings = None,
        available_tenors: OptStrings = None,
        constituent_override_mode: Optional[ConstituentOverrideMode] = None,
        ignore_existing_definition: OptBool = None,
        is_non_deliverable: OptBool = None,
        owner: OptStr = None,
    ) -> None:
        super().__init__()
        self.index_name = index_name
        self.index_tenors = index_tenors
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.currency = currency
        self.discounting_tenor = discounting_tenor
        self.id = id
        self.market_data_location = market_data_location
        self.name = name
        self.source = source
        self.available_discounting_tenors = try_copy_to_list(available_discounting_tenors)
        self.available_tenors = try_copy_to_list(available_tenors)
        self.constituent_override_mode = constituent_override_mode
        self.ignore_existing_definition = ignore_existing_definition
        self.is_non_deliverable = is_non_deliverable
        self.owner = owner

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)

    def _get_items(self):
        return [
            enum_param_item.to_kv("mainConstituentAssetClass", self.main_constituent_asset_class),
            enum_param_item.to_kv("riskType", self.risk_type),
            param_item.to_kv("currency", self.currency),
            param_item.to_kv("discountingTenor", self.discounting_tenor),
            param_item.to_kv("id", self.id),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("marketDataLocation", self.market_data_location),
            param_item.to_kv("name", self.name),
            param_item.to_kv("source", self.source),
            param_item.to_kv("availableDiscountingTenors", self.available_discounting_tenors),
            param_item.to_kv("availableTenors", self.available_tenors),
            enum_param_item.to_kv("constituentOverrideMode", self.constituent_override_mode),
            param_item.to_kv("ignoreExistingDefinition", self.ignore_existing_definition),
            param_item.to_kv("isNonDeliverable", self.is_non_deliverable),
            param_item.to_kv("owner", self.owner),
        ]
