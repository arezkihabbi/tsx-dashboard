from typing import Optional, TYPE_CHECKING

from ._fx_forward_turn_fields import FxForwardTurnFields
from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptStr, OptDateTime


class OverrideFxForwardTurn(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    start_date : str or date or datetime or timedelta, optional

    end_date : str or date or datetime or timedelta, optional

    fields : FxForwardTurnFields, optional

    date : "OptDateTime"

    turn_tag : str, optional

    """

    def __init__(
        self,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        fields: Optional[FxForwardTurnFields] = None,
        date: "OptDateTime" = None,
        turn_tag: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.start_date = start_date
        self.end_date = end_date
        self.fields = fields
        self.date = date
        self.turn_tag = turn_tag

    @property
    def fields(self):
        """
        :return: object FxForwardTurnFields
        """
        return self._get_object_parameter(FxForwardTurnFields, "fields")

    @fields.setter
    def fields(self, value):
        self._set_object_parameter(FxForwardTurnFields, "fields", value)

    @property
    def date(self):
        """
        :return: str
        """
        return self._get_parameter("date")

    @date.setter
    def date(self, value):
        self._set_date_parameter("date", value)

    @property
    def end_date(self):
        """
        :return: str
        """
        return self._get_parameter("endDate")

    @end_date.setter
    def end_date(self, value):
        self._set_date_parameter("endDate", value)

    @property
    def start_date(self):
        """
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_date_parameter("startDate", value)

    @property
    def turn_tag(self):
        """
        :return: str
        """
        return self._get_parameter("turnTag")

    @turn_tag.setter
    def turn_tag(self, value):
        self._set_parameter("turnTag", value)
