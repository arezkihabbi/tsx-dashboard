from enum import unique

from ...._base_enum import StrEnum


@unique
class Format(StrEnum):
    """
    The enumerate that specifies whether the calculated volatilities
    """

    LIST = "List"
    MATRIX = "Matrix"
    N_DIMENSIONAL_ARRAY = "NDimensionalArray"
