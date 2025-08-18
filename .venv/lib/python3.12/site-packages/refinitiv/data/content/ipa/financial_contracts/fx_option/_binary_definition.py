from typing import Optional, Union

from ..._enums import FxBinaryType
from ..._param_item import param_item, enum_param_item
from ..._serializable import Serializable


class FxBinaryDefinition(Serializable):
    """
    Parameters
    ----------
    binary_type : FxBinaryType or str, optional
        The type of a binary option.
    payout_amount : float, optional
        The payout amount of the option. the default value is '1,000,000'.
    payout_ccy : str, optional
        The trade currency, which is either a domestic or foreign currency. either
        payoutccy or settlementtype can be used at a time. payoutccy="foreign currency"
        is equivalent to settlementtype ="physical", and payoutccy="domestic currency"
        is equivalent to settlementtype ="cash". the value is expressed in iso 4217
        alphabetical format (e.g. 'usd').
    trigger : float, optional
        The trigger of the binary option.
    """

    def __init__(
        self,
        binary_type: Union[FxBinaryType, str] = None,
        payout_amount: Optional[float] = None,
        payout_ccy: Optional[str] = None,
        trigger: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.binary_type = binary_type
        self.payout_amount = payout_amount
        self.payout_ccy = payout_ccy
        self.trigger = trigger

    def _get_items(self):
        return [
            enum_param_item.to_kv("binaryType", self.binary_type),
            param_item.to_kv("payoutAmount", self.payout_amount),
            param_item.to_kv("payoutCcy", self.payout_ccy),
            param_item.to_kv("trigger", self.trigger),
        ]
