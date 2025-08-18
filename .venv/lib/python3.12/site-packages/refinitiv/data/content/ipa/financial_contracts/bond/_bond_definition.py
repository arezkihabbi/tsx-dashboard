from typing import Optional, Union, List

from ..._enums import (
    DateRollingConvention,
    DayCountBasis,
    InterestType,
    StubRule,
    Frequency,
    AdjustInterestToPaymentDate,
    IndexCompoundingMethod,
    BusinessDayConvention,
    Direction,
    IndexAverageMethod,
)
from ..._enums import IndexObservationMethod
from ..._models import AmortizationItem
from ..._param_item import (
    enum_param_item,
    datetime_param_item,
    param_item,
    list_serializable_param_item,
)
from ..._serializable import Serializable
from ....._types import OptDateTime


class BondInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        end_date: OptDateTime = None,
        direction: Union[Direction, str] = None,
        interest_type: Union[InterestType, str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        spread_bp: Optional[float] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        accrued_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        payment_roll_convention: Union[DateRollingConvention, str] = None,
        index_reset_frequency: Union[Frequency, str] = None,
        index_fixing_lag: Optional[int] = None,
        first_regular_payment_date: OptDateTime = None,
        last_regular_payment_date: OptDateTime = None,
        amortization_schedule: List[AmortizationItem] = None,
        payment_business_days: Optional[str] = None,
        adjust_interest_to_payment_date: Union[AdjustInterestToPaymentDate, str] = None,
        index_compounding_method: Union[IndexCompoundingMethod, str] = None,
        interest_payment_delay: Optional[int] = None,
        stub_rule: Union[StubRule, str] = None,
        issue_date: OptDateTime = None,
        index_average_method: Union[IndexAverageMethod, str] = None,
        first_accrual_date: OptDateTime = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        is_perpetual: Optional[bool] = None,
        template: Optional[str] = None,
        index_observation_method: Union[IndexObservationMethod, str] = None,
        fixed_rate_percent_schedule: Optional[dict] = None,
        instrument_type: str = "Bond",
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.instrument_code = instrument_code
        self.end_date = end_date
        self.direction = direction
        self.interest_type = interest_type
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.spread_bp = spread_bp
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.accrued_calculation_method = accrued_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_fixing_lag = index_fixing_lag
        self.first_regular_payment_date = first_regular_payment_date
        self.last_regular_payment_date = last_regular_payment_date
        self.amortization_schedule = amortization_schedule
        self.payment_business_days = payment_business_days
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.index_compounding_method = index_compounding_method
        self.interest_payment_delay = interest_payment_delay
        self.stub_rule = stub_rule
        self.issue_date = issue_date
        self.index_average_method = index_average_method
        self.first_accrual_date = first_accrual_date
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.is_perpetual = is_perpetual
        self.template = template
        self.index_observation_method = index_observation_method
        self.fixed_rate_percent_schedule = fixed_rate_percent_schedule
        self.instrument_type = instrument_type

    def get_instrument_type(self):
        return self.instrument_type

    def _get_items(self):
        return [
            enum_param_item.to_kv("accruedCalculationMethod", self.accrued_calculation_method),
            enum_param_item.to_kv("adjustInterestToPaymentDate", self.adjust_interest_to_payment_date),
            list_serializable_param_item.to_kv("amortizationSchedule", self.amortization_schedule),
            enum_param_item.to_kv("direction", self.direction),
            enum_param_item.to_kv("indexAverageMethod", self.index_average_method),
            enum_param_item.to_kv("indexCompoundingMethod", self.index_compounding_method),
            enum_param_item.to_kv("indexResetFrequency", self.index_reset_frequency),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            enum_param_item.to_kv("interestPaymentFrequency", self.interest_payment_frequency),
            enum_param_item.to_kv("interestType", self.interest_type),
            enum_param_item.to_kv("paymentBusinessDayConvention", self.payment_business_day_convention),
            enum_param_item.to_kv("paymentRollConvention", self.payment_roll_convention),
            enum_param_item.to_kv("stubRule", self.stub_rule),
            datetime_param_item.to_kv("endDate", self.end_date),
            datetime_param_item.to_kv("firstAccrualDate", self.first_accrual_date),
            datetime_param_item.to_kv("firstRegularPaymentDate", self.first_regular_payment_date),
            param_item.to_kv("fixedRatePercent", self.fixed_rate_percent),
            param_item.to_kv("floorStrikePercent", self.floor_strike_percent),
            param_item.to_kv("indexFixingLag", self.index_fixing_lag),
            param_item.to_kv("indexFixingRic", self.index_fixing_ric),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("interestPaymentDelay", self.interest_payment_delay),
            param_item.to_kv("isPerpetual", self.is_perpetual),
            datetime_param_item.to_kv("issueDate", self.issue_date),
            datetime_param_item.to_kv("lastRegularPaymentDate", self.last_regular_payment_date),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("paymentBusinessDays", self.payment_business_days),
            param_item.to_kv("spreadBp", self.spread_bp),
            param_item.to_kv("template", self.template),
            enum_param_item.to_kv("indexObservationMethod", self.index_observation_method),
            param_item.to_kv("fixedRatePercentSchedule", self.fixed_rate_percent_schedule),
            param_item.to_kv("instrumentTag", self.instrument_tag),
        ]
