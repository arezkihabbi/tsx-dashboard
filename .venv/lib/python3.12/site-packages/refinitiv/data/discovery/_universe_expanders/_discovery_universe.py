from typing import TYPE_CHECKING

from ._universe_expander import UniverseExpander
from ..._core.session import get_default
from ..._tools import cached_property
from ...content._get_adc_data import get_adc_data

if TYPE_CHECKING:
    pass


def update_universe(raw, _universe):
    index = 0  # instrument
    data = raw.get("data")
    if data and all(isinstance(i[index], str) for i in data):
        universe = [i[index] for i in data]
    else:
        universe = _universe
    return universe


def get_universe(expression):
    session = get_default()
    logger = session.logger()
    adc_data = get_adc_data(
        params={
            "universe": expression,
            "fields": "TR.RIC",
        },
        logger=logger,
    )
    adc_raw = adc_data.raw
    return update_universe(
        adc_raw,
        None,
    )


class DiscoveryUniverse(UniverseExpander):
    def __init__(self, expression):
        self._expression = expression

    @property
    def expression(self):
        return self._expression

    @cached_property
    def _universe(self):
        universe = get_universe(self._expression)
        if not universe:
            universe = []

        return universe
