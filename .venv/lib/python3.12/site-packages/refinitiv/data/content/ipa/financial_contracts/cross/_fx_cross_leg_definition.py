from typing import Optional, Union

from ..._enums import FxLegType, BuySell
from ..._param_item import enum_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class LegDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    start_date : str or date or datetime or timedelta, optional

    end_date : str or date or datetime or timedelta, optional
        The maturity date of the contract that is the date the amounts are exchanged.
        Either the end_date or the tenor must be provided.
    tenor : str, optional
        The tenor representing the maturity date of the contract (e.g. '1Y' or '6M' ).
        Either the end_date or the tenor must be provided.
    leg_tag : str, optional
        A user defined string to identify the leg. Optional.
    deal_ccy_buy_sell : BuySell or str, optional
        The direction of the trade in terms of the deal currency.
        Optional. Defaults to 'Buy'
    fx_leg_type : FxLegType or str, optional
        The enumeration that specifies the type of the leg. Mandatory for MultiLeg,
        FwdFwdSwap, or Swap contracts. Optional for Spot and Forwards contracts.
    contra_amount : float, optional
        The unsigned amount exchanged to buy or sell the traded amount. Optional. By
        default, it is calculated from the traded rate and the deal_amount. If no traded
        rate is provided the market rate will be used.
    contra_ccy : str, optional
        The currency that is exchanged. Optional. By default, the second currency in the
        FxCrossCode.
    deal_amount : float, optional
        The unsigned amount of traded currency actually bought or sold. Optional.
        Defaults to 1,000,000'.
    deal_ccy : str, optional
        The ISO code of the traded currency (e.g. 'EUR' ). Optional. Defaults to the
        first currency of the FxCrossCode.
    start_tenor : str, optional
        The tenor representing the Starting of maturity period of the contract (e.g.
        '1Y' or '6M' ). Either the start_date or the start_tenor must be provided for
        TimeOptionForward.
    """

    def __init__(
        self,
        start_date: OptDateTime = None,
        end_date: OptDateTime = None,
        tenor: Optional[str] = None,
        leg_tag: Optional[str] = None,
        deal_ccy_buy_sell: Union[BuySell, str] = None,
        fx_leg_type: Union[FxLegType, str] = None,
        contra_amount: Optional[float] = None,
        contra_ccy: Optional[str] = None,
        deal_amount: Optional[float] = None,
        deal_ccy: Optional[str] = None,
        start_tenor: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.leg_tag = leg_tag
        self.deal_ccy_buy_sell = deal_ccy_buy_sell
        self.fx_leg_type = fx_leg_type
        self.contra_amount = contra_amount
        self.contra_ccy = contra_ccy
        self.deal_amount = deal_amount
        self.deal_ccy = deal_ccy
        self.start_tenor = start_tenor

    def _get_items(self):
        return [
            enum_param_item.to_kv("dealCcyBuySell", self.deal_ccy_buy_sell),
            enum_param_item.to_kv("fxLegType", self.fx_leg_type),
            param_item.to_kv("contraAmount", self.contra_amount),
            param_item.to_kv("contraCcy", self.contra_ccy),
            param_item.to_kv("dealAmount", self.deal_amount),
            param_item.to_kv("dealCcy", self.deal_ccy),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("legTag", self.leg_tag),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("startTenor", self.start_tenor),
            param_item.to_kv("tenor", self.tenor),
        ]
