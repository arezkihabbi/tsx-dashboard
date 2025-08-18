from typing import Optional, Union

from ..._enums import BusinessDayConvention, DateRollingConvention, DayCountBasis, Frequency
from ..._param_item import enum_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class TermDepositInstrumentDefinition(Serializable):
    def __init__(
        self,
        *,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        payment_roll_convention: Union[DateRollingConvention, str] = None,
        year_basis: Union[DayCountBasis, str] = None,
        calendar: Optional[str] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_days: Optional[str] = None,
        start_tenor: Optional[str] = None,
    ):
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.year_basis = year_basis
        self.calendar = calendar
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.payment_business_days = payment_business_days
        self.start_tenor = start_tenor

    @staticmethod
    def get_instrument_type():
        return "TermDeposit"

    def _get_items(self):
        return [
            enum_param_item.to_kv("paymentBusinessDayConvention", self.payment_business_day_convention),
            enum_param_item.to_kv("paymentRollConvention", self.payment_roll_convention),
            enum_param_item.to_kv("yearBasis", self.year_basis),
            param_item.to_kv("calendar", self.calendar),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("fixedRatePercent", self.fixed_rate_percent),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("tenor", self.tenor),
            enum_param_item.to_kv("interestPaymentFrequency", self.interest_payment_frequency),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            param_item.to_kv("paymentBusinessDays", self.payment_business_days),
            param_item.to_kv("startTenor", self.start_tenor),
        ]
