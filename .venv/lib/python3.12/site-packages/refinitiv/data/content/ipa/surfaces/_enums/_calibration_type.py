from enum import unique

from ....._base_enum import StrEnum


@unique
class CalibrationType(StrEnum):
    ALTERNATE_CONJUGATE_GRADIENT = "AlternateConjugateGradient"
    CONJUGATE_GRADIENT = "ConjugateGradient"
    POWELL = "Powell"
    SIMPLEX_NELDER_MEAD = "SimplexNelderMead"
