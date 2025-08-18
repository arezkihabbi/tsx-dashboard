from typing import Optional, Union, List

from ..._enums import (
    AdjustInterestToPaymentDate,
    BusinessDayConvention,
    BuySell,
    DateRollingConvention,
    DayCountBasis,
    Frequency,
    IndexResetType,
    InterestCalculationConvention,
    StubRule,
    PriceSide,
)
from ..._models import AmortizationItem, BarrierDefinitionElement, InputFlow
from ..._param_item import (
    enum_param_item,
    serializable_param_item,
    list_serializable_param_item,
    datetime_param_item,
    param_item,
)
from ..._serializable import Serializable
from ....._types import OptDateTime


class CapFloorInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: OptDateTime = None,
        end_date: OptDateTime = None,
        tenor: Optional[str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        index_name: Optional[str] = None,
        index_tenor: Optional[str] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        payment_roll_convention: Union[DateRollingConvention, str] = None,
        index_reset_frequency: Union[Frequency, str] = None,
        index_reset_type: Union[IndexResetType, str] = None,
        index_fixing_lag: Optional[int] = None,
        amortization_schedule: Optional[List[AmortizationItem]] = None,
        payment_business_days: Optional[str] = None,
        adjust_interest_to_payment_date: Union[AdjustInterestToPaymentDate, str] = None,
        stub_rule: Union[StubRule, str] = None,
        barrier_definition: Optional[BarrierDefinitionElement] = None,
        buy_sell: Union[BuySell, str] = None,
        interest_calculation_convention: Union[InterestCalculationConvention, str] = None,
        payments: Optional[InputFlow] = None,
        annualized_rebate: Optional[bool] = None,
        cap_digital_payout_percent: Optional[float] = None,
        cap_strike_percent: Optional[float] = None,
        cms_template: Optional[str] = None,
        floor_digital_payout_percent: Optional[float] = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        is_backward_looking_index: Optional[bool] = None,
        is_rfr: Optional[bool] = None,
        is_term_rate: Optional[bool] = None,
        index_price_side: Union[PriceSide, str] = None,
        cap_strike_percent_schedule: Optional[dict] = None,
        floor_strike_percent_schedule: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_reset_type = index_reset_type
        self.index_fixing_lag = index_fixing_lag
        self.amortization_schedule = amortization_schedule
        self.payment_business_days = payment_business_days
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.stub_rule = stub_rule
        self.barrier_definition = barrier_definition
        self.buy_sell = buy_sell
        self.interest_calculation_convention = interest_calculation_convention
        self.payments = payments
        self.annualized_rebate = annualized_rebate
        self.cap_digital_payout_percent = cap_digital_payout_percent
        self.cap_strike_percent = cap_strike_percent
        self.cms_template = cms_template
        self.floor_digital_payout_percent = floor_digital_payout_percent
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.is_backward_looking_index = is_backward_looking_index
        self.is_rfr = is_rfr
        self.is_term_rate = is_term_rate
        self.index_price_side = index_price_side
        self.cap_strike_percent_schedule = cap_strike_percent_schedule
        self.floor_strike_percent_schedule = floor_strike_percent_schedule

    @staticmethod
    def get_instrument_type():
        return "CapFloor"

    def _get_items(self):
        return [
            enum_param_item.to_kv("adjustInterestToPaymentDate", self.adjust_interest_to_payment_date),
            list_serializable_param_item.to_kv("amortizationSchedule", self.amortization_schedule),
            serializable_param_item.to_kv("barrierDefinition", self.barrier_definition),
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("indexResetFrequency", self.index_reset_frequency),
            enum_param_item.to_kv("indexResetType", self.index_reset_type),
            enum_param_item.to_kv("interestCalculationConvention", self.interest_calculation_convention),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            enum_param_item.to_kv("interestPaymentFrequency", self.interest_payment_frequency),
            enum_param_item.to_kv("paymentBusinessDayConvention", self.payment_business_day_convention),
            enum_param_item.to_kv("paymentRollConvention", self.payment_roll_convention),
            list_serializable_param_item.to_kv("payments", self.payments),
            enum_param_item.to_kv("stubRule", self.stub_rule),
            enum_param_item.to_kv("annualizedRebate", self.annualized_rebate),
            enum_param_item.to_kv("capDigitalPayoutPercent", self.cap_digital_payout_percent),
            enum_param_item.to_kv("capStrikePercent", self.cap_strike_percent),
            enum_param_item.to_kv("cmsTemplate", self.cms_template),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("floorDigitalPayoutPercent", self.floor_digital_payout_percent),
            param_item.to_kv("floorStrikePercent", self.floor_strike_percent),
            param_item.to_kv("indexFixingLag", self.index_fixing_lag),
            param_item.to_kv("indexFixingRic", self.index_fixing_ric),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("indexTenor", self.index_tenor),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("isBackwardLookingIndex", self.is_backward_looking_index),
            param_item.to_kv("isRfr", self.is_rfr),
            param_item.to_kv("isTermRate", self.is_term_rate),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("paymentBusinessDays", self.payment_business_days),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("tenor", self.tenor),
            enum_param_item.to_kv("indexPriceSide", self.index_price_side),
            param_item.to_kv("capStrikePercentSchedule", self.cap_strike_percent_schedule),
            param_item.to_kv("floorStrikePercentSchedule", self.floor_strike_percent_schedule),
        ]
