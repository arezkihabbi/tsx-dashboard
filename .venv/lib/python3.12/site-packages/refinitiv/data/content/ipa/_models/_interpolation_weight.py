from typing import Optional, Iterable

from .._models import DayWeight
from .._param_item import param_item, list_serializable_param_item
from .._serializable import Serializable
from ...._tools import try_copy_to_list


class InterpolationWeight(Serializable):
    """
    Parameters
    ----------
    days_list : list of DayWeight, optional

    holidays : float, optional

    week_days : float, optional

    week_ends : float, optional

    """

    def __init__(
        self,
        days_list: Optional[Iterable[DayWeight]] = None,
        holidays: Optional[float] = None,
        week_days: Optional[float] = None,
        week_ends: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.days_list = try_copy_to_list(days_list)
        self.holidays = holidays
        self.week_days = week_days
        self.week_ends = week_ends

    def _get_items(self):
        return [
            list_serializable_param_item.to_kv("daysList", self.days_list),
            param_item.to_kv("holidays", self.holidays),
            param_item.to_kv("weekDays", self.week_days),
            param_item.to_kv("weekEnds", self.week_ends),
        ]
