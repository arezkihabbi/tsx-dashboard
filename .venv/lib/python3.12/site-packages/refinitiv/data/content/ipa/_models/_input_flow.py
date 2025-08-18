from typing import Optional

from .._enums import PremiumSettlementType
from .._param_item import enum_param_item, param_item, datetime_param_item
from .._serializable import Serializable
from ...._types import OptDateTime


class InputFlow(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    amount : float, optional

    premium_settlement_type : PremiumSettlementType, optional
        The cash settlement type of the option premium -spot -forward
    currency : str, optional

    date : str or date or datetime or timedelta, optional

    """

    def __init__(
        self,
        amount: Optional[float] = None,
        premium_settlement_type: Optional[PremiumSettlementType] = None,
        currency: Optional[str] = None,
        date: OptDateTime = None,
    ) -> None:
        super().__init__()
        self.amount = amount
        self.premium_settlement_type = premium_settlement_type
        self.currency = currency
        self.date = date

    def _get_items(self):
        return [
            enum_param_item.to_kv("premiumSettlementType", self.premium_settlement_type),
            param_item.to_kv("amount", self.amount),
            param_item.to_kv("currency", self.currency),
            datetime_param_item.to_kv("date", self.date),
        ]
