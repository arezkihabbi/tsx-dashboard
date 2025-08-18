from typing import Optional, TYPE_CHECKING

from ...._enums._extrapolation_mode import ExtrapolationMode
from ...._enums._interpolation_mode import InterpolationMode
from ...._object_definition import ObjectDefinition
from ....curves._models import ValuationTime

if TYPE_CHECKING:
    from ......_types import OptBool, OptDateTime


class FxForwardCurveParameters(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    extrapolation_mode : ExtrapolationMode, optional

    interpolation_mode : InterpolationMode, optional

    valuation_time : ValuationTime, optional
        The time identified by offsets at which the zero coupon curve is generated.
    ignore_invalid_instrument : bool, optional
        Ignore invalid instrument to calculate the curve.  if false and some instrument
        are invlide, the curve is not calculated and an error is returned.  the default
        value is 'true'.
    ignore_pivot_currency_holidays : bool, optional

    use_delayed_data_if_denied : bool, optional
        Use delayed ric to retrieve data when not permissioned on constituent ric. the
        default value is 'false'.
    valuation_date : str or date or datetime or timedelta, optional

    valuation_date_time : str or date or datetime or timedelta, optional
        The date and time at which the zero coupon curve is generated. the value is
        expressed in iso 8601 format: yyyy-mm-ddt00:00:00z (e.g., '2021-01-01t14:00:00z'
        or '2021-01-01t14:00:00+02:00'). only one parameter of valuationdate and
        valuationdatetime must be specified.
    """

    def __init__(
        self,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[InterpolationMode] = None,
        valuation_time: Optional[ValuationTime] = None,
        ignore_invalid_instrument: "OptBool" = None,
        ignore_pivot_currency_holidays: "OptBool" = None,
        use_delayed_data_if_denied: "OptBool" = None,
        valuation_date: "OptDateTime" = None,
        valuation_date_time: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.valuation_time = valuation_time
        self.ignore_invalid_instrument = ignore_invalid_instrument
        self.ignore_pivot_currency_holidays = ignore_pivot_currency_holidays
        self.use_delayed_data_if_denied = use_delayed_data_if_denied
        self.valuation_date = valuation_date
        self.valuation_date_time = valuation_date_time

    @property
    def extrapolation_mode(self):
        """
        :return: enum ExtrapolationMode
        """
        return self._get_enum_parameter(ExtrapolationMode, "extrapolationMode")

    @extrapolation_mode.setter
    def extrapolation_mode(self, value):
        self._set_enum_parameter(ExtrapolationMode, "extrapolationMode", value)

    @property
    def interpolation_mode(self):
        """
        :return: enum InterpolationMode
        """
        return self._get_enum_parameter(InterpolationMode, "interpolationMode")

    @interpolation_mode.setter
    def interpolation_mode(self, value):
        self._set_enum_parameter(InterpolationMode, "interpolationMode", value)

    @property
    def valuation_time(self):
        """
        The time identified by offsets at which the zero coupon curve is generated.
        :return: object ValuationTime
        """
        return self._get_object_parameter(ValuationTime, "valuationTime")

    @valuation_time.setter
    def valuation_time(self, value):
        self._set_object_parameter(ValuationTime, "valuationTime", value)

    @property
    def ignore_invalid_instrument(self):
        """
        Ignore invalid instrument to calculate the curve.  if false and some instrument
        are invlide, the curve is not calculated and an error is returned.  the default
        value is 'true'.
        :return: bool
        """
        return self._get_parameter("ignoreInvalidInstrument")

    @ignore_invalid_instrument.setter
    def ignore_invalid_instrument(self, value):
        self._set_parameter("ignoreInvalidInstrument", value)

    @property
    def ignore_pivot_currency_holidays(self):
        """
        :return: bool
        """
        return self._get_parameter("ignorePivotCurrencyHolidays")

    @ignore_pivot_currency_holidays.setter
    def ignore_pivot_currency_holidays(self, value):
        self._set_parameter("ignorePivotCurrencyHolidays", value)

    @property
    def use_delayed_data_if_denied(self):
        """
        Use delayed ric to retrieve data when not permissioned on constituent ric. the
        default value is 'false'.
        :return: bool
        """
        return self._get_parameter("useDelayedDataIfDenied")

    @use_delayed_data_if_denied.setter
    def use_delayed_data_if_denied(self, value):
        self._set_parameter("useDelayedDataIfDenied", value)

    @property
    def valuation_date(self):
        """
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)

    @property
    def valuation_date_time(self):
        """
        The date and time at which the zero coupon curve is generated. the value is
        expressed in iso 8601 format: yyyy-mm-ddt00:00:00z (e.g., '2021-01-01t14:00:00z'
        or '2021-01-01t14:00:00+02:00'). only one parameter of valuationdate and
        valuationdatetime must be specified.
        :return: str
        """
        return self._get_parameter("valuationDateTime")

    @valuation_date_time.setter
    def valuation_date_time(self, value):
        self._set_datetime_parameter("valuationDateTime", value)
