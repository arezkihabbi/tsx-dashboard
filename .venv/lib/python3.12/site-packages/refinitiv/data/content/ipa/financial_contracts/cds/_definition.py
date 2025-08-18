from typing import Optional, TYPE_CHECKING

from . import PricingParameters
from ._cds_definition import CdsInstrumentDefinition
from ._premium_leg_definition import PremiumLegDefinition
from ._protection_leg_definition import ProtectionLegDefinition
from .._base_financial_contracts_definition import BaseFinancialContractsDefinition
from ..._enums import BusinessDayConvention, CdsConvention
from ...._content_provider_layer import PosArgsWarnMixin
from ....._tools import try_copy_to_list

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
    instrument_code : str, optional
        A cds RIC that is used to retrieve the description of the cds contract.
        Optional. If null, the protection_leg and the premium_leg  must be provided.
    cds_convention : CdsConvention, optional
        Define the cds convention. Optional. Defaults to 'ISDA'.
    trade_date : str or date, optional
        The date the cds contract was created. Optional. By default the valuation date.
    step_in_date : str or date, optional
        The effective protection date. Optional. By default the trade_date + 1 calendar.
    start_date : str or date or datetime or timedelta, optional
        The date the cds starts accruing interest. Its effective date. Optional. By
        default it is the accrued_begin_date (the last IMM date before trade_date) if
        cds_convention is ISDA, else it is the step_in_date.
    end_date : str or date or datetime or timedelta, optional
        The maturity date of the cds contract. Mandatory if instrument_code is null.
        Either the end_date or the tenor must be provided.
    tenor : str, optional
        The period code that represents the time between the start date and end date the
        contract. Mandatory if instrument_code is null. Either the end_date or the tenor
        must be provided.
    start_date_moving_convention : BusinessDayConvention, optional
        The method to adjust the start_date. Optional. By default 'NoMoving' is used.
    end_date_moving_convention : BusinessDayConvention, optional
        The method to adjust the end_date. Optional. By default 'NoMoving' is used.
    adjust_to_isda_end_date : bool, optional
        The way the end_date is adjusted if computed from tenor input. Optional.
        By default true is used if cds_convention is ISDA, else false is used.
    protection_leg : ProtectionLegDefinition, optional
        The Protection Leg of the CDS. It is the default leg. Mandatory if instrumenCode
        is null. Optional if instrument_code not null.
    premium_leg : PremiumLegDefinition, optional
        The Premium Leg of the CDS. It is a swap leg paying a fixed coupon. Mandatory if
        instrument_code is null. Optional if instrument_code not null.
    accrued_begin_date : str, optional
        The last cashflow date. Optional. By default it is the last cashflow date.
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
        Get stream object of this definition

    Examples
    --------
    >>> import refinitiv.data.content.ipa.financial_contracts as rdf
    >>> definition = rdf.cds.Definition(
    ...     instrument_tag="Cds1_InstrumentCode",
    ...     instrument_code="BNPP5YEUAM=R",
    ...     cds_convention=rdf.cds.CdsConvention.ISDA,
    ...     end_date_moving_convention=rdf.cds.BusinessDayConvention.NO_MOVING,
    ...     adjust_to_isda_end_date=True,
    ...     pricing_parameters=rdf.cds.PricingParameters(
    ...         market_data_date="2020-01-01"
    ...     ),
    ...     fields=[
    ...         "InstrumentTag",
    ...         "ValuationDate",
    ...         "InstrumentDescription",
    ...         "StartDate",
    ...         "EndDate",
    ...         "SettlementDate",
    ...         "UpfrontAmountInDealCcy",
    ...         "CashAmountInDealCcy",
    ...         "AccruedAmountInDealCcy",
    ...         "AccruedBeginDate",
    ...         "NextCouponDate",
    ...         "UpfrontPercent",
    ...         "ConventionalSpreadBp",
    ...         "ParSpreadBp",
    ...         "AccruedDays",
    ...         "ErrorCode",
    ...         "ErrorMessage",
    ...     ],
    ... )
    >>> response = definition.get_data()
    >>> df = response.data.df
    """

    _WARN_NAME = "financial_contracts.cds.Definition"
    _WARN_EX = "use financial_contracts.cds.Definition(instrument_code='BNPP5YEUAM=R') instead of financial_contracts.cds.Definition('BNPP5YEUAM=R')"

    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        instrument_code: Optional[str] = None,
        cds_convention: Optional[CdsConvention] = None,
        trade_date: "OptDateTime" = None,
        step_in_date: "OptDateTime" = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        start_date_moving_convention: Optional[BusinessDayConvention] = None,
        end_date_moving_convention: Optional[BusinessDayConvention] = None,
        adjust_to_isda_end_date: Optional[bool] = None,
        protection_leg: Optional[ProtectionLegDefinition] = None,
        premium_leg: Optional[PremiumLegDefinition] = None,
        accrued_begin_date: "OptDateTime" = None,
        fields: "OptStrStrs" = None,
        pricing_parameters: Optional[PricingParameters] = None,
        extended_params: "ExtendedParams" = None,
    ):
        fields = try_copy_to_list(fields)
        definition = CdsInstrumentDefinition(
            cds_convention=cds_convention,
            end_date_moving_convention=end_date_moving_convention,
            premium_leg=premium_leg,
            protection_leg=protection_leg,
            start_date_moving_convention=start_date_moving_convention,
            accrued_begin_date=accrued_begin_date,
            adjust_to_isda_end_date=adjust_to_isda_end_date,
            end_date=end_date,
            instrument_code=instrument_code,
            instrument_tag=instrument_tag,
            start_date=start_date,
            step_in_date=step_in_date,
            tenor=tenor,
            trade_date=trade_date,
        )
        super().__init__(
            definition=definition,
            fields=fields,
            pricing_parameters=pricing_parameters,
            extended_params=extended_params,
        )
