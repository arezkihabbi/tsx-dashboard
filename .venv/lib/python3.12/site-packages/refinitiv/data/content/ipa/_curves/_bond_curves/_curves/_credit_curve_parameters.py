from typing import Optional, TYPE_CHECKING

from ....curves._enums import CompoundingType
from ......_tools import try_copy_to_list
from .....ipa._enums._extrapolation_mode import ExtrapolationMode
from ...._object_definition import ObjectDefinition
from ..._bond_curves._enums import (
    BasisSplineSmoothModel,
    CalendarAdjustment,
    CalibrationModel,
    InterestCalculationMethod,
    InterpolationMode,
    PriceSide,
)


if TYPE_CHECKING:
    from ......_types import OptStrings, OptInt, OptBool, OptDateTime


class CreditCurveParameters(ObjectDefinition):
    """
    Generates the credit curves for the definition provided

    Parameters
    ----------
    interest_calculation_method : InterestCalculationMethod, optional
        The day count basis method used to compute the points of the zero coupon curve.
        the possible values are:   * dcb_30_360     actual number of days in the coupon
        period calculated on the basis of a year of 360 days with twelve 30-day months
        unless:     - the last day of the period is the 31st day of a month and the
        first day of the period is a day other than the 30th or 31st day of a month, in
        which case the month that includes the last day shall not be considered to be
        shortened to a 30-day month,     - the last day of the period is the last day of
        the month of february, in which case the month of february shall not be
        considered to be lengthened to a 30-day month.   * dcb_30_actual     the day
        count is identical to 30/360 (us) and the year basis is identical to
        actual/actual.   * dcb_actual_360     the day count is the actual number of days
        of the period. the year basis is 360.   * dcb_actual_365     the day count is
        the actual number of days of the period. the year basis is 365.   *
        dcb_actual_actual     the dcb is calculated by actual days / year basis where:
        - actual days are defined as the actual days between the starting date
        (d1.m1.y1) and end date (d2.m2.y2).     - year basis is defined as the actual
        days between the start date (d1.m1.y1) and the next relevant interest payment
        date (d3.m3.y3) multiplied by the instrument coupon frequency.   *
        dcb_actual_actual_isda     similar to actual/365, except for a period that
        includes days falling in a leap year. it is calculated by dcb = number of days
        in a leap year/366 + number of days in a non-leap year/365.     a convention is
        also known as actual/365 isda.   *dcb_30_360_isda     for two dates (y1,m1,d1)
        and (y2,m2,d2):     - if d1 is 31, change it to 30,     - if d2 is 31 and d1 is
        30, change d2 to 30.     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_30_365_isda     for two dates (y1,m1,d1)
        and (y2,m2,d2):     - if d1=31 then d1=30,     - if d2=31 and d1=30 or 31 then
        d2=30.     then the date difference is (y2-y1)*365+(m2-m1)*30+(d2-d1)   *
        dcb_30_360_us     for two dates (y1,m1,d1) and (y2,m2,d2):     - if d1=31 then
        d1=30,     - if d2=31 and d1=30 or 31 then d2=30,     - if d1 is the last day of
        february then d1=30,     - if d1 is the last day of february and d2 is the last
        day of february then d2=30.     the last day of february is february 29 in leap
        years and february 28 in non leap years.     the 30/360 us rule is identical to
        30/360 isda when the eom (end-of-month) convention does not apply. this
        indicates whether all coupon payment dates fall on the last day of the month. if
        the investment is not eom, it will always pay on the same day of the month
        (e.g., the 10th).     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_actual_actual_afb     the dcb is
        calculated by actual days / year basis where:     actual days are defined as the
        actual days between the start date (d1.m1.y1) and end date (d2.m2.y2).     year
        basis is either 365 if the calculation period does not contain 29th feb, or 366
        if the calculation period includes 29th feb.   * dcb_workingdays_252     the day
        count is the actual number of business days of the period according to the
        instrument calendars. the year basis is 252. commonly used in the brazilian
        market.   * dcb_actual_365l     the day count is the actual number of days of
        the period. the year basis is calculated in the following two rules:     - if
        the coupon frequency is annual, then year basis is 366 if the 29 feb. is
        included in the interest period, else 365,     - if the coupon frequency is not
        annual, then year basis is 366 for each interest period where ending date falls
        in a leap year, otherwise it is 365.   * dcb_actualleapday_365     the day count
        ignores 29th february when counting days. the year basis is 365 days.   *
        dcb_actualleapday_360     the day count ignores 29th february when counting
        days. the year basis is 360 days.   * dcb_actual_36525     the day count is the
        actual number of days of the period. the year basis is 365.25.   *
        dcb_actual_365_canadianconvention     follows the canadian domestic bond market
        convention. the day count basis is computed as follows:     - if the number of
        days of a period is less than the actual number of days in a regular coupon
        period the dcb_actual_365 convention is used,     - otherwise: dcb = 1 -
        daysremaininginperiod x frequency / 365.   * dcb_30_360_german     for two dates
        (y1,m1,d1) and (y2,m2,d2):     - if d1=31 then d1=30,     - if d2=31 then d2=30,
        - if d1 is the last day of february then d1=30,     - if d2 is the last day of
        february then d2=30.     the last day of february is february 29 in leap years
        and february 28 in non leap years.     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_30_365_german     similar to 30/360
        (german), except that the year basis is treated as 365 days.   *
        dcb_30_actual_german     the day count is identical to 30/360 (german) and the
        year basis is similar to actual/actual. this method was formerly used in the
        eurobond markets.   * dcb_30e_360_isma     actual number of days in the coupon
        period calculated on the basis of a year of 360 days with twelve 30-day months
        (regardless of the date of the first day or last day of the period).   *
        dcb_actual_364     a special case of actual/actual (isma) when a coupon period
        contains 91 or 182 days. actual/364 applies for some short-term instruments.
        day count basis = 364.   * dcb_30_actual_isda   * dcb_30_365_brazil   *
        dcb_actual_365p   * dcb_constant
    basis_spline_smooth_model : BasisSplineSmoothModel, optional
        Basis spline model. values can be: - mccullochlinearregression -
        waggonersmoothingsplinemodel - andersonsmoothingsplinemodel
    calendar_adjustment : CalendarAdjustment, optional
        The cash flow adjustment according to a selected calendar. the possible values
        are:   * no   * weekend: for the cash flow pricing using the calendar 'weekend'
        * calendar: for the cash flow pricing using the calendar defined by the
        parameter 'calendars'. the default value is 'calendar'.
    calendars : string, optional
        The list of comma-separated calendar codes used to define non-working days and
        to adjust interest rate curve coupon dates and values (e.g., 'emu_fi'). by
        default, the calendar code is derived from the interest rate curve currency.
    calibration_model : CalibrationModel, optional
        Bond zero coupon curve calibration method. values can be:   - basisspline   -
        nelsonsiegelsvensson   - bootstrap
    compounding_type : CompoundingType, optional
        The yield type of the interest rate curve. the possible values are:   *
        continuous   * moneymarket   * compounded   * discounted the default value is
        'compounded'.
    extrapolation_mode : ExtrapolationMode, optional
        The extrapolation method used in the zero coupon curve bootstrapping. the
        possible values are:   * none: no extrapolation,   * constant: constant
        extrapolation,   * linear: linear extrapolation. the default value is 'none'.
    interpolation_mode : InterpolationMode, optional
        The interpolation method used in zero curve bootstrapping. the possible values
        are:   * cubicdiscount: local cubic interpolation of discount factors   *
        cubicrate: local cubic interpolation of rates   * cubicspline: a natural cubic
        spline   * forwardmonotoneconvex: forward monotone convexc interpolation   *
        linear: linear interpolation   * log: log-linear interpolation   * hermite:
        hermite (bessel) interpolation   * akimamethod: the akima method (a smoother
        variant of local cubic interpolation)   * fritschbutlandmethod: the
        fritsch-butland method (a monotonic cubic variant)   * krugermethod: the kruger
        method (a monotonic cubic variant)   * monotoniccubicnaturalspline: a monotonic
        natural cubic spline   * monotonichermitecubic: monotonic hermite (bessel) cubic
        interpolation   * tensionspline: a tension spline
    price_side : PriceSide, optional
        The quoted price side of the instrument to be used for the zero coupon curve
        construction. the possible values are:   * bid   * ask   * mid the default value
        is 'mid'.
    basis_spline_knots : int, optional
        Number of knots you can choose to build the yield curve when using the
        basis-spline models
    return_calibrated_parameters : bool, optional
        If true, returns parametric model calibrated parameters
    use_delayed_data_if_denied : bool, optional
        Use delayed ric to retrieve data when not permissioned on constituent ric. the
        default value is 'false'.
    use_duration_weighted_minimization : bool, optional
        Specifies the type of minimization of residual errors in the vasicek-fong model
        and basis spline model: - true: minimize residual errors between market and
        model prices weighted by the inverse of the modified duration of the bonds -
        false: minimize residual errors between market and model prices
    use_multi_dimensional_solver : bool, optional
        An indicator whether the multi-dimensional solver for yield curve bootstrapping
        must be used. this solving method is required because the bootstrapping method
        sometimes creates a zero coupon curve which does not accurately reprice the
        input instruments used to build it. the multi-dimensional solver is recommended
        when cubic interpolation methods are used in building the curve (in other cases,
        performance might be inferior to the regular bootstrapping method). when use for
        credit curve it is only used when the calibrationmodel is set to 'bootstrap'.
        the possible values are:   * true: the multi-dimensional solver is used,   *
        false: the multi-dimensional solver is not used. the default value is 'true'.
    valuation_date : str or date or timedelta, optional
        Valuation date for this curve, that means the data at which instrument market
        data is retrieved.
    """

    def __init__(
        self,
        interest_calculation_method: Optional[InterestCalculationMethod] = None,
        basis_spline_smooth_model: Optional[BasisSplineSmoothModel] = None,
        calendar_adjustment: Optional[CalendarAdjustment] = None,
        calendars: "OptStrings" = None,
        calibration_model: Optional[CalibrationModel] = None,
        compounding_type: Optional[CompoundingType] = None,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[InterpolationMode] = None,
        price_side: Optional[PriceSide] = None,
        basis_spline_knots: "OptInt" = None,
        return_calibrated_parameters: "OptBool" = None,
        use_delayed_data_if_denied: "OptBool" = None,
        use_duration_weighted_minimization: "OptBool" = None,
        use_multi_dimensional_solver: "OptBool" = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.interest_calculation_method = interest_calculation_method
        self.basis_spline_smooth_model = basis_spline_smooth_model
        self.calendar_adjustment = calendar_adjustment
        self.calendars = try_copy_to_list(calendars)
        self.calibration_model = calibration_model
        self.compounding_type = compounding_type
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.price_side = price_side
        self.basis_spline_knots = basis_spline_knots
        self.return_calibrated_parameters = return_calibrated_parameters
        self.use_delayed_data_if_denied = use_delayed_data_if_denied
        self.use_duration_weighted_minimization = use_duration_weighted_minimization
        self.use_multi_dimensional_solver = use_multi_dimensional_solver
        self.valuation_date = valuation_date

    @property
    def basis_spline_smooth_model(self):
        """
        Basis spline model. values can be: - mccullochlinearregression -
        waggonersmoothingsplinemodel - andersonsmoothingsplinemodel
        :return: enum BasisSplineSmoothModel
        """
        return self._get_enum_parameter(BasisSplineSmoothModel, "basisSplineSmoothModel")

    @basis_spline_smooth_model.setter
    def basis_spline_smooth_model(self, value):
        self._set_enum_parameter(BasisSplineSmoothModel, "basisSplineSmoothModel", value)

    @property
    def calendar_adjustment(self):
        """
        The cash flow adjustment according to a selected calendar. the possible values
        are:   * no   * weekend: for the cash flow pricing using the calendar 'weekend'
        * calendar: for the cash flow pricing using the calendar defined by the
        parameter 'calendars'. the default value is 'calendar'.
        :return: enum CalendarAdjustment
        """
        return self._get_enum_parameter(CalendarAdjustment, "calendarAdjustment")

    @calendar_adjustment.setter
    def calendar_adjustment(self, value):
        self._set_enum_parameter(CalendarAdjustment, "calendarAdjustment", value)

    @property
    def calendars(self):
        """
        The list of comma-separated calendar codes used to define non-working days and
        to adjust interest rate curve coupon dates and values (e.g., 'emu_fi'). by
        default, the calendar code is derived from the interest rate curve currency.
        :return: list string
        """
        return self._get_list_parameter(str, "calendars")

    @calendars.setter
    def calendars(self, value):
        self._set_list_parameter(str, "calendars", value)

    @property
    def calibration_model(self):
        """
        Bond zero coupon curve calibration method. values can be:   - basisspline   -
        nelsonsiegelsvensson   - bootstrap
        :return: enum CalibrationModel
        """
        return self._get_enum_parameter(CalibrationModel, "calibrationModel")

    @calibration_model.setter
    def calibration_model(self, value):
        self._set_enum_parameter(CalibrationModel, "calibrationModel", value)

    @property
    def compounding_type(self):
        """
        The yield type of the interest rate curve. the possible values are:   *
        continuous   * moneymarket   * compounded   * discounted the default value is
        'compounded'.
        :return: enum CompoundingType
        """
        return self._get_enum_parameter(CompoundingType, "compoundingType")

    @compounding_type.setter
    def compounding_type(self, value):
        self._set_enum_parameter(CompoundingType, "compoundingType", value)

    @property
    def extrapolation_mode(self):
        """
        The extrapolation method used in the zero coupon curve bootstrapping. the
        possible values are:   * none: no extrapolation,   * constant: constant
        extrapolation,   * linear: linear extrapolation. the default value is 'none'.
        :return: enum ExtrapolationMode
        """
        return self._get_enum_parameter(ExtrapolationMode, "extrapolationMode")

    @extrapolation_mode.setter
    def extrapolation_mode(self, value):
        self._set_enum_parameter(ExtrapolationMode, "extrapolationMode", value)

    @property
    def interest_calculation_method(self):
        """
        The day count basis method used to compute the points of the zero coupon curve.
        the possible values are:   * dcb_30_360     actual number of days in the coupon
        period calculated on the basis of a year of 360 days with twelve 30-day months
        unless:     - the last day of the period is the 31st day of a month and the
        first day of the period is a day other than the 30th or 31st day of a month, in
        which case the month that includes the last day shall not be considered to be
        shortened to a 30-day month,     - the last day of the period is the last day of
        the month of february, in which case the month of february shall not be
        considered to be lengthened to a 30-day month.   * dcb_30_actual     the day
        count is identical to 30/360 (us) and the year basis is identical to
        actual/actual.   * dcb_actual_360     the day count is the actual number of days
        of the period. the year basis is 360.   * dcb_actual_365     the day count is
        the actual number of days of the period. the year basis is 365.   *
        dcb_actual_actual     the dcb is calculated by actual days / year basis where:
        - actual days are defined as the actual days between the starting date
        (d1.m1.y1) and end date (d2.m2.y2).     - year basis is defined as the actual
        days between the start date (d1.m1.y1) and the next relevant interest payment
        date (d3.m3.y3) multiplied by the instrument coupon frequency.   *
        dcb_actual_actual_isda     similar to actual/365, except for a period that
        includes days falling in a leap year. it is calculated by dcb = number of days
        in a leap year/366 + number of days in a non-leap year/365.     a convention is
        also known as actual/365 isda.   *dcb_30_360_isda     for two dates (y1,m1,d1)
        and (y2,m2,d2):     - if d1 is 31, change it to 30,     - if d2 is 31 and d1 is
        30, change d2 to 30.     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_30_365_isda     for two dates (y1,m1,d1)
        and (y2,m2,d2):     - if d1=31 then d1=30,     - if d2=31 and d1=30 or 31 then
        d2=30.     then the date difference is (y2-y1)*365+(m2-m1)*30+(d2-d1)   *
        dcb_30_360_us     for two dates (y1,m1,d1) and (y2,m2,d2):     - if d1=31 then
        d1=30,     - if d2=31 and d1=30 or 31 then d2=30,     - if d1 is the last day of
        february then d1=30,     - if d1 is the last day of february and d2 is the last
        day of february then d2=30.     the last day of february is february 29 in leap
        years and february 28 in non leap years.     the 30/360 us rule is identical to
        30/360 isda when the eom (end-of-month) convention does not apply. this
        indicates whether all coupon payment dates fall on the last day of the month. if
        the investment is not eom, it will always pay on the same day of the month
        (e.g., the 10th).     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_actual_actual_afb     the dcb is
        calculated by actual days / year basis where:     actual days are defined as the
        actual days between the start date (d1.m1.y1) and end date (d2.m2.y2).     year
        basis is either 365 if the calculation period does not contain 29th feb, or 366
        if the calculation period includes 29th feb.   * dcb_workingdays_252     the day
        count is the actual number of business days of the period according to the
        instrument calendars. the year basis is 252. commonly used in the brazilian
        market.   * dcb_actual_365l     the day count is the actual number of days of
        the period. the year basis is calculated in the following two rules:     - if
        the coupon frequency is annual, then year basis is 366 if the 29 feb. is
        included in the interest period, else 365,     - if the coupon frequency is not
        annual, then year basis is 366 for each interest period where ending date falls
        in a leap year, otherwise it is 365.   * dcb_actualleapday_365     the day count
        ignores 29th february when counting days. the year basis is 365 days.   *
        dcb_actualleapday_360     the day count ignores 29th february when counting
        days. the year basis is 360 days.   * dcb_actual_36525     the day count is the
        actual number of days of the period. the year basis is 365.25.   *
        dcb_actual_365_canadianconvention     follows the canadian domestic bond market
        convention. the day count basis is computed as follows:     - if the number of
        days of a period is less than the actual number of days in a regular coupon
        period the dcb_actual_365 convention is used,     - otherwise: dcb = 1 -
        daysremaininginperiod x frequency / 365.   * dcb_30_360_german     for two dates
        (y1,m1,d1) and (y2,m2,d2):     - if d1=31 then d1=30,     - if d2=31 then d2=30,
        - if d1 is the last day of february then d1=30,     - if d2 is the last day of
        february then d2=30.     the last day of february is february 29 in leap years
        and february 28 in non leap years.     then the date difference is
        (y2-y1)x360+(m2-m1)*30+(d2-d1).   * dcb_30_365_german     similar to 30/360
        (german), except that the year basis is treated as 365 days.   *
        dcb_30_actual_german     the day count is identical to 30/360 (german) and the
        year basis is similar to actual/actual. this method was formerly used in the
        eurobond markets.   * dcb_30e_360_isma     actual number of days in the coupon
        period calculated on the basis of a year of 360 days with twelve 30-day months
        (regardless of the date of the first day or last day of the period).   *
        dcb_actual_364     a special case of actual/actual (isma) when a coupon period
        contains 91 or 182 days. actual/364 applies for some short-term instruments.
        day count basis = 364.   * dcb_30_actual_isda   * dcb_30_365_brazil   *
        dcb_actual_365p   * dcb_constant
        :return: enum InterestCalculationMethod
        """
        return self._get_enum_parameter(InterestCalculationMethod, "interestCalculationMethod")

    @interest_calculation_method.setter
    def interest_calculation_method(self, value):
        self._set_enum_parameter(InterestCalculationMethod, "interestCalculationMethod", value)

    @property
    def interpolation_mode(self):
        """
        The interpolation method used in zero curve bootstrapping. the possible values
        are:   * cubicdiscount: local cubic interpolation of discount factors   *
        cubicrate: local cubic interpolation of rates   * cubicspline: a natural cubic
        spline   * forwardmonotoneconvex: forward monotone convexc interpolation   *
        linear: linear interpolation   * log: log-linear interpolation   * hermite:
        hermite (bessel) interpolation   * akimamethod: the akima method (a smoother
        variant of local cubic interpolation)   * fritschbutlandmethod: the
        fritsch-butland method (a monotonic cubic variant)   * krugermethod: the kruger
        method (a monotonic cubic variant)   * monotoniccubicnaturalspline: a monotonic
        natural cubic spline   * monotonichermitecubic: monotonic hermite (bessel) cubic
        interpolation   * tensionspline: a tension spline
        :return: enum InterpolationMode
        """
        return self._get_enum_parameter(InterpolationMode, "interpolationMode")

    @interpolation_mode.setter
    def interpolation_mode(self, value):
        self._set_enum_parameter(InterpolationMode, "interpolationMode", value)

    @property
    def price_side(self):
        """
        The quoted price side of the instrument to be used for the zero coupon curve
        construction. the possible values are:   * bid   * ask   * mid the default value
        is 'mid'.
        :return: enum PriceSide
        """
        return self._get_enum_parameter(PriceSide, "priceSide")

    @price_side.setter
    def price_side(self, value):
        self._set_enum_parameter(PriceSide, "priceSide", value)

    @property
    def basis_spline_knots(self):
        """
        Number of knots you can choose to build the yield curve when using the
        basis-spline models
        :return: int
        """
        return self._get_parameter("basisSplineKnots")

    @basis_spline_knots.setter
    def basis_spline_knots(self, value):
        self._set_parameter("basisSplineKnots", value)

    @property
    def return_calibrated_parameters(self):
        """
        If true, returns parametric model calibrated parameters
        :return: bool
        """
        return self._get_parameter("returnCalibratedParameters")

    @return_calibrated_parameters.setter
    def return_calibrated_parameters(self, value):
        self._set_parameter("returnCalibratedParameters", value)

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
    def use_duration_weighted_minimization(self):
        """
        Specifies the type of minimization of residual errors in the vasicek-fong model
        and basis spline model: - true: minimize residual errors between market and
        model prices weighted by the inverse of the modified duration of the bonds -
        false: minimize residual errors between market and model prices
        :return: bool
        """
        return self._get_parameter("useDurationWeightedMinimization")

    @use_duration_weighted_minimization.setter
    def use_duration_weighted_minimization(self, value):
        self._set_parameter("useDurationWeightedMinimization", value)

    @property
    def use_multi_dimensional_solver(self):
        """
        An indicator whether the multi-dimensional solver for yield curve bootstrapping
        must be used. this solving method is required because the bootstrapping method
        sometimes creates a zero coupon curve which does not accurately reprice the
        input instruments used to build it. the multi-dimensional solver is recommended
        when cubic interpolation methods are used in building the curve (in other cases,
        performance might be inferior to the regular bootstrapping method). when use for
        credit curve it is only used when the calibrationmodel is set to 'bootstrap'.
        the possible values are:   * true: the multi-dimensional solver is used,   *
        false: the multi-dimensional solver is not used. the default value is 'true'.
        :return: bool
        """
        return self._get_parameter("useMultiDimensionalSolver")

    @use_multi_dimensional_solver.setter
    def use_multi_dimensional_solver(self, value):
        self._set_parameter("useMultiDimensionalSolver", value)

    @property
    def valuation_date(self):
        """
        Valuation date for this curve, that means the data at which instrument market
        data is retrieved.
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)
