from typing import Optional, List

from ._fx_forward_curve_definition import FxForwardCurveDefinition
from ._fx_forward_curve_parameters import FxForwardCurveParameters
from ._fx_shift_scenario import FxShiftScenario
from ._fx_forward_constituents import FxForwardConstituents


CurveDefinition = Optional[FxForwardCurveDefinition]
CurveParameters = Optional[FxForwardCurveParameters]
ShiftScenarios = Optional[List[FxShiftScenario]]
FxConstituents = Optional[FxForwardConstituents]
