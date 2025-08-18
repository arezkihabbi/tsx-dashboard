from typing import Optional, Union

from ..._enums import AverageType, FixingFrequency
from ..._param_item import param_item, datetime_param_item, enum_param_item
from ..._serializable import Serializable


class EtiFixingInfo(Serializable):
    """
    Parameters
    ----------
    average_type : AverageType or str, optional
        The type of average used to compute.
    fixing_frequency : FixingFrequency or str, optional
        The fixing's frequency.
    average_so_far : float, optional
        The value of the average_type
    fixing_calendar : str, optional
        The calendar of the underlying's currency.
    fixing_end_date : str or date or datetime or timedelta, optional
        The end date of the fixing period. Should be less or equal to the expiry.
    fixing_start_date : str or date or datetime or timedelta, optional
        The beginning date of the fixing period.
    include_holidays : bool, optional
        Include the holidays in the list of fixings
    include_week_ends : bool, optional
        Include the week-ends in the list of fixings
    """

    def __init__(
        self,
        average_type: Union[AverageType, str] = None,
        fixing_frequency: Union[FixingFrequency, str] = None,
        average_so_far: Optional[float] = None,
        fixing_calendar: Optional[str] = None,
        fixing_end_date: "OptDateTime" = None,
        fixing_start_date: "OptDateTime" = None,
        include_holidays: Optional[bool] = None,
        include_week_ends: Optional[bool] = None,
    ) -> None:
        super().__init__()
        self.average_type = average_type
        self.fixing_frequency = fixing_frequency
        self.average_so_far = average_so_far
        self.fixing_calendar = fixing_calendar
        self.fixing_end_date = fixing_end_date
        self.fixing_start_date = fixing_start_date
        self.include_holidays = include_holidays
        self.include_week_ends = include_week_ends

    def _get_items(self):
        return [
            enum_param_item.to_kv("averageType", self.average_type),
            enum_param_item.to_kv("fixingFrequency", self.fixing_frequency),
            param_item.to_kv("averageSoFar", self.average_so_far),
            param_item.to_kv("fixingCalendar", self.fixing_calendar),
            datetime_param_item.to_kv("fixingEndDate", self.fixing_end_date),
            datetime_param_item.to_kv("fixingStartDate", self.fixing_start_date),
            param_item.to_kv("includeHolidays", self.include_holidays),
            param_item.to_kv("includeWeekEnds", self.include_week_ends),
        ]
