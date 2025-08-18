from enum import unique
from ...._base_enum import StrEnum


@unique
class ForwardComputeMethod(StrEnum):
    USE_DIVIDENDS_ONLY = "UseDividendsOnly"
    USE_FORWARD_CRV = "UseForwardCrv"
    USE_FORWARD_CRV_AND_DIVIDENDS = "UseForwardCrvAndDividends"
