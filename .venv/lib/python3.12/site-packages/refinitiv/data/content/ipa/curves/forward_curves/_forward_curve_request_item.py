from typing import TYPE_CHECKING, Any, Union, Iterable

from ..._param_item import param_item, serializable_param_item, list_serializable_param_item
from ..._serializable import Serializable
from ....._tools import ArgsParser

if TYPE_CHECKING:
    from .._models import ShiftScenario
    from ._forward_curve_definition import ForwardCurveDefinition
    from ._swap_zc_curve_definition import SwapZcCurveDefinition
    from ._swap_zc_curve_parameters import SwapZcCurveParameters
    from ....._types import OptStr


def parse_objects(param: object) -> Union[list, Any]:
    if not param:
        return param

    if not isinstance(param, list):
        param = [param]

    return param


object_arg_parser = ArgsParser(parse_objects)


class ForwardCurveRequestItem(Serializable):
    def __init__(
        self,
        curve_definition: "SwapZcCurveDefinition" = None,
        forward_curve_definitions: Union["ForwardCurveDefinition", Iterable["ForwardCurveDefinition"]] = None,
        curve_parameters: "SwapZcCurveParameters" = None,
        curve_tag: "OptStr" = None,
        shift_scenarios: Union["ShiftScenario", Iterable["ShiftScenario"]] = None,
    ) -> None:
        super().__init__()
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.forward_curve_definitions = object_arg_parser.parse(forward_curve_definitions)
        self.curve_tag = curve_tag
        self.shift_scenarios = object_arg_parser.parse(shift_scenarios)

    def _get_items(self):
        return [
            serializable_param_item.to_kv("curveDefinition", self.curve_definition),
            serializable_param_item.to_kv("curveParameters", self.curve_parameters),
            list_serializable_param_item.to_kv("forwardCurveDefinitions", self.forward_curve_definitions),
            param_item.to_kv("curveTag", self.curve_tag),
            list_serializable_param_item.to_kv("shiftScenarios", self.shift_scenarios),
        ]
