from enum import unique
from ...._base_enum import StrEnum


@unique
class NumeraireType(StrEnum):
    CASH = "Cash"
    ROLLING_EVENT = "RollingEvent"
    ROLLING_PAYMENT = "RollingPayment"
    TERMINAL_EVENT_ZC = "TerminalEventZc"
    TERMINAL_ZC = "TerminalZc"
