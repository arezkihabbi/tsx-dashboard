import warnings
from typing import Optional, Union, TYPE_CHECKING

from ._underlying_type import UnderlyingType
from ..._enums import BuySell, CallPut, ExerciseStyle, SettlementType
from ._option_instrument_definition import OptionInstrumentDefinition
from ._option_pricing_parameters import PricingParameters
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..eti_option import (
    EtiUnderlyingDefinition,
    EtiBinaryDefinition,
    EtiBarrierDefinition,
    EtiCbbcDefinition,
    EtiDoubleBarriersDefinition,
    EtiFixingInfo,
)
from ..fx_option import (
    FxUnderlyingDefinition,
    FxBinaryDefinition,
    FxBarrierDefinition,
    FxDualCurrencyDefinition,
    FxAverageInfo,
    FxDoubleBarrierDefinition,
    FxDoubleBinaryDefinition,
    FxForwardStart,
)
from ..._models import InputFlow
from ....._tools import validate_types, try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs, OptDateTime
    from ...financial_contracts._stream_facade import Stream
    from ....._core.session import Session


class Definition(BaseFinancialContractsDefinition):
    """
    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
    end_date : str or date or datetime or timedelta, optional
        Expiry date of the option
    buy_sell : BuySell or str, optional
        The side of the deal.
    call_put : CallPut or str, optional
        Tells if the option is a call or a put.
    exercise_style : ExerciseStyle or str, optional
        EURO or AMER
    underlying_type : UnderlyingType, optional
        Underlying type of the option.
    strike : float, optional
        strike of the option
    tenor : str, optional
        tenor of the option
    notional_ccy : str, optional
        Currency of the notional amount If the option is a EURGBP Call option,
        notional_ccy can be expressed in EUR OR GBP
    notional_amount : float, optional
        The notional amount of currency If the option is a EURGBP Call option, amount of
        EUR or GBP of the contract
    asian_definition : FxOptionAverageInfo, EtiOptionFixingInfo, optional
        Fixing details for asian options
    barrier_definition : FxOptionBarrierDefinition, EtiOptionBarrierDefinition, optional
        Details for barrier option.
    binary_definition : FxOptionBinaryDefinition, EtiOptionBinaryDefinition, optional
        Details for binary option.
    double_barrier_definition : FxOptionDoubleBarrierDefinition, optional
        Details for double barriers option.
    double_binary_definition : FxOptionDoubleBinaryDefinition, optional
        Details for double binary option.
    dual_currency_definition : FxDualCurrencyDefinition, optional
        Details for dual currency option.
    forward_start_definition : FxOptionForwardStart, optional
        Details for Forward Start option.
    underlying_definition : FxUnderlyingDefinition, EtiUnderlyingDefinition, optional
        Details of the underlying. Can be used to override some data of the underlying.
    delivery_date : str or date or datetime or timedelta, optional
        Expiry date of the option
    instrument_code : str, optional
        An option RIC that is used to retrieve the description of the
        EtiOptionDefinition contract. Optional.If null, the instrument_code of
        underlying_definition must be provided.
    cbbc_definition : EtiOptionCbbcDefinition, optional
        Details for CBBC (Call Bear/Bull Contract) option.
    double_barriers_definition : EtiOptionDoubleBarriersDefinition, optional
        Details for double barriers option.
    deal_contract : int, optional
        deal_contract. It is the number of contracts bought or sold in the deal.
    end_date_time : str or date or datetime or timedelta, optional
        Expiry date time of the option
    lot_size : float, optional
        The lot size. It is the number of options bought or sold in one transaction.
    offset : int, optional
        offset. The offset in minutes between the time UTC and the time of the exchange
        where the contract is traded.
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

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_stream(session=session)
        Get stream quantitative analytic service subscription

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.option.Definition(
    ...    instrument_code="FCHI560000L1.p",
    ...    underlying_type=rdf.option.UnderlyingType.ETI,
    ...    fields=[
    ...        "MarketValueInDealCcy",
    ...        "DeltaPercent",
    ...        "GammaPercent",
    ...        "RhoPercent",
    ...        "ThetaPercent",
    ...        "VegaPercent",
    ...        "ErrorCode",
    ...        "ErrorMessage",
    ...    ],
    ... )
    >>> response = definition.get_data()

    Using get_stream

    >>> stream = definition.get_stream()
    """

    def __init__(
        self,
        asian_definition: Union[EtiFixingInfo, FxAverageInfo] = None,
        barrier_definition: Union[FxBarrierDefinition, EtiBarrierDefinition] = None,
        binary_definition: Union[FxBinaryDefinition, EtiBinaryDefinition] = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        cbbc_definition: Optional[EtiCbbcDefinition] = None,
        deal_contract: Optional[int] = None,
        delivery_date: "OptDateTime" = None,
        double_barrier_definition: Optional[FxDoubleBarrierDefinition] = None,
        double_barriers_definition: Optional[EtiDoubleBarriersDefinition] = None,
        double_binary_definition: Union[FxDoubleBinaryDefinition] = None,
        dual_currency_definition: Optional[FxDualCurrencyDefinition] = None,
        end_date: "OptDateTime" = None,
        end_date_time: "OptDateTime" = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        forward_start_definition: Optional[FxForwardStart] = None,
        instrument_code: Optional[str] = None,
        instrument_tag: Optional[str] = None,
        lot_size: Optional[float] = None,
        notional_amount: Optional[float] = None,
        notional_ccy: Optional[str] = None,
        payments: Optional[InputFlow] = None,
        settlement_ccy: Optional[str] = None,
        settlement_type: Union[SettlementType, str] = None,
        start_date: "OptDateTime" = None,
        strike: Optional[float] = None,
        tenor: Optional[str] = None,
        time_zone_offset: Optional[int] = None,
        underlying_definition: Union[FxUnderlyingDefinition, EtiUnderlyingDefinition] = None,
        underlying_type: Union[UnderlyingType, str] = None,
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
    ):
        warnings.warn(
            "The rd.content.ipa.financial_contracts.option module will be removed in future library version v2.0. "
            "Please use rd.content.ipa.financial_contracts.fx_option or rd.content.ipa.financial_contracts.eti_option instead.",
            category=FutureWarning,
        )
        validate_types(deal_contract, [int, type(None)], "deal_contract")
        fields = try_copy_to_list(fields)

        definition = OptionInstrumentDefinition(
            asian_definition=asian_definition,
            barrier_definition=barrier_definition,
            binary_definition=binary_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            cbbc_definition=cbbc_definition,
            deal_contract=deal_contract,
            delivery_date=delivery_date,
            double_barrier_definition=double_barrier_definition,
            double_barriers_definition=double_barriers_definition,
            double_binary_definition=double_binary_definition,
            dual_currency_definition=dual_currency_definition,
            end_date=end_date,
            end_date_time=end_date_time,
            exercise_style=exercise_style,
            forward_start_definition=forward_start_definition,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            lot_size=lot_size,
            notional_amount=notional_amount,
            notional_ccy=notional_ccy,
            payments=payments,
            settlement_ccy=settlement_ccy,
            settlement_type=settlement_type,
            start_date=start_date,
            strike=strike,
            tenor=tenor,
            time_zone_offset=time_zone_offset,
            underlying_definition=underlying_definition,
            underlying_type=underlying_type,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )

    def get_stream(self, session: Optional["Session"] = None) -> "Stream":
        fields = self._kwargs.get("fields")
        if fields is None:
            response = self.get_data(session=session)
            if isinstance(response.data.raw, dict) and "headers" in response.data.raw:
                fields = [item.get("name", "") for item in response.data.raw["headers"]]
                self._kwargs["fields"] = fields

        return super().get_stream(session=session)
