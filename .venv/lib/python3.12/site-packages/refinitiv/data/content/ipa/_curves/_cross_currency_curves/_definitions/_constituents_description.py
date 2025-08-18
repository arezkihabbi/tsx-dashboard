from typing import Optional, List

from ......_tools import try_copy_to_list
from ._instrument_description import CrossCurrencyInstrumentDescription
from ._fx_forward_instrument_description import FxForwardInstrumentDescription
from ._fx_spot_instrument_description import FxSpotInstrumentDescription
from ...._object_definition import ObjectDefinition


class CrossCurrencyConstituentsDescription(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    cross_currency_swaps : list of CrossCurrencyInstrumentDescription, optional

    fx_forwards : list of FxForwardInstrumentDescription, optional

    fx_spot :  FxSpotInstrumentDescription, optional

    interest_rate_swaps : list of CrossCurrencyInstrumentDescription, optional

    overnight_index_swaps : list of CrossCurrencyInstrumentDescription, optional

    """

    def __init__(
        self,
        cross_currency_swaps: Optional[List[CrossCurrencyInstrumentDescription]] = None,
        fx_forwards: Optional[List[FxForwardInstrumentDescription]] = None,
        fx_spot: Optional[FxSpotInstrumentDescription] = None,
        interest_rate_swaps: Optional[List[CrossCurrencyInstrumentDescription]] = None,
        overnight_index_swaps: Optional[List[CrossCurrencyInstrumentDescription]] = None,
    ) -> None:
        super().__init__()
        self.cross_currency_swaps = try_copy_to_list(cross_currency_swaps)
        self.fx_forwards = try_copy_to_list(fx_forwards)
        self.fx_spot = fx_spot
        self.interest_rate_swaps = try_copy_to_list(interest_rate_swaps)
        self.overnight_index_swaps = try_copy_to_list(overnight_index_swaps)

    @property
    def cross_currency_swaps(self):
        """
        :return: list CrossCurrencyInstrumentDescription
        """
        return self._get_list_parameter(CrossCurrencyInstrumentDescription, "crossCurrencySwaps")

    @cross_currency_swaps.setter
    def cross_currency_swaps(self, value):
        self._set_list_parameter(CrossCurrencyInstrumentDescription, "crossCurrencySwaps", value)

    @property
    def fx_forwards(self):
        """
        :return: list FxForwardInstrumentDescription
        """
        return self._get_list_parameter(FxForwardInstrumentDescription, "fxForwards")

    @fx_forwards.setter
    def fx_forwards(self, value):
        self._set_list_parameter(FxForwardInstrumentDescription, "fxForwards", value)

    @property
    def fx_spot(self):
        """
        :return: object FxSpotInstrumentDescription
        """
        return self._get_object_parameter(FxSpotInstrumentDescription, "fxSpot")

    @fx_spot.setter
    def fx_spot(self, value):
        self._set_object_parameter(FxSpotInstrumentDescription, "fxSpot", value)

    @property
    def interest_rate_swaps(self):
        """
        :return: list CrossCurrencyInstrumentDescription
        """
        return self._get_list_parameter(CrossCurrencyInstrumentDescription, "interestRateSwaps")

    @interest_rate_swaps.setter
    def interest_rate_swaps(self, value):
        self._set_list_parameter(CrossCurrencyInstrumentDescription, "interestRateSwaps", value)

    @property
    def overnight_index_swaps(self):
        """
        :return: list CrossCurrencyInstrumentDescription
        """
        return self._get_list_parameter(CrossCurrencyInstrumentDescription, "overnightIndexSwaps")

    @overnight_index_swaps.setter
    def overnight_index_swaps(self, value):
        self._set_list_parameter(CrossCurrencyInstrumentDescription, "overnightIndexSwaps", value)
