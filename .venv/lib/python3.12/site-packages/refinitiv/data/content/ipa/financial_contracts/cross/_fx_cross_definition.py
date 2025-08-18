from typing import Optional, Union

from ._fx_cross_leg_definition import LegDefinition
from ..._enums import FxCrossType
from ..._param_item import enum_param_item, list_serializable_param_item, param_item
from ..._serializable import Serializable


class FxCrossInstrumentDefinition(Serializable):
    def __init__(
        self,
        *,
        instrument_tag: Optional[str] = None,
        legs: Optional[LegDefinition] = None,
        fx_cross_type: Union[FxCrossType, str] = None,
        fx_cross_code: Optional[str] = None,
        ndf_fixing_settlement_ccy: Optional[str] = None,
        reference_spot_rate: Optional[float] = None,
        traded_cross_rate: Optional[float] = None,
        traded_swap_points: Optional[float] = None,
        settlement_ccy: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.legs = legs
        self.fx_cross_type = fx_cross_type
        self.fx_cross_code = fx_cross_code
        self.ndf_fixing_settlement_ccy = ndf_fixing_settlement_ccy
        self.reference_spot_rate = reference_spot_rate
        self.traded_cross_rate = traded_cross_rate
        self.traded_swap_points = traded_swap_points
        self.settlement_ccy = settlement_ccy

    @staticmethod
    def get_instrument_type():
        return "FxCross"

    def _get_items(self):
        return [
            enum_param_item.to_kv("fxCrossType", self.fx_cross_type),
            list_serializable_param_item.to_kv("legs", self.legs),
            param_item.to_kv("fxCrossCode", self.fx_cross_code),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("ndfFixingSettlementCcy", self.ndf_fixing_settlement_ccy),
            param_item.to_kv("referenceSpotRate", self.reference_spot_rate),
            param_item.to_kv("tradedCrossRate", self.traded_cross_rate),
            param_item.to_kv("tradedSwapPoints", self.traded_swap_points),
            param_item.to_kv("settlementCcy", self.settlement_ccy),
        ]
