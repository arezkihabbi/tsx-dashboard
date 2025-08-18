from enum import unique
from ...._base_enum import StrEnum


@unique
class Method(StrEnum):
    AMERICAN_MONTE_CARLO = "AmericanMonteCarlo"
    ANALYTIC = "Analytic"
    MONTE_CARLO = "MonteCarlo"
    PDE = "PDE"
    TREE = "Tree"
