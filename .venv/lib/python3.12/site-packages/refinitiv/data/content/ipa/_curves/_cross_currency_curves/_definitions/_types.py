from typing import Optional, List

from ._create._curve_definition_description import (
    CrossCurrencyCurveCreateDefinition,
)
from ._instruments_segment import CrossCurrencyInstrumentsSegment
from ._override_bid_ask import OverrideBidAsk
from ._override_fx_forward_turn import OverrideFxForwardTurn
from ._update._curve_update_definition import (
    CrossCurrencyCurveUpdateDefinition,
)


CurveCreateDefinition = CrossCurrencyCurveCreateDefinition
CurveUpdateDefinition = CrossCurrencyCurveUpdateDefinition
OptOverrides = Optional[List[OverrideBidAsk]]
Segments = List[CrossCurrencyInstrumentsSegment]
OptTurns = Optional[List[OverrideFxForwardTurn]]
