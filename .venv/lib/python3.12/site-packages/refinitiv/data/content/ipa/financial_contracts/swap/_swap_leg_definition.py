from typing import Optional, List, Union

from ..._enums import (
    AdjustInterestToPaymentDate,
    BusinessDayConvention,
    DateRollingConvention,
    DayCountBasis,
    Direction,
    Frequency,
    IndexAverageMethod,
    IndexCompoundingMethod,
    IndexObservationMethod,
    IndexResetType,
    IndexSpreadCompoundingMethod,
    InterestCalculationConvention,
    InterestType,
    NotionalExchange,
    StubRule,
    PriceSide,
)
from ..._models import AmortizationItem
from ..._param_item import enum_param_item, list_serializable_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._tools import try_copy_to_list
from ....._types import OptDateTime


class LegDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional

    leg_tag : str, optional
        A user-defined string to identify the direction of the leg: 'paid' or
        'received'. optional. no default value applies.
    direction : Direction or str, optional
        The indication whether the cash flows of the instrument's leg are paid or
        received. the possible values are:   paid: the cash flows are paid to the
        counterparty,   received: the cash flows are received from the counterparty.  no
        default value applies.
    interest_type : InterestType or str, optional
        An indicator whether the instrument pays a fixed or floating interest. the
        possible values are: fixed, float. no default value applies.
    notional_ccy : str, optional
        The currency of the instrument's notional amount. the value is expressed in iso
        4217 alphabetical format (e.g. 'usd'). no default value applies.
    notional_amount : float, optional
        The notional amount of the instrument's leg. the default value is '1,000,000'.
    fixed_rate_percent : float, optional
        The interest rate of the instrument. the value is expressed in percentages.
        mandatory if no instrumentcode is defined. if instrumentcode is defined, the
        value comes from the instrument reference data.
    index_name : str, optional
        The name of the floating rate index (e.g. 'euribor'). no default value applies.
    index_tenor : str, optional
        The period code indicating the maturity of the floating rate index. the default
        value is the tenor equivalent toindexresetfrequency or interestpaymentfrequency.
    spread_bp : float, optional
        The interest spread in basis points that is added to the floating rate index
        value. optional. if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is '0'.
    interest_payment_frequency : Frequency or str, optional
        The frequency of the interest payment. either indexresetfrequency or
        interestpaymentfrequency must be provided (e.g. annual, semiannual).   the
        default value is indexresetfrequency.
    interest_calculation_method : DayCountBasis or str, optional
        The day count basis method used to calculate the interest payments(e.g.
        dcb_30_360, dcb_30_actual). the default value is selected based onnotionalccy.
    accrued_calculation_method : DayCountBasis or str, optional
        The day count basis method used to calculate the accrued interest payments (e.g.
        dcb_30_360, dcb_30_actual).   if instrumentcode is defined, the value comes from
        the instrument reference data. in case of a user-defined instrument,
        interestcalculationmethod is used.
    payment_business_day_convention : BusinessDayConvention or str, optional
        The method to adjust dates to working days. the possible values are:
        previousbusinessday,    nextbusinessday,    modified following,    nomoving,
        bbswmodifiedfollowing.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'modifiedfollowing'.
    payment_roll_convention : DateRollingConvention or str, optional
        The method to adjust payment dates when they fall at the end of the month (e.g.
        28th of february, 30th, 31st). the possible values are:    last,    same,
        last28,    same28.   if instrumentcode is defined, the value comes from the
        instrument reference data. in case of a user-defined instrument, the default
        value is'same'.
    index_reset_frequency : Frequency or str, optional
        The reset frequency for the floating instrument (e.g. annual, semiannual).   the
        default value is interestpaymentfrequency.
    index_reset_type : IndexResetType or str, optional
        A type indicating if the floating rate index is reset before the coupon period
        starts or at the end of the coupon period. the possible values are: inadvance:
        resets the index before the start of the interest period, inarrears: resets the
        index at the end of the interest period. the default value is 'inadvance'.
    index_fixing_lag : int, optional
        The number of working daysbetween the fixing date and the start of the coupon
        period ('inadvance') or the end of the coupon period ('inarrears'). the
        inadvance/inarrears mode is set in the indexresettype parameter. the default
        value is the fixing lag associated to the index defined/determined by default on
        the floating instrument.
    first_regular_payment_date : str or date or datetime or timedelta, optional
        The first regular interest payment date used for the odd first interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
    last_regular_payment_date : str or date or datetime or timedelta, optional
        The last regular interest payment date used for the odd last interest period.
        the value is expressed in iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g.
        2021-01-01t00:00:00z). no default value applies.
    amortization_schedule : AmortizationItem, optional
        The amortization schedule of the instrument. it contains the following
        information:   startdate,   enddate,   remainingnotional,
        amortizationfrequency,   amount,   amortizationtype.  optional. no default value
        applies.
    payment_business_days : str, optional
        A list of comma-separated calendar codes to adjust dates (e.g. 'emu' or 'usa').
        the default value is the calendar associated to the market conventions of the
        interestpaymentccy for the corresponding leg.
    notional_exchange : NotionalExchange or str, optional
        An indicator if the notional amount is exchanged and when it is exchanged. the
        possible values are:    none,    start,    end,    both,    endadjustment.   the
        default value is 'none'.
    adjust_interest_to_payment_date : AdjustInterestToPaymentDate or str, optional
        An indication if the coupon dates are adjusted to the payment dates. the
        possible values are:   adjusted,   unadjusted.  if instrumentcode is defined,
        the value comes from the instrument reference data. in case of a user-defined
        instrument, the default value is 'adjusted'.
    index_compounding_method : IndexCompoundingMethod or str, optional
        The method how the interest rate is calculated from the reset floating rates
        when the reset frequency is higher than the interest payment frequency (e.g.
        daily index reset with quarterly interest payments). the possible values are:
        compounded, average, constant, adjustedcompounded, mexicancompounded. if
        instrumentcode is defined, the value comes from the instrument reference data.
        in case of a user-defined instrument, the default value is 'constant'.
    interest_payment_delay : int, optional
        The number of working days between the end of the interest accrual period and
        the interest payment date. by default, no delay (0) is applied.
    stub_rule : StubRule or str, optional
        The rule that defines whether coupon roll dates are aligned to the maturity or
        issue date. the possible values are:   issue,   maturity,   shortfirstprorata,
        shortfirstfull,   longfirstfull,   shortlastprorata.  the default value is
        'maturity'.
    index_average_method : IndexAverageMethod or str, optional
        The value of the average index calculation method. the possible values are:
        compoundedactual,      dailycompoundedaverage,      compoundedaveragerate,
        arithmeticaverage
    index_observation_method : IndexObservationMethod or str, optional
        (rfr) method for determining the accrual observation period. the possible values
        are:      lookback: use the interest period for both rate accrual and interest
        payment.      periodshift: use the observation period for both rate accrual and
        interest payment.      mixed: use the observation period for rate accrual and
        the interest period for interest payment.
    index_spread_compounding_method : IndexSpreadCompoundingMethod or str, optional
        The method defining how the computed float leg spread is applied to compounded
        rate. it applies only when indexcompoundingmethod= compounded. the possible
        values are:    isdacompounding,    nocompounding,    isdaflatcompounding.  the
        default value is 'isdacompounding'.
    interest_calculation_convention : InterestCalculationConvention or str, optional
        The day count basis method convention used to calculate the interest payments.
        optional. defaults to moneymarket. if instrumentcode is defined, the value comes
        from the instrument reference data.
    cms_template : str, optional
        A reference to a common swap contract that represents the underlying swap in
        case of a constant maturity swap contract (cms). example: eur_ab6e. no default
        value applies.
    floor_strike_percent : float, optional
        The contractual strike rate of the floor. the value is expressed in percentages.
        if this parameter is set, the floor will apply to the leg with the same
        parameters set in the swaplegdefinition (e.g.maturity, frequency, index,
        discounting rule). no default value applies.
    index_fixing_ric : str, optional
        The ric that carries the fixing value if the instrument has a floating interest.
        optional. mandatory for floating rate instruments if no instrumentcode is
        defined. if instrumentcode is defined, the value comes from the instrument
        reference data. no default value applies.
    upfront_amount : float, optional
        The amount which represents the net present value of the swap. it is computed as
        [(100  dirtypricepercent / 100) x notionalamount]. the value is expressed in
        upfrontamountccy. by default, no payment (0) applies.
    index_price_side : PriceSide or str, optional
        The side that is selected for an index supporting Bid/Ask/Mid (which is the case of deposits).
    fixed_rate_percent_schedule : dict, optional
        The step structure: a list of pre-determined future coupon rates indexed by their dates.
        Either fixedRatePercent or fixedRatePercentSchedule is used.
        No default value applies.
    """

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        leg_tag: Optional[str] = None,
        direction: Union[Direction, str] = None,
        interest_type: Union[InterestType, str] = None,
        notional_ccy: Optional[str] = None,
        notional_amount: Optional[float] = None,
        fixed_rate_percent: Optional[float] = None,
        index_name: Optional[str] = None,
        index_tenor: Optional[str] = None,
        spread_bp: Optional[float] = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        accrued_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_day_convention: Union[BusinessDayConvention, str] = None,
        payment_roll_convention: Union[DateRollingConvention, str] = None,
        index_reset_frequency: Union[Frequency, str] = None,
        index_reset_type: Union[IndexResetType, str] = None,
        index_fixing_lag: Optional[int] = None,
        first_regular_payment_date: "OptDateTime" = None,
        last_regular_payment_date: "OptDateTime" = None,
        amortization_schedule: Optional[List[AmortizationItem]] = None,
        payment_business_days: Optional[str] = None,
        notional_exchange: Union[NotionalExchange, str] = None,
        adjust_interest_to_payment_date: Union[AdjustInterestToPaymentDate, str] = None,
        index_compounding_method: Union[IndexCompoundingMethod, str] = None,
        interest_payment_delay: Optional[int] = None,
        stub_rule: Union[StubRule, str] = None,
        index_average_method: Union[IndexAverageMethod, str] = None,
        index_observation_method: Union[IndexObservationMethod, str] = None,
        index_spread_compounding_method: Union[IndexSpreadCompoundingMethod, str] = None,
        interest_calculation_convention: Union[InterestCalculationConvention, str] = None,
        cms_template: Optional[str] = None,
        floor_strike_percent: Optional[float] = None,
        index_fixing_ric: Optional[str] = None,
        upfront_amount: Optional[float] = None,
        index_price_side: Union[PriceSide, str] = None,
        fixed_rate_percent_schedule: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.leg_tag = leg_tag
        self.direction = direction
        self.interest_type = interest_type
        self.notional_ccy = notional_ccy
        self.notional_amount = notional_amount
        self.fixed_rate_percent = fixed_rate_percent
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.spread_bp = spread_bp
        self.interest_payment_frequency = interest_payment_frequency
        self.interest_calculation_method = interest_calculation_method
        self.accrued_calculation_method = accrued_calculation_method
        self.payment_business_day_convention = payment_business_day_convention
        self.payment_roll_convention = payment_roll_convention
        self.index_reset_frequency = index_reset_frequency
        self.index_reset_type = index_reset_type
        self.index_fixing_lag = index_fixing_lag
        self.first_regular_payment_date = first_regular_payment_date
        self.last_regular_payment_date = last_regular_payment_date
        self.amortization_schedule = try_copy_to_list(amortization_schedule)
        self.payment_business_days = payment_business_days
        self.notional_exchange = notional_exchange
        self.adjust_interest_to_payment_date = adjust_interest_to_payment_date
        self.index_compounding_method = index_compounding_method
        self.interest_payment_delay = interest_payment_delay
        self.stub_rule = stub_rule
        self.index_average_method = index_average_method
        self.index_observation_method = index_observation_method
        self.index_spread_compounding_method = index_spread_compounding_method
        self.interest_calculation_convention = interest_calculation_convention
        self.cms_template = cms_template
        self.floor_strike_percent = floor_strike_percent
        self.index_fixing_ric = index_fixing_ric
        self.upfront_amount = upfront_amount
        self.index_price_side = index_price_side
        self.fixed_rate_percent_schedule = fixed_rate_percent_schedule

    def _get_items(self):
        return [
            enum_param_item.to_kv("accruedCalculationMethod", self.accrued_calculation_method),
            enum_param_item.to_kv("adjustInterestToPaymentDate", self.adjust_interest_to_payment_date),
            list_serializable_param_item.to_kv("amortizationSchedule", self.amortization_schedule),
            enum_param_item.to_kv("direction", self.direction),
            enum_param_item.to_kv("indexAverageMethod", self.index_average_method),
            enum_param_item.to_kv("indexCompoundingMethod", self.index_compounding_method),
            enum_param_item.to_kv("indexObservationMethod", self.index_observation_method),
            enum_param_item.to_kv("indexResetFrequency", self.index_reset_frequency),
            enum_param_item.to_kv("indexResetType", self.index_reset_type),
            enum_param_item.to_kv("indexSpreadCompoundingMethod", self.index_spread_compounding_method),
            enum_param_item.to_kv("interestCalculationConvention", self.interest_calculation_convention),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            enum_param_item.to_kv("interestPaymentFrequency", self.interest_payment_frequency),
            enum_param_item.to_kv("interestType", self.interest_type),
            enum_param_item.to_kv("notionalExchange", self.notional_exchange),
            enum_param_item.to_kv("paymentBusinessDayConvention", self.payment_business_day_convention),
            enum_param_item.to_kv("paymentRollConvention", self.payment_roll_convention),
            enum_param_item.to_kv("stubRule", self.stub_rule),
            param_item.to_kv("cmsTemplate", self.cms_template),
            datetime_param_item.to_kv("firstRegularPaymentDate", self.first_regular_payment_date),
            param_item.to_kv("fixedRatePercent", self.fixed_rate_percent),
            param_item.to_kv("floorStrikePercent", self.floor_strike_percent),
            param_item.to_kv("indexFixingLag", self.index_fixing_lag),
            param_item.to_kv("indexFixingRic", self.index_fixing_ric),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("indexTenor", self.index_tenor),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("interestPaymentDelay", self.interest_payment_delay),
            datetime_param_item.to_kv("lastRegularPaymentDate", self.last_regular_payment_date),
            param_item.to_kv("legTag", self.leg_tag),
            param_item.to_kv("notionalAmount", self.notional_amount),
            param_item.to_kv("notionalCcy", self.notional_ccy),
            param_item.to_kv("paymentBusinessDays", self.payment_business_days),
            param_item.to_kv("spreadBp", self.spread_bp),
            param_item.to_kv("upfrontAmount", self.upfront_amount),
            enum_param_item.to_kv("indexPriceSide", self.index_price_side),
            param_item.to_kv("fixedRatePercentSchedule", self.fixed_rate_percent_schedule),
        ]
