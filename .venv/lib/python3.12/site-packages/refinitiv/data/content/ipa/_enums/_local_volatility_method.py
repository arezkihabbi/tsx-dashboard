from enum import unique
from ...._base_enum import StrEnum


@unique
class LocalVolatilityMethod(StrEnum):
    BEST_SMILE = "BestSmile"
    CONVEX_SMILE = "ConvexSmile"
    PARABOLA_SMOOTH = "ParabolaSmooth"
    PARABOLA_WITHOUT_EXTRAPOL = "ParabolaWithoutExtrapol"
    RATIONAL_SMOOTH = "RationalSmooth"
    RATIONAL_WITHOUT_EXTRAPOL = "RationalWithoutExtrapol"
