from typing import Optional, Union

from .._enums import AmortizationType, AmortizationFrequency
from .._param_item import param_item, enum_param_item, datetime_param_item
from .._serializable import Serializable
from ...._types import OptDateTime


class AmortizationItem(Serializable):
    """
    Parameters
    ----------
    start_date : str or date or datetime or timedelta, optional
        Start Date of an amortization section/window, or stepped rate
    end_date : str or date or datetime or timedelta, optional
        End Date of an amortization section/window, or stepped rate
    amortization_frequency : AmortizationFrequency, optional
        Frequency of the Amortization
    amortization_type : AmortizationType or str, optional
        Amortization type Annuity, Schedule, Linear, ....
    remaining_notional : float, optional
        The Remaining Notional Amount after Amortization
    amount : float, optional
        Amortization Amount at each Amortization Date

    Examples
    ----------
    >>> amortization_item = AmortizationItem(
    ...     start_date="2021-02-11",
    ...     end_date="2022-02-11",
    ...     amount=100000,
    ...     amortization_type=AmortizationType.SCHEDULE
    ... )
    >>> amortization_item
    """

    def __init__(
        self,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        amortization_frequency: Optional[AmortizationFrequency] = None,
        amortization_type: Union[AmortizationType, str] = None,
        remaining_notional: Optional[float] = None,
        amount: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.amortization_frequency = amortization_frequency
        self.amortization_type = amortization_type
        self.remaining_notional = remaining_notional
        self.amount = amount

    def _get_items(self):
        return [
            enum_param_item.to_kv("amortizationFrequency", self.amortization_frequency),
            enum_param_item.to_kv("amortizationType", self.amortization_type),
            param_item.to_kv("amount", self.amount),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("remainingNotional", self.remaining_notional),
            datetime_param_item.to_kv("startDate", self.start_date),
        ]
