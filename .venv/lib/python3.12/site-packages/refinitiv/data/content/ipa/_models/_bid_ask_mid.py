from typing import Optional

from .._param_item import param_item
from .._serializable import Serializable


class BidAskMid(Serializable):
    """
    Parameters
    ----------
    bid : float, optional

    ask : float, optional

    mid : float, optional

    """

    def __init__(
        self,
        bid: Optional[float] = None,
        ask: Optional[float] = None,
        mid: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.bid = bid
        self.ask = ask
        self.mid = mid

    def _get_items(self):
        return [
            param_item.to_kv("ask", self.ask),
            param_item.to_kv("bid", self.bid),
            param_item.to_kv("mid", self.mid),
        ]
