from enum import unique

from ...._base_enum import StrEnum


@unique
class BuySell(StrEnum):
    """
    - Buy: buying the option,
    - Sell: selling/writing the option. the output amounts calculated with taking
      buysell into consideration are returned with a reversed sign when the value
      'sell' is used. optional. the default value is 'buy'.
    """

    BUY = "Buy"
    SELL = "Sell"
