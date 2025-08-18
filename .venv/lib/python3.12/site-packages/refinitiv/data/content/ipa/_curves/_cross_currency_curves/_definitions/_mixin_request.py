from ._instruments_segment import CrossCurrencyInstrumentsSegment
from ._override_bid_ask import OverrideBidAsk
from ._override_fx_forward_turn import OverrideFxForwardTurn
from ...._object_definition import ObjectDefinition


class MixinRequest(ObjectDefinition):
    @property
    def overrides(self):
        """
        :return: list OverrideBidAsk
        """
        return self._get_list_parameter(OverrideBidAsk, "overrides")

    @overrides.setter
    def overrides(self, value):
        self._set_list_parameter(OverrideBidAsk, "overrides", value)

    @property
    def segments(self):
        """
        :return: list CrossCurrencyInstrumentsSegment
        """
        return self._get_list_parameter(CrossCurrencyInstrumentsSegment, "segments")

    @segments.setter
    def segments(self, value):
        self._set_list_parameter(CrossCurrencyInstrumentsSegment, "segments", value)

    @property
    def turns(self):
        """
        :return: list OverrideFxForwardTurn
        """
        return self._get_list_parameter(OverrideFxForwardTurn, "turns")

    @turns.setter
    def turns(self, value):
        self._set_list_parameter(OverrideFxForwardTurn, "turns", value)
