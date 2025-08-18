from typing import Optional, TYPE_CHECKING

from ._constituents_description import (
    CrossCurrencyConstituentsDescription,
)
from ._curve_parameters import CrossCurrencyCurveParameters
from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptDateTime


class CrossCurrencyInstrumentsSegment(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    start_date : str or date or datetime or timedelta, optional

    constituents : CrossCurrencyConstituentsDescription, optional

    curve_parameters : CrossCurrencyCurveParameters, optional

    """

    def __init__(
        self,
        start_date: "OptDateTime" = None,
        constituents: Optional[CrossCurrencyConstituentsDescription] = None,
        curve_parameters: Optional[CrossCurrencyCurveParameters] = None,
    ) -> None:
        super().__init__()
        self.start_date = start_date
        self.constituents = constituents
        self.curve_parameters = curve_parameters

    @property
    def constituents(self):
        """
        :return: object CrossCurrencyConstituentsDescription
        """
        return self._get_object_parameter(CrossCurrencyConstituentsDescription, "constituents")

    @constituents.setter
    def constituents(self, value):
        self._set_object_parameter(CrossCurrencyConstituentsDescription, "constituents", value)

    @property
    def curve_parameters(self):
        """
        :return: object CrossCurrencyCurveParameters
        """
        return self._get_object_parameter(CrossCurrencyCurveParameters, "curveParameters")

    @curve_parameters.setter
    def curve_parameters(self, value):
        self._set_object_parameter(CrossCurrencyCurveParameters, "curveParameters", value)

    @property
    def start_date(self):
        """
        :return: str
        """
        return self._get_parameter("startDate")

    @start_date.setter
    def start_date(self, value):
        self._set_datetime_parameter("startDate", value)
