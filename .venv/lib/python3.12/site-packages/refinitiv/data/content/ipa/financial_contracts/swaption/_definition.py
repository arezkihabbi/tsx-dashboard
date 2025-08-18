from typing import Optional, TYPE_CHECKING, Union

from ._bermudan_swaption_definition import BermudanSwaptionDefinition
from ._swaption_definition import SwaptionInstrumentDefinition
from ._swaption_pricing_parameters import PricingParameters
from .. import swap
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..._enums import (
    BuySell,
    ExerciseStyle,
    SwaptionSettlementType,
    PremiumSettlementType,
    SwaptionType,
)
from ..._models import InputFlow
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
    instrument_tag : str, optional
        A user defined string to identify the instrument. it can be used to link output
        results to the instrument definition.limited to 40 characters.only alphabetic,
        numeric and '- _.#=@' characters are supported. optional. no default value
        applies.
    start_date : str or date or datetime or timedelta, optional
        The date the swaption starts. optional. by default it is derived from the
        tradedate and the day to spot convention of the contract currency.
    end_date : str or date or datetime or timedelta, optional
        The maturity or expiry date of the instrument's leg. the value is expressed in
        iso 8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g. 2021-01-01t00:00:00z). either
        tenor or enddate must be provided. the default value is valuationdate shifted
        forward by tenor.
    tenor : str, optional
        The code indicating the period between startdate and enddate of the instrument
        (e.g. '6m', '1y'). mandatory, if enddate is not provided. the default value is
        calculated from enddate.
    notional_amount : float, optional
        The notional amount of the instrument. the default value is '1,000,000'.
    bermudan_swaption_definition : BermudanSwaptionDefinition, optional

    buy_sell : BuySell, optional
        The indicator of the deal side. the possible values are:   buy: buying the
        option,   sell: selling/writing the option.  no default value applies.
    exercise_style : ExerciseStyle, optional
        The option style based on its exercise restrictions. the possible values are:
        amer,   euro,   berm.  note: all exercise styles may not apply to certain option
        no default value applies.
    payments : InputFlow, optional
        An array of payments
    premium_settlement_type : PremiumSettlementType or str, optional
        The cash settlement type of the option premium   spot,   forward.
    settlement_type : SwaptionSettlementType or str, optional
        The settlement method for options when exercised. the possible values are:
        physical: delivering the underlying asset, or for a swaption, physically
        entering into the underlying swap.    cash: paying out in cash.  the default
        value is 'physical'.
    swaption_type : SwaptionType or str, optional
        The indicator if the swaption is a payer or a receiver. the possible values are:
        receiver: a right to receive a fixed rate of the underlying swap,   payer: a
        right to pay a fixed rate of the underlying swap.  no default value applies.
    underlying_definition : SwapDefinition, optional

    spread_vs_atm_in_bp : float, optional
        Spread between strike and atm strike, expressed in basis points (bp).
    strike_percent : float, optional
        The set price at which the owner of the option can buy or sell the underlying
        asset. for a swaption, it is the fixed rate of the underlying swap at which the
        owner of the swaption can enter the swap. the value is expressed in percentages.
        by default, fixedratepercent of the underlying swap is used.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. If pricing parameters
        are not provided at this level parameters defined globally at the request
        level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters.
    delivery_date : str or date or datetime or timedelta, optional
        The date when the underlying asset is delivered.
        The value is expressed in ISO 8601 format: YYYY-MM-DDT[hh]:[mm]:[ss]Z (e.g. '2021-01-01T00:00:00Z').

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
    >>> definition = rdf.swaption.Definition(
    ...   buy_sell=rdf.swaption.BuySell.BUY,
    ...   call_put=rdf.swaption.CallPut.CALL,
    ...   exercise_style=rdf.swaption.ExerciseStyle.BERM,
    ...   underlying_definition=rdf.swap.Definition(tenor="3Y", template="EUR_AB6E"),
    ...)
    >>> response = definition.get_data()

    Using get_stream

    >>> stream = definition.get_stream()
    >>> stream.open()
    """

    _WARN_NAME = "financial_contracts.swaption.Definition"
    _WARN_EX = "use financial_contracts.swaption.Definition(instrument_tag='myEURswaption') instead of financial_contracts.swaption.Definition('myEURswaption')"

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        notional_amount: Optional[float] = None,
        bermudan_swaption_definition: Optional[BermudanSwaptionDefinition] = None,
        buy_sell: Optional[BuySell] = None,
        exercise_style: Optional[ExerciseStyle] = None,
        payments: Optional[InputFlow] = None,
        premium_settlement_type: Union[PremiumSettlementType, str] = None,
        settlement_type: Union[SwaptionSettlementType, str] = None,
        swaption_type: Union[SwaptionType, str] = None,
        underlying_definition: Optional[swap.Definition] = None,
        spread_vs_atm_in_bp: Optional[float] = None,
        strike_percent: Optional[float] = None,
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
        delivery_date: "OptDateTime" = None,
    ):
        fields = try_copy_to_list(fields)
        self.underlying_definition = underlying_definition
        definition = SwaptionInstrumentDefinition(
            bermudan_swaption_definition=bermudan_swaption_definition,
            buy_sell=buy_sell,
            exercise_style=exercise_style,
            payments=payments,
            premium_settlement_type=premium_settlement_type,
            settlement_type=settlement_type,
            swaption_type=swaption_type,
            underlying_definition=underlying_definition,
            end_date=end_date,
            instrument_tag=instrument_tag,
            notional_amount=notional_amount,
            spread_vs_atm_in_bp=spread_vs_atm_in_bp,
            start_date=start_date,
            strike_percent=strike_percent,
            tenor=tenor,
            delivery_date=delivery_date,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="content.ipa.financial_contracts.swaption",
            content=f"{{underlying_definition='{self.underlying_definition}'}}",
        )
