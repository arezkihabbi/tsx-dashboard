from ...._tools import add_periods_datetime_adapter
from .._object_definition import ObjectDefinition


class StartEndDateBase(ObjectDefinition):
    def __init__(
        self,
        start_date,
        end_date,
    ):
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date

    @property
    def start_date(self):
        """
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        if value is not None:
            value = add_periods_datetime_adapter.get_str(value)
        self._set_parameter("startDate", value)

    @property
    def end_date(self):
        """
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        if value is not None:
            value = add_periods_datetime_adapter.get_str(value)
        self._set_parameter("endDate", value)


class StartDateBase(ObjectDefinition):
    def __init__(
        self,
        start_date,
    ):
        super().__init__()
        self.start_date = start_date

    @property
    def start_date(self):
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        if value is not None:
            value = add_periods_datetime_adapter.get_str(value)
        self._set_parameter("startDate", value)


class DateBase(ObjectDefinition):
    def __init__(
        self,
        date,
    ):
        super().__init__()
        self.date = date

    @property
    def date(self):
        return self._get_parameter("date")

    @date.setter
    def date(self, value):
        if value is not None:
            value = add_periods_datetime_adapter.get_str(value)
        self._set_parameter("date", value)
