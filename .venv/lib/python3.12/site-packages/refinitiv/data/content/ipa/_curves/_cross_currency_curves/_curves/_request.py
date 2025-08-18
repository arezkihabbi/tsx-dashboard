from typing import TYPE_CHECKING, Optional

from ._fx_forward_constituents import FxForwardConstituents
from ._fx_forward_curve_definition import FxForwardCurveDefinition
from ._fx_forward_curve_parameters import FxForwardCurveParameters
from ._fx_shift_scenario import FxShiftScenario
from ...._object_definition import ObjectDefinition
from ......_tools import try_copy_to_list

if TYPE_CHECKING:
    from ......_types import OptStr
    from ._types import CurveDefinition, CurveParameters, ShiftScenarios


class RequestItem(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------

    constituents : FxForwardConstituents, optional

    curve_definition : FxForwardCurveDefinition, optional

    curve_parameters : FxForwardCurveParameters, optional

    shift_scenarios : list of FxShiftScenario, optional
        The list of attributes applied to the curve shift scenarios.
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    """

    def __init__(
        self,
        constituents: Optional[FxForwardConstituents] = None,
        curve_definition: "CurveDefinition" = None,
        curve_parameters: "CurveParameters" = None,
        shift_scenarios: "ShiftScenarios" = None,
        curve_tag: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.constituents = constituents
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.shift_scenarios = try_copy_to_list(shift_scenarios)
        self.curve_tag = curve_tag

    @property
    def constituents(self):
        """
        :return: object FxForwardConstituents
        """
        return self._get_object_parameter(FxForwardConstituents, "constituents")

    @constituents.setter
    def constituents(self, value):
        self._set_object_parameter(FxForwardConstituents, "constituents", value)

    @property
    def curve_definition(self):
        """
        :return: object FxForwardCurveDefinition
        """
        return self._get_object_parameter(FxForwardCurveDefinition, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(FxForwardCurveDefinition, "curveDefinition", value)

    @property
    def curve_parameters(self):
        """
        :return: object FxForwardCurveParameters
        """
        return self._get_object_parameter(FxForwardCurveParameters, "curveParameters")

    @curve_parameters.setter
    def curve_parameters(self, value):
        self._set_object_parameter(FxForwardCurveParameters, "curveParameters", value)

    @property
    def shift_scenarios(self):
        """
        The list of attributes applied to the curve shift scenarios.
        :return: list FxShiftScenario
        """
        return self._get_list_parameter(FxShiftScenario, "shiftScenarios")

    @shift_scenarios.setter
    def shift_scenarios(self, value):
        self._set_list_parameter(FxShiftScenario, "shiftScenarios", value)

    @property
    def curve_tag(self):
        """
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
        :return: str
        """
        return self._get_parameter("curveTag")

    @curve_tag.setter
    def curve_tag(self, value):
        self._set_parameter("curveTag", value)
