from typing import Optional

from ...._object_definition import ObjectDefinition


class CreditConstituents(ObjectDefinition):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    credit_instruments : dict, optional

    cross_currency_instruments : dict, optional

    """

    def __init__(
        self,
        *,
        credit_instruments: Optional[dict] = None,
        cross_currency_instruments: Optional[dict] = None,
    ) -> None:
        super().__init__()
        self.credit_instruments = credit_instruments
        self.cross_currency_instruments = cross_currency_instruments

    @property
    def credit_instruments(self):
        """
        :return: dict
        """
        return self._get_parameter("creditInstruments")

    @credit_instruments.setter
    def credit_instruments(self, value):
        self._set_parameter("creditInstruments", value)

    @property
    def cross_currency_instruments(self):
        """
        :return: dict
        """
        return self._get_parameter("crossCurrencyInstruments")

    @cross_currency_instruments.setter
    def cross_currency_instruments(self, value):
        self._set_parameter("crossCurrencyInstruments", value)
