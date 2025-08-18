from typing import Union, TYPE_CHECKING

from ._barrier_definition import EtiBarrierDefinition
from ._binary_definition import EtiBinaryDefinition
from ._cbbc_definition import EtiCbbcDefinition
from ._eti_definition import EtiDefinition
from ._fixing_info import EtiFixingInfo
from ._pricing_parameters import PricingParameters
from ._underlying_definition import EtiUnderlyingDefinition
from .._base_option_definition import BaseOptionDefinition
from ..._enums import BuySell, CallPut, ExerciseStyle, UnderlyingType
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import validate_types, try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs


class Definition(BaseOptionDefinition, PosArgsWarnMixin):
    """
    Parameters
    ----------
    instrument_tag : str, optional
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
    strike : float, optional
        strike of the option
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. Optional. If pricing
        parameters are not provided at this level parameters defined globally at the
        request level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters
    buy_sell : BuySell or str, optional
        The side of the deal.
    call_put : CallPut or str, optional
        Tells if the option is a call or a put.
    exercise_style : ExerciseStyle or str, optional
        EURO or AMER
    end_date : str, optional
        Expiry date of the option
    asian_definition : FxOptionAverageInfo, EtiOptionFixingInfo, optional
        Fixing details for asian options
    barrier_definition : FxOptionBarrierDefinition, EtiOptionBarrierDefinition, optional
        Details for barrier option.
    binary_definition : FxOptionBinaryDefinition, EtiOptionBinaryDefinition, optional
        Details for binary option.
    underlying_definition : FxUnderlyingDefinition, EtiUnderlyingDefinition, optional
        Details of the underlying. Can be used to override some data of the underlying.
    instrument_code : str, optional
        An option RIC that is used to retrieve the description of the
        EtiOptionDefinition contract. Optional.If null, the instrument_code of
        underlying_definition must be provided.
    cbbc_definition : EtiOptionCbbcDefinition, optional
        Details for CBBC (Call Bear/Bull Contract) option.
    deal_contract : int, optional
        deal_contract. It is the number of contracts bought or sold in the deal.
    end_date_time : str, optional
        Expiry date time of the option
    lot_size : float, optional
        The lot size. It is the number of options bought or sold in one transaction.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.


    Methods
    -------
    get_data(session=session)
        Returns a response to the data platform
    get_stream(session=session)
        Get stream quantitative analytic service subscription

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.eti_option.Definition(
    ...    instrument_code="FCHI560000L1.p",
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

    _WARN_NAME = "financial_contracts.eti_option.Definition"
    _WARN_EX = "use financial_contracts.eti_option.Definition(instrument_code='FCHI560000L1.p') instead of financial_contracts.eti_option.Definition('FCHI560000L1.p')"

    def __init__(
        self,
        underlying_definition: EtiUnderlyingDefinition = None,
        pricing_parameters: PricingParameters = None,
        instrument_tag: str = None,
        strike: float = None,
        buy_sell: Union[BuySell, str] = None,
        call_put: Union[CallPut, str] = None,
        exercise_style: Union[ExerciseStyle, str] = None,
        end_date: str = None,
        asian_definition: EtiFixingInfo = None,
        barrier_definition: EtiBarrierDefinition = None,
        binary_definition: EtiBinaryDefinition = None,
        cbbc_definition: EtiCbbcDefinition = None,
        instrument_code: str = None,
        lot_size: float = None,
        deal_contract: int = None,
        end_date_time: str = None,
        time_zone_offset: int = None,
        fields: "OptStrStrs" = None,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(deal_contract, [int, type(None)], "deal_contract")
        fields = try_copy_to_list(fields)

        definition = EtiDefinition(
            asian_definition=asian_definition,
            barrier_definition=barrier_definition,
            binary_definition=binary_definition,
            buy_sell=buy_sell,
            call_put=call_put,
            cbbc_definition=cbbc_definition,
            deal_contract=deal_contract,
            end_date=end_date,
            end_date_time=end_date_time,
            exercise_style=exercise_style,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            lot_size=lot_size,
            strike=strike,
            time_zone_offset=time_zone_offset,
            underlying_definition=underlying_definition,
            underlying_type=UnderlyingType.ETI,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
