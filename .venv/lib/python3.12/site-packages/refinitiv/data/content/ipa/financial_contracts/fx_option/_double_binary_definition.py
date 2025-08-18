from typing import Optional, Union

from ..._enums import DoubleBinaryType
from ..._param_item import param_item, enum_param_item
from ..._serializable import Serializable


class FxDoubleBinaryDefinition(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    double_binary_type : DoubleBinaryType or str, optional
        The type of a double binary option.
    payout_amount : float, optional
        The payout amount of the option. the default value is '1,000,000'.
    payout_ccy : str, optional
        The trade currency, which is either a domestic or foreign currency. either
        payoutccy or settlementtype can be used at a time. payoutccy="foreign currency"
        is equivalent to settlementtype ="physical", and payoutccy="domestic currency"
        is equivalent to settlementtype ="cash". the value is expressed in iso 4217
        alphabetical format (e.g. 'usd').
    trigger_down : float, optional
        The lower trigger of the binary option.
    trigger_up : float, optional
        The upper trigger of the binary option.
    """

    def __init__(
        self,
        double_binary_type: Union[DoubleBinaryType, str] = None,
        payout_amount: Optional[float] = None,
        payout_ccy: Optional[str] = None,
        trigger_down: Optional[float] = None,
        trigger_up: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.double_binary_type = double_binary_type
        self.payout_amount = payout_amount
        self.payout_ccy = payout_ccy
        self.trigger_down = trigger_down
        self.trigger_up = trigger_up

    def _get_items(self):
        return [
            enum_param_item.to_kv("doubleBinaryType", self.double_binary_type),
            param_item.to_kv("payoutAmount", self.payout_amount),
            param_item.to_kv("payoutCcy", self.payout_ccy),
            param_item.to_kv("triggerDown", self.trigger_down),
            param_item.to_kv("triggerUp", self.trigger_up),
        ]
