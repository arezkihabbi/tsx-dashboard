from typing import Optional, Union

from ..._enums import BusinessDayConvention, DayCountBasis, Direction, Frequency, StubRule
from ..._param_item import enum_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PremiumLegDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    direction : Direction or str, optional
        The direction of the leg.
    notional_ccy : str, optional
        The ISO code of the notional currency. Mandatory if instrument code or
        instrument style has not been defined. In case an instrument code/style has been
        defined, value may comes from the reference data.
    notional_amount : float, optional
        The notional amount of the leg at the period start date. Optional. By default
        1,000,000 is used.
    fixed_rate_percent : float, optional
        The fixed coupon rate in percentage. It is mandatory in case of a single leg
        instrument. Otherwise, in case of multi leg instrument, it can be computed as
        the Par rate.
    interest_payment_frequency : Frequency or str, optional
        The frequency of the interest payments. Optional if an instrument code/style
        have been defined : in that case, value comes from reference data. Otherwise, it
        is mandatory.
    interest_calculation_method : DayCountBasis or str, optional
        The Day Count Basis method used to calculate the coupon interest payments.
        Mandatory.
    accrued_calculation_method : DayCountBasis or str, optional
        The Day Count Basis method used to calculate the accrued interest payments.
        Optional. By default, the same value than interest_calculation_method is used.
    payment_business_day_convention : BusinessDayConvention or str, optional
        The method to adjust dates to a working day. Optional.
        In case an instrument code/style has been defined, value comes from
        bond reference data. Otherwise 'ModifiedFollowing' is used.
    first_regular_payment_date : str or date or datetime or timedelta, optional
        The first regular coupon payment date for leg with an odd first coupon.
        Optional.
    last_regular_payment_date : str or date or datetime or timedelta, optional
        The last regular coupon payment date for leg with an odd last coupon. Optional.
    payment_business_days : str, optional
        A list of coma-separated calendar codes to adjust dates (e.g. 'EMU' or 'USA').
        Optional. By default the calendar associated to notional_ccy is used.
    stub_rule : StubRule or str, optional
        The rule that defines whether coupon roll dates are aligned on the  maturity or
        the issue date. Optional. By default 'Maturity' is used.
    accrued_paid_on_default : bool, optional
        Specifies whether the accrued is paid at the credit event date or not.
        - true :  the accrued is paid at the credit event date
        - false :  the accrued is not paid at the credit event date Optional. Defaults
          to false.
    interest_payment_ccy : str, optional
        The ISO code of the interest payment currency. Mandatory.
    """

    def __init__(
        self,
        *,
        direction: Union[Direction, str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        accrued_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        first_regular_payment_date: OptDateTime = None,
        last_regular_payment_date: OptDateTime = None,
        payment_business_days: Optional[str] = None,
        stub_rule: Union[StubRule, str] = None,
        accrued_paid_on_default: Optional[bool] = None,
        interest_payment_ccy: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.direction = direction
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.accrued_calculation_method = accrued_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.first_regular_payment_date = first_regular_payment_date
        self.last_regular_payment_date = last_regular_payment_date
        self.payment_business_days = payment_business_days
        self.stub_rule = stub_rule
        self.accrued_paid_on_default = accrued_paid_on_default
        self.interest_payment_ccy = interest_payment_ccy

    def _get_items(self):
        return [
            enum_param_item.to_kv("accruedCalculationMethod", self.accrued_calculation_method),
            enum_param_item.to_kv("direction", self.direction),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            enum_param_item.to_kv("interestPaymentFrequency", self.interest_payment_frequency),
            enum_param_item.to_kv("paymentBusinessDayConvention", self.payment_business_day_convention),
            enum_param_item.to_kv("stubRule", self.stub_rule),
            param_item.to_kv("accruedPaidOnDefault", self.accrued_paid_on_default),
            datetime_param_item.to_kv("firstRegularPaymentDate", self.first_regular_payment_date),
            param_item.to_kv("fixedRatePercent", self.fixed_rate_percent),
            param_item.to_kv("interestPaymentCcy", self.interest_payment_ccy),
            datetime_param_item.to_kv("lastRegularPaymentDate", self.last_regular_payment_date),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("paymentBusinessDays", self.payment_business_days),
        ]
