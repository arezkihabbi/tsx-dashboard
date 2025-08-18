from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr, OptBool


class EtiSurfaceDefinition(Serializable):
    """
    The definition of the volatility surface.

    Parameters
    ----------
    instrument_code : str, optional
        The code (ric for equities and indices and ricroot for futures.) that represents
        the instrument. the format for equities and indices is xxx@ric (example:
        vod.l@ric) the format for futures is xx@ricroot (example: cl@ricroot)
    clean_instrument_code : str, optional
    exchange : str, optional
        Specifies the exchange to be used to retrieve the underlying data.
    is_future_underlying : bool, optional
    is_lme_future_underlying : bool, optional
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        clean_instrument_code: "OptStr" = None,
        exchange: "OptStr" = None,
        is_future_underlying: "OptBool" = None,
        is_lme_future_underlying: "OptBool" = None,
    ):
        super().__init__()
        self.instrument_code = instrument_code
        self.clean_instrument_code = clean_instrument_code
        self.exchange = exchange
        self.is_future_underlying = is_future_underlying
        self.is_lme_future_underlying = is_lme_future_underlying

    def _get_items(self):
        return [
            param_item.to_kv("cleanInstrumentCode", self.clean_instrument_code),
            param_item.to_kv("exchange", self.exchange),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("isFutureUnderlying", self.is_future_underlying),
            param_item.to_kv("isLmeFutureUnderlying", self.is_lme_future_underlying),
        ]
