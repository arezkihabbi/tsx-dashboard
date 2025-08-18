from typing import Optional, TYPE_CHECKING

from ...._object_definition import ObjectDefinition
from ._enums import (
    ShiftType,
    ShiftUnit,
)


if TYPE_CHECKING:
    from ......_types import OptStr, OptFloat


class CombinedShift(ObjectDefinition):
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
    end_tenor : str, optional
        The code indicating the end tenor from which the combined shifts scenario is
        applied to curve points. when starttenor equals endtenor:   * shift equals 0 for
        tenor less than starttenor,   * shift equals amount for tenor is equal and
        greater than endtenor. when starttenor less than endtenor:   * shift equals 0
        for tenor which is less or equal starttenor,   * shift rises from 0 to amount in
        period from starttenor to endtenor. shift equals amount for tenor greater than
        endtenor.
    start_tenor : str, optional
        The code indicating the start tenor from which the combined shifts scenario is
        applied to curve points. when starttenor equals endtenor:   * shift equals 0 for
        tenor less than starttenor,   * shift equals amount for tenor is equal and
        greater than endtenor. when starttenor less than endtenor:   * shift equals 0
        for tenor which is less or equal starttenor,   * shift rises from 0 to amount in
        period from starttenor to endtenor. shift equals amount for tenor greater than
        endtenor.
    """

    def __init__(
        self,
        amount: "OptFloat" = None,
        shift_type: Optional[ShiftType] = None,
        shift_unit: Optional[ShiftUnit] = None,
        end_tenor: "OptStr" = None,
        start_tenor: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.amount = amount
        self.shift_type = shift_type
        self.shift_unit = shift_unit
        self.end_tenor = end_tenor
        self.start_tenor = start_tenor

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

    @property
    def end_tenor(self):
        """
        The code indicating the end tenor from which the combined shifts scenario is
        applied to curve points. when starttenor equals endtenor:   * shift equals 0 for
        tenor less than starttenor,   * shift equals amount for tenor is equal and
        greater than endtenor. when starttenor less than endtenor:   * shift equals 0
        for tenor which is less or equal starttenor,   * shift rises from 0 to amount in
        period from starttenor to endtenor. shift equals amount for tenor greater than
        endtenor.
        :return: str
        """
        return self._get_parameter("endTenor")

    @end_tenor.setter
    def end_tenor(self, value):
        self._set_parameter("endTenor", value)

    @property
    def start_tenor(self):
        """
        The code indicating the start tenor from which the combined shifts scenario is
        applied to curve points. when starttenor equals endtenor:   * shift equals 0 for
        tenor less than starttenor,   * shift equals amount for tenor is equal and
        greater than endtenor. when starttenor less than endtenor:   * shift equals 0
        for tenor which is less or equal starttenor,   * shift rises from 0 to amount in
        period from starttenor to endtenor. shift equals amount for tenor greater than
        endtenor.
        :return: str
        """
        return self._get_parameter("startTenor")

    @start_tenor.setter
    def start_tenor(self, value):
        self._set_parameter("startTenor", value)
