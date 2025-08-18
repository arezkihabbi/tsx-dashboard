from enum import unique

from ...._base_enum import StrEnum


@unique
class IndexConvexityAdjustmentIntegrationMethod(StrEnum):
    RIEMANN_SUM = "RiemannSum"
    RUNGE_KUTTA = "RungeKutta"
