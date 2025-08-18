from typing import Optional, TYPE_CHECKING, Union

from ._term_deposit_definition import TermDepositInstrumentDefinition
from ._term_deposit_pricing_parameters import PricingParameters
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..._enums import BusinessDayConvention, DateRollingConvention, DayCountBasis, Frequency
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import create_repr, try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs, OptDateTime


class Definition(BaseFinancialContractsDefinition, PosArgsWarnMixin):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_code : str, optional
        Code to define the term deposit instrument. For the moment, only RICs for CDs
        and Wholesales deposits are supported, with deposit code (ex:"EUR1MD=").
    instrument_tag : str, optional
        User defined string to identify the instrument. It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported.
    start_date : str or date or datetime or timedelta, optional
        The date the term deposit starts accruing interest. Its effective date.
        By default it is derived from the ValuationDate and the day to spot convention
        of the contract currency.
    end_date : str or date or datetime or timedelta, optional
        The maturity date of the term deposit contract. Either the endDate or the tenor
        must be provided.
    tenor : str, optional
        The period code that represents the time between the start date and end date of
        the contract.
        Mandatory if instrumentCode is null. Either the endDate or the tenor must be
        provided.
    notional_ccy : str, optional
        The ISO code of the notional currency.
        Should be explicitly specified if InstrumentCode hasn't been specified.
        May be retrieved from reference data.
    notional_amount : float, optional
        The notional amount of the term deposit at the start date.
        By default 1,000,000 is used.
    fixed_rate_percent : float, optional
        Fixed interest rate percent to be applied for notional by deal terms.
        Mandatory if instrument_code is None.
    payment_business_day_convention : BusinessDayConvention, optional
        The method to adjust dates to a working day.
        By default 'ModifiedFollowing'.
    payment_roll_convention : DateRollingConvention, optional
        Method to adjust payment dates when they fall at the end of the month.
        By default 'Last'.
    year_basis : DayCountBasis or str, optional
        The Day Count Basis method used to calculate the interest payments.
        By default 'Dcb_Actual_365'.
    calendar : str, optional
        Calendar used to adjust deposit duration calculation.
        By default the calendar corresponding to notional currency is used.
    fields : list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. If pricing parameters
        are not provided at this level parameters defined globally at the request
        level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters.
    interest_payment_frequency : Frequency or str, optional
        The frequency of the interest payment.
        The default value is zero.
    interest_calculation_method : DayCountBasis or str, optional
        The day count basis method used to calculate the interest payments. The possible values are listed here.
        Mandatory if no instrumentCode is defined.
    payment_business_days : str, optional
        A comma-separated calendar code used to adjust dates(e.g., 'EMU' or 'USA').
        The default value is the calendar associated to the market conventions of NotionalCcy.
    start_tenor : str, optional
        The code indicating the period from a spot date to startDate of the instrument (e.g., '1M').
        Either startDate or startTenor can be specified, but not both.

    Methods
    -------
    get_data(session=session, on_response=on_response, async_mode=None)
        Returns a response to the data platform
    get_data_async(session=session, on_response=on_response, async_mode=None)
        Returns a response to the async data platform
    get_stream(session=session)
        Get stream quantitative analytic service subscription

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.term_deposit.Definition(
    ...   tenor="5Y",
    ...   notional_ccy="EUR",
    ...   fixed_rate_percent=11
    ...)
    >>> response = definition.get_data()

    Using get_stream

    >>> stream = definition.get_stream()
    >>> stream.open()
    """

    _WARN_NAME = "financial_contracts.term_deposit.Definition"
    _WARN_EX = "use financial_contracts.term_deposit.Definition(instrument_tag='AED_AM1A') instead of financial_contracts.term_deposit.Definition('AED_AM1A')"

    def __init__(
        self,
        instrument_code: Optional[str] = None,
        instrument_tag: Optional[str] = None,
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
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
        interest_payment_frequency: Union[Frequency, str] = None,
        interest_calculation_method: Union[DayCountBasis, str] = None,
        payment_business_days: Optional[str] = None,
        start_tenor: Optional[str] = None,
    ):
        fields = try_copy_to_list(fields)
        definition = TermDepositInstrumentDefinition(
            payment_business_day_convention=payment_business_day_convention,
            payment_roll_convention=payment_roll_convention,
            year_basis=year_basis,
            calendar=calendar,
            end_date=end_date,
            fixed_rate_percent=fixed_rate_percent,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            notional_amount=notional_amount,
            notional_ccy=notional_ccy,
            start_date=start_date,
            tenor=tenor,
            interest_payment_frequency=interest_payment_frequency,
            interest_calculation_method=interest_calculation_method,
            payment_business_days=payment_business_days,
            start_tenor=start_tenor,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self, middle_path="content.ipa.financial_contracts.term_deposit")
