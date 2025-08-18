from enum import unique

from ...._base_enum import StrEnum


@unique
class FxSwapCalculationMethod(StrEnum):
    """
    - FxSwapImpliedFromDeposit: implied FX swap points are computed from deposit rates,
    - DepositCcy1ImpliedFromFxSwap: Currency 1 deposit rates are computed using swap points,
    - DepositCcy2ImpliedFromFxSwap: Currency 2 deposit rates are computed using swap points.
    """

    FX_SWAP = "FxSwap"
    FX_SWAP_IMPLIED_FROM_DEPOSIT = "FxSwapImpliedFromDeposit"
    DEPOSIT_CCY1_IMPLIED_FROM_FX_SWAP = "DepositCcy1ImpliedFromFxSwap"
    DEPOSIT_CCY2_IMPLIED_FROM_FX_SWAP = "DepositCcy2ImpliedFromFxSwap"
