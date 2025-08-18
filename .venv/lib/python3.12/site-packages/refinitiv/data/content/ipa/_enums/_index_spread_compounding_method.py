from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexSpreadCompoundingMethod(StrEnum):
    ISDA_COMPOUNDING = "IsdaCompounding"
    ISDA_FLAT_COMPOUNDING = "IsdaFlatCompounding"
    NO_COMPOUNDING = "NoCompounding"
