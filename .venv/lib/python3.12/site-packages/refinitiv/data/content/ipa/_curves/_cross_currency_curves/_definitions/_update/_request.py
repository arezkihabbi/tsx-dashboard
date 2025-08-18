from typing import TYPE_CHECKING

from ......._tools import try_copy_to_list
from .._mixin_request import MixinRequest
from ._curve_update_definition import CrossCurrencyCurveUpdateDefinition


if TYPE_CHECKING:
    from .._types import CurveUpdateDefinition, OptOverrides, Segments, OptTurns


class UpdateRequest(MixinRequest):
    """
    Update an existing cross currency curve request

    Parameters
    ----------
    curve_definition : CrossCurrencyCurveUpdateDefinition, optional

    overrides : list of OverrideBidAsk, optional

    segments : list of CrossCurrencyInstrumentsSegment

    turns : list of OverrideFxForwardTurn, optional

    """

    def __init__(
        self,
        curve_definition: "CurveUpdateDefinition" = None,
        overrides: "OptOverrides" = None,
        segments: "Segments" = None,
        turns: "OptTurns" = None,
    ) -> None:
        super().__init__()
        self.curve_definition = curve_definition
        self.overrides = try_copy_to_list(overrides)
        self.segments = try_copy_to_list(segments)
        self.turns = try_copy_to_list(turns)

    @property
    def curve_definition(self):
        """
        :return: object CrossCurrencyCurveUpdateDefinition
        """
        return self._get_object_parameter(CrossCurrencyCurveUpdateDefinition, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(CrossCurrencyCurveUpdateDefinition, "curveDefinition", value)
