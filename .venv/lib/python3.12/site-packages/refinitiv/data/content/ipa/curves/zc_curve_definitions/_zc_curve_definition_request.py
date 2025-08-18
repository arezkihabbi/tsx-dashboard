from typing import TYPE_CHECKING, Optional

from ..._enums import AssetClass, RiskType
from ..._param_item import enum_param_item, param_item, date_param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr


class ZcCurveDefinitionRequest(Serializable):
    def __init__(
        self,
        index_name: "OptStr" = None,
        main_constituent_asset_class: Optional[AssetClass] = None,
        risk_type: Optional[RiskType] = None,
        currency: "OptStr" = None,
        curve_tag: "OptStr" = None,
        id: "OptStr" = None,
        name: "OptStr" = None,
        source: "OptStr" = None,
        valuation_date: "OptStr" = None,
        market_data_location: "OptStr" = None,
    ):
        super().__init__()
        self.index_name = index_name
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.currency = currency
        self.curve_tag = curve_tag
        self.id = id
        self.name = name
        self.source = source
        self.valuation_date = valuation_date
        self.market_data_location = market_data_location

    def _get_items(self):
        return [
            enum_param_item.to_kv("mainConstituentAssetClass", self.main_constituent_asset_class),
            enum_param_item.to_kv("riskType", self.risk_type),
            param_item.to_kv("currency", self.currency),
            param_item.to_kv("curveTag", self.curve_tag),
            param_item.to_kv("id", self.id),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("name", self.name),
            param_item.to_kv("source", self.source),
            date_param_item.to_kv("valuationDate", self.valuation_date),
            param_item.to_kv("marketDataLocation", self.market_data_location),
        ]
