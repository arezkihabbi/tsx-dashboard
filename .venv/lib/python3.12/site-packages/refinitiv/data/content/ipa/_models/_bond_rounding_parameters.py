from .._enums import Rounding, RoundingType
from .._param_item import enum_param_item
from .._serializable import Serializable


class BondRoundingParameters(Serializable):
    def __init__(
        self,
        accrued_rounding: Rounding = None,
        accrued_rounding_type: RoundingType = None,
        price_rounding: Rounding = None,
        price_rounding_type: RoundingType = None,
        spread_rounding: Rounding = None,
        spread_rounding_type: RoundingType = None,
        yield_rounding: Rounding = None,
        yield_rounding_type: RoundingType = None,
    ):
        super().__init__()
        self.accrued_rounding = accrued_rounding
        self.accrued_rounding_type = accrued_rounding_type
        self.price_rounding = price_rounding
        self.price_rounding_type = price_rounding_type
        self.spread_rounding = spread_rounding
        self.spread_rounding_type = spread_rounding_type
        self.yield_rounding = yield_rounding
        self.yield_rounding_type = yield_rounding_type

    def _get_items(self):
        return [
            enum_param_item.to_kv("accruedRounding", self.accrued_rounding),
            enum_param_item.to_kv("accruedRoundingType", self.accrued_rounding_type),
            enum_param_item.to_kv("priceRounding", self.price_rounding),
            enum_param_item.to_kv("priceRoundingType", self.price_rounding_type),
            enum_param_item.to_kv("spreadRounding", self.spread_rounding),
            enum_param_item.to_kv("spreadRoundingType", self.spread_rounding_type),
            enum_param_item.to_kv("yieldRounding", self.yield_rounding),
            enum_param_item.to_kv("yieldRoundingType", self.yield_rounding_type),
        ]
