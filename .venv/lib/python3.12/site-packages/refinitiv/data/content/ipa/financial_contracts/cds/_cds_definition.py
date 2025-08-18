from typing import Optional, Union

from ._premium_leg_definition import PremiumLegDefinition
from ._protection_leg_definition import ProtectionLegDefinition
from ..._enums import BusinessDayConvention, CdsConvention
from ..._param_item import enum_param_item, serializable_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class CdsInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        cds_convention: Union[CdsConvention, str] = None,
        trade_date: OptDateTime = None,
        step_in_date: OptDateTime = None,
        start_date: OptDateTime = None,
        end_date: OptDateTime = None,
        tenor: Optional[str] = None,
        start_date_moving_convention: Union[BusinessDayConvention, str] = None,
        end_date_moving_convention: Union[BusinessDayConvention, str] = None,
        adjust_to_isda_end_date: Optional[bool] = None,
        protection_leg: Optional[ProtectionLegDefinition] = None,
        premium_leg: Optional[PremiumLegDefinition] = None,
        accrued_begin_date: OptDateTime = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.cds_convention = cds_convention
        self.trade_date = trade_date
        self.step_in_date = step_in_date
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.start_date_moving_convention = start_date_moving_convention
        self.end_date_moving_convention = end_date_moving_convention
        self.adjust_to_isda_end_date = adjust_to_isda_end_date
        self.protection_leg = protection_leg
        self.premium_leg = premium_leg
        self.accrued_begin_date = accrued_begin_date

    @staticmethod
    def get_instrument_type():
        return "Cds"

    def _get_items(self):
        return [
            enum_param_item.to_kv("cdsConvention", self.cds_convention),
            enum_param_item.to_kv("endDateMovingConvention", self.end_date_moving_convention),
            serializable_param_item.to_kv("premiumLeg", self.premium_leg),
            serializable_param_item.to_kv("protectionLeg", self.protection_leg),
            enum_param_item.to_kv("startDateMovingConvention", self.start_date_moving_convention),
            datetime_param_item.to_kv("accruedBeginDate", self.accrued_begin_date),
            param_item.to_kv("adjustToIsdaEndDate", self.adjust_to_isda_end_date),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("instrumentCode", self.instrument_code),
            datetime_param_item.to_kv("startDate", self.start_date),
            datetime_param_item.to_kv("stepInDate", self.step_in_date),
            param_item.to_kv("tenor", self.tenor),
            datetime_param_item.to_kv("tradeDate", self.trade_date),
            enum_param_item.to_kv("instrumentTag", self.instrument_tag),
        ]
