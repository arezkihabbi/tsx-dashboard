from typing import Optional, Union, List, TYPE_CHECKING

from ._cap_floor_definition import CapFloorInstrumentDefinition
from ._cap_floor_pricing_parameters import PricingParameters
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..._enums import (
    AdjustInterestToPaymentDate,
    IndexResetType,
    Frequency,
    DateRollingConvention,
    DayCountBasis,
    StubRule,
    BuySell,
    BusinessDayConvention,
    PriceSide,
)
from ..._enums import InterestCalculationConvention
from ..._models import AmortizationItem, BarrierDefinitionElement
from ..._models import InputFlow
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import validate_types, try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs, OptDateTime


class Definition(BaseFinancialContractsDefinition, PosArgsWarnMixin):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
    start_date : str or date or datetime or timedelta, optional
        The option start date
    end_date : str or date or datetime or timedelta, optional
        The maturity date of the CapFloor
    tenor : str, optional
        Tenor of the option
    notional_ccy : str, optional
        The ISO code of the notional currency. Mandatory if instrument code or
        instrument style has not been defined. In case an instrument code/style has been
        defined, value may comes from the reference data.
    notional_amount : float, optional
        The notional amount of the leg at the period start date. Optional. By default
        1,000,000 is used.
    index_name : str, optional
        The name of the floating rate index.
    index_tenor : str, optional
        The period code that represents the maturity of the floating rate index.
        Mandatory when the leg is float.
    interest_payment_frequency : Frequency or str, optional
        The frequency of the interest payments. Optional if an instrument code/style
        have been defined : in that case, value comes from reference data. Otherwise, it
        is mandatory.
    interest_calculation_method : DayCountBasis or str, optional
        The Day Count Basis method used to calculate the coupon interest payments.
        Mandatory.
    payment_business_day_convention : BusinessDayConvention or str, optional
        The method to adjust dates to a working day.
    payment_roll_convention : DateRollingConvention or str, optional
        The method to adjust payment dates whn they fall at the end of the month (28th
        of February, 30th, 31st). Optional. By default 'SameDay' is used.
    index_reset_frequency : Frequency or str, optional
        The reset frequency in case the leg Type is Float. Optional. By default the
        IndexTenor is used.
    index_reset_type : IndexResetType or str, optional
        A flag that indicates if the floating rate index is reset before the coupon
        period starts or at the end of the coupon period. Optional. By
          default 'InAdvance' is used.
    index_fixing_lag : int, optional
        Defines the positive number of working days between the fixing date and the
        start of the coupon period ('InAdvance') or the end of the coupon period
        ('InArrears'). Optional. By default 0 is used.
    amortization_schedule : list of AmortizationItem, optional
        Definition of amortizations
    payment_business_days : str, optional
        A list of coma-separated calendar codes to adjust dates (e.g. 'EMU' or 'USA').
        Optional. By default, the calendar associated to NotionalCcy is used.
    adjust_interest_to_payment_date : AdjustInterestToPaymentDate or str, optional
        A flag that indicates if the coupon dates are adjusted to the payment dates.
        Optional. By default, 'false' is used.
    stub_rule : StubRule or str, optional
        The rule that defines whether coupon roll dates are aligned on the  maturity or
        the issue date. Optional. By default, 'Maturity' is used.
    barrier_definition : BarrierDefinitionElement, optional

    buy_sell : BuySell, optional
        The side of the deal. Possible values:
        - Buy
        - Sell
    annualized_rebate : bool, optional

    cap_digital_payout_percent : float, optional

    cap_strike_percent : float, optional
        Cap leg strike expressed in %
    cms_template : str, optional
        A reference to a common swap contract that represents the underlying swap in
        case of a Constant Maturity Swap contract (CMS). Mandatory for CMS contract.
    floor_digital_payout_percent : float, optional

    floor_strike_percent : float, optional
        Floor leg strike expressed in %
    index_fixing_ric : str, optional
        The RIC that carries the fixing value. This value overrides the RIC associated
        by default with the IndexName and IndexTenor. Optional.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. Optional. If pricing
        parameters are not provided at this level parameters defined globally at the
        request level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters
    index_price_side : PriceSide, optional
        The side that is selected for an index supporting Bid/Ask/Mid (which is the case of deposits).
    cap_strike_percent_schedule : dict, optional
        The schedule of the dates and cap strike rates. The rates are expressed in percentages.
        Either capStrikePercent or capStrikePercentSchedule must be provided.
        No default value applies.
    floor_strike_percent_schedule : dict, optional
        The schedule of the dates and floor strike rates. The rates are expressed in percentages.
        Either FloorStrikePercent or FloorStrikePercentSchedule must be provided.
        No default value applies.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_stream(session=session)
        Get stream object of this definition

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.cap_floor.Definition(
    ...    instrument_tag="CapOnCms",
    ...    stub_rule=rdf.cap_floor.StubRule.MATURITY,
    ...    notional_ccy="USD",
    ...    start_date="2018-06-15",
    ...    end_date="2022-06-15",
    ...    notional_amount=1000000,
    ...    index_name="Composite",
    ...    index_tenor="5Y",
    ...    interest_calculation_method="Dcb_Actual_360",
    ...    interest_payment_frequency=rdf.cap_floor.Frequency.QUARTERLY,
    ...    buy_sell=rdf.cap_floor.BuySell.BUY,
    ...    cap_strike_percent=1,
    ...    pricing_parameters=rdf.cap_floor.PricingParameters(
    ...        skip_first_cap_floorlet=False, valuation_date="2020-02-07"
    ...    ),
    ...    fields=[
    ...        "InstrumentTag",
    ...        "InstrumentDescription",
    ...        "StartDate",
    ...        "EndDate",
    ...        "InterestPaymentFrequency",
    ...        "IndexRic",
    ...        "CapStrikePercent",
    ...        "FloorStrikePercent",
    ...        "NotionalCcy",
    ...        "NotionalAmount",
    ...        "PremiumBp",
    ...        "PremiumPercent",
    ...        "MarketValueInDealCcy",
    ...        "MarketValueInReportCcy",
    ...        "ErrorMessage",
    ...    ],
    ...)
    >>> response = definition.get_data()

    Using get_stream

    >>> stream = definition.get_stream()
    """

    _WARN_NAME = "financial_contracts.cap_floor.Definition"
    _WARN_EX = "use financial_contracts.cap_floor.Definition(instrument_tag='CapOnCms') instead of financial_contracts.cap_floor.Definition('CapOnCms')"

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
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
        payments: Optional[List[InputFlow]] = None,
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
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
        index_price_side: Optional[PriceSide] = None,
        cap_strike_percent_schedule: Optional[dict] = None,
        floor_strike_percent_schedule: Optional[dict] = None,
    ):
        validate_types(index_fixing_lag, [int, type(None)], "index_fixing_lag")

        amortization_schedule = try_copy_to_list(amortization_schedule)
        payments = try_copy_to_list(payments)
        fields = try_copy_to_list(fields)
        definition = CapFloorInstrumentDefinition(
            instrument_tag=instrument_tag,
            start_date=start_date,
            end_date=end_date,
            tenor=tenor,
            notional_ccy=notional_ccy,
            notional_amount=notional_amount,
            index_name=index_name,
            index_tenor=index_tenor,
            interest_payment_frequency=interest_payment_frequency,
            interest_calculation_method=interest_calculation_method,
            payment_business_day_convention=payment_business_day_convention,
            payment_roll_convention=payment_roll_convention,
            index_reset_frequency=index_reset_frequency,
            index_reset_type=index_reset_type,
            index_fixing_lag=index_fixing_lag,
            amortization_schedule=amortization_schedule,
            payment_business_days=payment_business_days,
            adjust_interest_to_payment_date=adjust_interest_to_payment_date,
            stub_rule=stub_rule,
            barrier_definition=barrier_definition,
            buy_sell=buy_sell,
            interest_calculation_convention=interest_calculation_convention,
            payments=payments,
            annualized_rebate=annualized_rebate,
            cap_digital_payout_percent=cap_digital_payout_percent,
            cap_strike_percent=cap_strike_percent,
            cms_template=cms_template,
            floor_digital_payout_percent=floor_digital_payout_percent,
            floor_strike_percent=floor_strike_percent,
            index_fixing_ric=index_fixing_ric,
            is_backward_looking_index=is_backward_looking_index,
            is_rfr=is_rfr,
            is_term_rate=is_term_rate,
            index_price_side=index_price_side,
            cap_strike_percent_schedule=cap_strike_percent_schedule,
            floor_strike_percent_schedule=floor_strike_percent_schedule,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
