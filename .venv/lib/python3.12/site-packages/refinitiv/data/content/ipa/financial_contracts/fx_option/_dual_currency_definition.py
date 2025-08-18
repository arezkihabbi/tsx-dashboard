from typing import Optional

from ..._param_item import param_item, datetime_param_item
from ..._serializable import Serializable


class FxDualCurrencyDefinition(Serializable):
    """
    Parameters
    ----------
    deposit_start_date : str or date or datetime or timedelta, optional
        Deposit Start Date for the DualCurrencyDeposit option
    margin_percent : float, optional
        Margin for the DualCurrencyDeposit option
    """

    def __init__(
        self,
        deposit_start_date: "OptDateTime" = None,
        margin_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.deposit_start_date = deposit_start_date
        self.margin_percent = margin_percent

    def _get_items(self):
        return [
            datetime_param_item.to_kv("depositStartDate", self.deposit_start_date),
            param_item.to_kv("marginPercent", self.margin_percent),
        ]
