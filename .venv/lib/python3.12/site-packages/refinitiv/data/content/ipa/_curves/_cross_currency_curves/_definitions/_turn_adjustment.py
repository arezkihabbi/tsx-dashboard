from typing import Optional

from ...._object_definition import ObjectDefinition
from ._enums import StandardTurnPeriod


class TurnAdjustment(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    standard_turn_period : StandardTurnPeriod, optional

    """

    def __init__(
        self,
        standard_turn_period: Optional[StandardTurnPeriod] = None,
    ) -> None:
        super().__init__()
        self.standard_turn_period = standard_turn_period

    @property
    def standard_turn_period(self):
        """
        :return: enum StandardTurnPeriod
        """
        return self._get_enum_parameter(StandardTurnPeriod, "standardTurnPeriod")

    @standard_turn_period.setter
    def standard_turn_period(self, value):
        self._set_enum_parameter(StandardTurnPeriod, "standardTurnPeriod", value)
