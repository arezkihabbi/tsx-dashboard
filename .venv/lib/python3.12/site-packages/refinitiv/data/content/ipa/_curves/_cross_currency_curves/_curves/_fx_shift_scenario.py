from typing import Optional, TYPE_CHECKING

from ._shift_definition import ShiftDefinition
from ...._object_definition import ObjectDefinition
from ....curves._models import ParRateShift

if TYPE_CHECKING:
    from ......_types import OptStr


class FxShiftScenario(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    fx_curve_shift : ShiftDefinition, optional
        Collection of shift parameters tenor. "all" selector supported as well.
    par_rate_shift : ParRateShift, optional
        Scenario of par rates shift (shift applied to constituents).
    shift_tag : str, optional
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    """

    def __init__(
        self,
        fx_curve_shift: Optional[ShiftDefinition] = None,
        par_rate_shift: Optional[ParRateShift] = None,
        shift_tag: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.fx_curve_shift = fx_curve_shift
        self.par_rate_shift = par_rate_shift
        self.shift_tag = shift_tag

    @property
    def fx_curve_shift(self):
        """
        Collection of shift parameters tenor. "all" selector supported as well.
        :return: object ShiftDefinition
        """
        return self._get_object_parameter(ShiftDefinition, "fxCurveShift")

    @fx_curve_shift.setter
    def fx_curve_shift(self, value):
        self._set_object_parameter(ShiftDefinition, "fxCurveShift", value)

    @property
    def par_rate_shift(self):
        """
        Scenario of par rates shift (shift applied to constituents).
        :return: object ParRateShift
        """
        return self._get_object_parameter(ParRateShift, "parRateShift")

    @par_rate_shift.setter
    def par_rate_shift(self, value):
        self._set_object_parameter(ParRateShift, "parRateShift", value)

    @property
    def shift_tag(self):
        """
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
        :return: str
        """
        return self._get_parameter("shiftTag")

    @shift_tag.setter
    def shift_tag(self, value):
        self._set_parameter("shiftTag", value)
