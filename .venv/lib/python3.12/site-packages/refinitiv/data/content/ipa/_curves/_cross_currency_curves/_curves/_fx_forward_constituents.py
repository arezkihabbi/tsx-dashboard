from typing import Optional
from ...._object_definition import ObjectDefinition


class FxForwardConstituents(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    cross_currency_instruments : dict, optional

    interest_rate_instruments : dict, optional

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

    @property
    def cross_currency_instruments(self):
        """
        :return: dict
        """
        return self._get_parameter("crossCurrencyInstruments")

    @cross_currency_instruments.setter
    def cross_currency_instruments(self, value):
        self._set_parameter("crossCurrencyInstruments", value)

    @property
    def interest_rate_instruments(self):
        """
        :return: dict
        """
        return self._get_parameter("interestRateInstruments")

    @interest_rate_instruments.setter
    def interest_rate_instruments(self, value):
        self._set_parameter("interestRateInstruments", value)
