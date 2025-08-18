from typing import TYPE_CHECKING, Iterable, Union

from ..._param_item import param_item, serializable_param_item, list_serializable_param_item
from ..._serializable import Serializable
from ....._tools import try_copy_to_list

if TYPE_CHECKING:
    from ..zc_curves._zc_curve_definitions import ZcCurveDefinitions
    from .._models import Constituents, ShiftScenario
    from ._zc_curve_parameters import ZcCurveParameters
    from ....._types import OptStr


class ZcCurveRequestItem(Serializable):
    def __init__(
        self,
        constituents: "Constituents" = None,
        curve_definition: "ZcCurveDefinitions" = None,
        curve_parameters: "ZcCurveParameters" = None,
        curve_tag: "OptStr" = None,
        shift_scenarios: Union["ShiftScenario", Iterable["ShiftScenario"]] = None,
    ) -> None:
        super().__init__()
        self.constituents = constituents
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.curve_tag = curve_tag
        self.shift_scenarios = try_copy_to_list(shift_scenarios)

    def _get_items(self):
        return [
            serializable_param_item.to_kv("constituents", self.constituents),
            serializable_param_item.to_kv("curveDefinition", self.curve_definition),
            serializable_param_item.to_kv("curveParameters", self.curve_parameters),
            param_item.to_kv("curveTag", self.curve_tag),
            list_serializable_param_item.to_kv("shiftScenarios", self.shift_scenarios),
        ]
