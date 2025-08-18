from typing import Optional, List, TYPE_CHECKING

from ._fx_cross_definition import FxCrossInstrumentDefinition
from ._fx_cross_leg_definition import LegDefinition
from ._fx_cross_pricing_parameters import PricingParameters
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..._enums import FxCrossType
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import try_copy_to_list

if TYPE_CHECKING:
    from ....._types import ExtendedParams, OptStrStrs


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
    legs : list of LegDefinition, optional
        Extra parameters to describe further the contract. 1 leg is mandatory for
        Forwards and NDFs contracts. 2 legs are required for Swaps, and FwdFwdSwaps
        contracts. Optional for Spot contracts.
    fx_cross_type : FxCrossType or str, optional
        The type of the Fx Cross instrument. Mandatory.
    fx_cross_code : str, optional
        The ISO code of the cross currency (e.g. 'EURCHF'). Mandatory.
    ndf_fixing_settlement_ccy : str, optional
        In case of a NDF contract, the ISO code of the settlement currency (e.g. 'EUR'
        ). Optional.
    reference_spot_rate : float, optional
        Contractual Spot Rate the counterparties agreed. It is used to compute the
        traded_cross_rate as 'reference_spot_rate + traded_swap_points /
        FxSwapPointScalingFactor'. In the case of a "FxSwap" contract, it is also used
        to compute  nearLeg.ContraAmount from nearLeg.DealAmount as
        'nearLeg.ContraAmount = nearLeg.DealAmount *  (reference_spot_rate /
        FxCrossScalingFactor)'. Optional. Default value is null. In that case
        traded_cross_rate and Leg ContraAmount may not be computed.
    traded_cross_rate : float, optional
        The contractual exchange rate agreed by the two counterparties.  It is used to
        compute the ContraAmount if the amount is not filled.  In the case of a
        'FxForward' and 'FxNonDeliverableForward' contract : ContraAmount is computed as
        'DealAmount x traded_cross_rate / FxCrossScalingFactor'. In the case of a
        'FxSwap' contract : farLeg.ContraAmount is computed as 'nearLeg.DealAmount x
        traded_cross_rate / FxCrossScalingFactor'. Optional. Default value is null. It
        emans that if both ContraAmount and traded_cross_rate are sot set, market value
        cannot be computed.
    traded_swap_points : float, optional
        Contractual forward points agreed by the two counterparties. It is used to
        compute the traded_cross_rate as 'reference_spot_rate + traded_swap_points /
        FxSwapPointScalingFactor'. Optional. Default value is null. In that case
        traded_cross_rate and Leg ContraAmount may not be computed.
    fields: list of str, optional
        Contains the list of Analytics that the quantitative analytic service will
        compute.
    pricing_parameters : PricingParameters, optional
        The pricing parameters to apply to this instrument. Optional. If pricing
        parameters are not provided at this level parameters defined globally at the
        request level are used. If no pricing parameters are provided globally default
        values apply.
    extended_params : dict, optional
        If necessary other parameters.
    settlement_ccy : str, optional
        This settlement currency code in case of an FxNonDeliverableForward (NDF) contract.
        The value is expressed in ISO 4217 alphabetical format (e.g., 'USD').
        Default value is 'USD'.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_stream(session=session)
        Get stream quantitative analytic service subscription

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.cross.Definition(
    ...     instrument_tag="00102700008910C",
    ...     fx_cross_type=rdf.cross.FxCrossType.FX_FORWARD,
    ...     fx_cross_code="USDEUR",
    ...     legs=[rdf.cross.LegDefinition(end_date="2015-04-09T00:00:00Z")],
    ...     pricing_parameters=rdf.cross.PricingParameters(
    ...         valuation_date="2015-02-02T00:00:00Z",
    ...         price_side=rdf.cross.PriceSide.MID,
    ...     ),
    ...     fields=[
    ...         "InstrumentTag",
    ...         "ValuationDate",
    ...         "InstrumentDescription",
    ...         "FxOutrightCcy1Ccy2",
    ...     ],
    ... )
    >>> response = definition.get_data()
    >>> response.data.df

    Using get_stream
    >>> stream = definition.get_stream()
    """

    _WARN_NAME = "financial_contracts.cross.Definition"
    _WARN_EX = "use financial_contracts.cross.Definition(fx_cross_code='USDEUR') instead of financial_contracts.cross.Definition('USDEUR')"

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        legs: Optional[List[LegDefinition]] = None,
        fx_cross_type: Optional[FxCrossType] = None,
        fx_cross_code: Optional[str] = None,
        ndf_fixing_settlement_ccy: Optional[str] = None,
        reference_spot_rate: Optional[float] = None,
        traded_cross_rate: Optional[float] = None,
        traded_swap_points: Optional[float] = None,
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
        settlement_ccy: Optional[str] = None,
    ):
        legs = try_copy_to_list(legs)
        fields = try_copy_to_list(fields)
        definition = FxCrossInstrumentDefinition(
            fx_cross_type=fx_cross_type,
            legs=legs,
            fx_cross_code=fx_cross_code,
            instrument_tag=instrument_tag,
            ndf_fixing_settlement_ccy=ndf_fixing_settlement_ccy,
            reference_spot_rate=reference_spot_rate,
            traded_cross_rate=traded_cross_rate,
            traded_swap_points=traded_swap_points,
            settlement_ccy=settlement_ccy,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
