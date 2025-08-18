from enum import unique
from typing import Union, List, Optional

from ..._tools import make_enum_arg_parser
from ..._base_enum import StrEnum

# --------------------------------------------------------------------------------------
#   EventTypes
# --------------------------------------------------------------------------------------


@unique
class EventTypes(StrEnum):
    """The list of market events, supported event types are trade, quote and correction."""

    TRADE = "trade"
    QUOTE = "quote"
    CORRECTION = "correction"


OptEventTypes = Optional[Union[str, List[str], EventTypes, List[EventTypes]]]
event_types_arg_parser = make_enum_arg_parser(EventTypes)


# --------------------------------------------------------------------------------------
#   Adjustments
# --------------------------------------------------------------------------------------


@unique
class Adjustments(StrEnum):
    """
    The list of adjustment types (comma delimiter) that tells the system whether
     to apply or not apply CORAX (Corporate Actions) events or
     exchange/manual corrections to historical time series data.

     The supported values of adjustments :

        UNADJUSTED - Not apply both exchange/manual corrections and CORAX
        EXCHANGE_CORRECTION - Apply exchange correction adjustment to historical pricing
        MANUAL_CORRECTION - Apply manual correction adjustment to historical pricing
                            i.e. annotations made by content analysts
        CCH - Apply Capital Change adjustment to historical Pricing due
              to Corporate Actions e.g. stock split
        CRE - Apply Currency Redenomination adjustment
              when there is redenomination of currency
        RPO - Apply Reuters Price Only adjustment
              to adjust historical price only not volume
        RTS - Apply Reuters TimeSeries adjustment
              to adjust both historical price and volume
        QUALIFIERS - Apply price or volume adjustment
              to historical pricing according to trade/quote qualifier
              summarization actions
    """

    UNADJUSTED = "unadjusted"
    EXCHANGE_CORRECTION = "exchangeCorrection"
    MANUAL_CORRECTION = "manualCorrection"
    CCH = "CCH"
    CRE = "CRE"
    RPO = "RPO"
    RTS = "RTS"
    QUALIFIERS = "qualifiers"


OptAdjustments = Optional[Union[str, List[str], Adjustments, List[Adjustments]]]
adjustments_arg_parser = make_enum_arg_parser(Adjustments)


# --------------------------------------------------------------------------------------
#   MarketSession
# --------------------------------------------------------------------------------------


@unique
class MarketSession(StrEnum):
    """
    The Market Session represents a list of interested official durations in which trade and quote activities occur
    for a particular instrument.
    """

    PRE = "pre"
    NORMAL = "normal"
    POST = "post"


OptMarketSession = Optional[Union[str, List[str], MarketSession, List[MarketSession]]]
market_sessions_arg_parser = make_enum_arg_parser(MarketSession)
