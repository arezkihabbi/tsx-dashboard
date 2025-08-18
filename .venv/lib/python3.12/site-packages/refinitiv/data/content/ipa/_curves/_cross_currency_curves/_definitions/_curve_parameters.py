from typing import Optional

from ._turn_adjustment import TurnAdjustment
from .._enums import InterpolationMode
from ...._enums._extrapolation_mode import ExtrapolationMode
from ...._object_definition import ObjectDefinition


class CrossCurrencyCurveParameters(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    extrapolation_mode : ExtrapolationMode, optional

    interpolation_mode : InterpolationMode, optional

    turn_adjustment : TurnAdjustment, optional

    """

    def __init__(
        self,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[InterpolationMode] = None,
        turn_adjustment: Optional[TurnAdjustment] = None,
    ) -> None:
        super().__init__()
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.turn_adjustment = turn_adjustment

    @property
    def extrapolation_mode(self):
        """
        :return: enum ExtrapolationMode
        """
        return self._get_enum_parameter(ExtrapolationMode, "extrapolationMode")

    @extrapolation_mode.setter
    def extrapolation_mode(self, value):
        self._set_enum_parameter(ExtrapolationMode, "extrapolationMode", value)

    @property
    def interpolation_mode(self):
        """
        :return: enum InterpolationMode
        """
        return self._get_enum_parameter(InterpolationMode, "interpolationMode")

    @interpolation_mode.setter
    def interpolation_mode(self, value):
        self._set_enum_parameter(InterpolationMode, "interpolationMode", value)

    @property
    def turn_adjustment(self):
        """
        :return: object TurnAdjustment
        """
        return self._get_object_parameter(TurnAdjustment, "turnAdjustment")

    @turn_adjustment.setter
    def turn_adjustment(self, value):
        self._set_object_parameter(TurnAdjustment, "turnAdjustment", value)
