from enum import unique
from ...._base_enum import StrEnum


@unique
class CallPut(StrEnum):
    """
    - CALL: the right to buy the underlying asset,
    - PUT: the right to sell the underlying asset. optional. if instrumentcode of
      listed eti option is defined, the value comes from the instrument reference
      data.
    """

    CALL = "CALL"
    NONE = "None"
    PUT = "PUT"
