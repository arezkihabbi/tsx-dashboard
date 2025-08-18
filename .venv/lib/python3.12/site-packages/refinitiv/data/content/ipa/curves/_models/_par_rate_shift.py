from typing import Optional

from ..._param_item import param_item
from ..._serializable import Serializable


class ParRateShift(Serializable):
    """
    Parameters
    ----------
    cross_currency_instruments : dict, optional
        The list of shift attributes applied to the zero coupon curve constructed from
        cross currency instrument constituents.
    interest_rate_instruments : dict, optional
        The list of shift attributes applied to curve constructed from interest rate
        instrument constituents.
    """

    def __init__(
        self,
        *,
        cross_currency_instruments: Optional[dict] = None,
        interest_rate_instruments: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.cross_currency_instruments = cross_currency_instruments
        self.interest_rate_instruments = interest_rate_instruments

    def _get_items(self):
        return [
            param_item.to_kv("crossCurrencyInstruments", self.cross_currency_instruments),
            param_item.to_kv("interestRateInstruments", self.interest_rate_instruments),
        ]
