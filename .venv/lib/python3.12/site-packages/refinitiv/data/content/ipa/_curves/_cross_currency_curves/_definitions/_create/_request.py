from typing import TYPE_CHECKING

from ._curve_definition_description import (
    CrossCurrencyCurveCreateDefinition,
)
from .._mixin_request import MixinRequest
from ......._tools import try_copy_to_list

if TYPE_CHECKING:
    from .._types import CurveCreateDefinition, OptOverrides, Segments, OptTurns


class CreateRequest(MixinRequest):
    """
    Create a cross currency curve request

    Parameters
    ----------
    curve_definition : CrossCurrencyCurveCreateDefinition

    overrides : list of OverrideBidAsk, optional

    segments : list of CrossCurrencyInstrumentsSegment

    turns : list of OverrideFxForwardTurn, optional

    """

    def __init__(
        self,
        curve_definition: "CurveCreateDefinition" = None,
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
        :return: object CrossCurrencyCurveDefinitionDescription
        """
        return self._get_object_parameter(CrossCurrencyCurveCreateDefinition, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(CrossCurrencyCurveCreateDefinition, "curveDefinition", value)
