from typing import Optional, TYPE_CHECKING

from ...._object_definition import ObjectDefinition
from ._enums import (
    ShiftType,
    ShiftUnit,
)


if TYPE_CHECKING:
    from ......_types import OptFloat


class FlatteningShift(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    amount : float, optional
        Amount of shifting, applied to points depending on shift method selected.<br/>
        can be measured in basis points/percents/future price based points.<br/> also
        can be expressed as multiplier for relative shift type.<br/>
    shift_type : ShiftType, optional
        The type of shifting. the possible values are:   * additive: the amount of
        shifting is added to the corresponding curve point,   * relative: the curve
        point is multiplied by the amount of shifting (e.g., if amount = 1, the curve
        point value will be doubled),   * relativepercent: the curve point is multiplied
        by the amount expressed in percentages (e.g., if amount = 1, the curve point
        value will multiplied by [1+1%]),   * scaled: the curve point is scaled by the
        value of the shifting amount (e.g., if amount = 1.1, the curve point value will
        multiplied by this value).
    shift_unit : ShiftUnit, optional
        The unit that describes the amount of shifting. the possible values are:   * bp:
        the amount of shifting is expressed in basis points,   * percent: the amount of
        shifting is expressed in percentages,   * absolute: the amount of shifting is
        expressed in absolute value.
    """

    def __init__(
        self,
        amount: "OptFloat" = None,
        shift_type: Optional[ShiftType] = None,
        shift_unit: Optional[ShiftUnit] = None,
    ) -> None:
        super().__init__()
        self.amount = amount
        self.shift_type = shift_type
        self.shift_unit = shift_unit

    @property
    def shift_type(self):
        """
        The type of shifting. the possible values are:   * additive: the amount of
        shifting is added to the corresponding curve point,   * relative: the curve
        point is multiplied by the amount of shifting (e.g., if amount = 1, the curve
        point value will be doubled),   * relativepercent: the curve point is multiplied
        by the amount expressed in percentages (e.g., if amount = 1, the curve point
        value will multiplied by [1+1%]),   * scaled: the curve point is scaled by the
        value of the shifting amount (e.g., if amount = 1.1, the curve point value will
        multiplied by this value).
        :return: enum ShiftType
        """
        return self._get_enum_parameter(ShiftType, "shiftType")

    @shift_type.setter
    def shift_type(self, value):
        self._set_enum_parameter(ShiftType, "shiftType", value)

    @property
    def shift_unit(self):
        """
        The unit that describes the amount of shifting. the possible values are:   * bp:
        the amount of shifting is expressed in basis points,   * percent: the amount of
        shifting is expressed in percentages,   * absolute: the amount of shifting is
        expressed in absolute value.
        :return: enum ShiftUnit
        """
        return self._get_enum_parameter(ShiftUnit, "shiftUnit")

    @shift_unit.setter
    def shift_unit(self, value):
        self._set_enum_parameter(ShiftUnit, "shiftUnit", value)

    @property
    def amount(self):
        """
        Amount of shifting, applied to points depending on shift method selected.<br/>
        can be measured in basis points/percents/future price based points.<br/> also
        can be expressed as multiplier for relative shift type.<br/>
        :return: float
        """
        return self._get_parameter("amount")

    @amount.setter
    def amount(self, value):
        self._set_parameter("amount", value)
