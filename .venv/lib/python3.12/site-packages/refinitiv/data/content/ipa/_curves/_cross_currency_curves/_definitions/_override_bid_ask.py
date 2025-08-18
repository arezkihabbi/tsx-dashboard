from typing import Optional, TYPE_CHECKING

from ._override_bid_ask_fields import OverrideBidAskFields
from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptStr, OptDateTime


class OverrideBidAsk(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    instrument_code : str, optional
        Reuters instrument code (ric)
    fields : OverrideBidAskFields, optional

    date : str or date or datetime or timedelta, optional
        Overridden date
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        fields: Optional[OverrideBidAskFields] = None,
        date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code
        self.fields = fields
        self.date = date

    @property
    def fields(self):
        """
        :return: object OverrideBidAskFields
        """
        return self._get_object_parameter(OverrideBidAskFields, "fields")

    @fields.setter
    def fields(self, value):
        self._set_object_parameter(OverrideBidAskFields, "fields", value)

    @property
    def date(self):
        """
        Overridden date
        :return: str
        """
        return self._get_parameter("date")

    @date.setter
    def date(self, value):
        self._set_date_parameter("date", value)

    @property
    def instrument_code(self):
        """
        Reuters instrument code (ric)
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)
