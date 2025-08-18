from enum import unique
from ...._base_enum import StrEnum


@unique
class QuoteFallbackLogic(StrEnum):
    """
    - "None": it means that there's no fallback logic. For example, if the user asks
      for a "Ask" price and instrument is only quoted with a "Bid" price, it is an
      error case.
    - "BestField" : it means that there's a fallback logic to use another market
      data field as quoted price. For example, if the user asks for a "Ask" price
      and instrument is only quoted with a "Bid" price, "Bid" price can be used.
    """

    BEST_FIELD = "BestField"
    NONE = "None"
