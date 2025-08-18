from typing import Optional, Iterable

from .._enums import (
    CalendarAdjustment,
    CompoundingType,
    MarketDataAccessDeniedFallback,
    SwapPriceSide,
    ZcInterpolationMode,
)
from .._models import (
    ConvexityAdjustment,
    InterestRateCurveParameters,
    Step,
    Turn,
    ValuationTime,
)
from ..._enums import DayCountBasis
from ..._enums._extrapolation_mode import ExtrapolationMode
from ..._param_item import (
    datetime_param_item,
    enum_param_item,
    param_item,
    serializable_param_item,
    list_serializable_param_item,
    date_param_item,
)
from ..._serializable import Serializable
from ....._tools import create_repr, try_copy_to_list
from ....._types import OptBool, OptStr, Strings, OptDateTime


class ZcCurveParameters(Serializable):
    """
    Parameters
    ----------
    interest_calculation_method : DayCountBasis, optional
        Day count basis of the calculated zero coupon rates
    calendar_adjustment : CalendarAdjustment, optional
        Cash flow adjustment according to a calendar.
        - No: for analytic pricing (i.e. from the bond structure)
        - Null: for cash flow pricing using the calendar null
        - Weekend: for cash flow pricing using the calendar weekend
        - Calendar: for cash flow pricing using the calendar defined
                    by the parameter calendars.
    calendars : string, optional
        A list of one or more calendar codes used to define non-working days and to
        adjust coupon dates and values.
    compounding_type : CompoundingType, optional
        Output rates yield type. Values can be:
        - Continuous: continuous rate (default value)
        - MoneyMarket: money market rate
        - Compounded: compounded rate
        - Discounted: discounted rate
    convexity_adjustment : ConvexityAdjustment, optional

    extrapolation_mode : ExtrapolationMode, optional
        Extrapolation method for the curve
        - None: no extrapolation
        - Constant: constant extrapolation
        - Linear: linear extrapolation
    interpolation_mode : ZcInterpolationMode, optional
        Interpolation method for the curve. Available values are:
        - CubicDiscount: local cubic interpolation of discount factors
        - CubicRate: local cubic interpolation of rates
        - CubicSpline: a natural cubic spline
        - ForwardMonotoneConvex: forward mMonotone Convexc interpolation
        - Linear: linear interpolation
        - Log: log-linear interpolation
        - Hermite: hermite (bessel) interpolation
        - AkimaMethod: the Akima method
            (a smoother variant of local cubic interpolation)
        - FritschButlandMethod: the Fritsch-Butland method (a monotonic cubic variant)
        - KrugerMethod: the Kruger method (a monotonic cubic variant)
        - MonotonicCubicNaturalSpline: a monotonic natural cubic spline
        - MonotonicHermiteCubic: monotonic hermite (Bessel) cubic interpolation
        - TensionSpline: a tension spline
    market_data_access_denied_fallback : MarketDataAccessDeniedFallback, optional
        - ReturnError: dont price the surface and return an error (Default value)
        - IgnoreConstituents: price the surface without the error market data
        - UseDelayedData: use delayed Market Data if possible
    pivot_curve_parameters : InterestRateCurveParameters, optional

    price_side : SwapPriceSide, optional
        Price side of the instrument to be used. default value is: mid
    reference_curve_parameters : InterestRateCurveParameters, optional

    steps : list of Step, optional

    turns : list of Turn, optional
        Used to include end period rates/turns when calculating swap rate surfaces
    reference_tenor : str, optional
        Root tenor(s) for the xIbor dependencies
    use_convexity_adjustment : bool, optional

    use_multi_dimensional_solver : bool, optional
        Specifies the use of the multi-dimensional solver for yield curve bootstrapping.
        This solving method is required because the bootstrapping method sometimes
        creates a ZC curve which does not accurately reprice the input instruments used
        to build it. The multi-dimensional solver is recommended when cubic
        interpolation methods are used in building the curve (in other cases,
        performance might be inferior to the regular bootstrapping method). When use for
        Credit Curve it is only used when the calibrationModel is set to Bootstrap.
        - true: to use multi-dimensional solver for yield curve bootstrapping
        - false: not to use multi-dimensional solver for yield curve bootstrapping
    use_steps : bool, optional

    valuation_date : str or date or datetime or timedelta, optional
        The valuation date. The default value is the current date.
    valuation_time : ValuationTime, optional
        The time identified by offsets at which the zero coupon curve is generated.
    ignore_invalid_instrument : bool, optional
        Ignore invalid instrument to calculate the curve.
        if False and some instrument are invlide, the curve is not calculated and an
        error is returned.
        The default value is 'True'.
    use_delayed_data_if_denied : bool, optional
        Use delayed ric to retrieve data when not permissioned on constituent ric.
        The default value is 'False'.
    valuation_date_time : str or date or datetime or timedelta, optional
        The date and time at which the zero coupon curve is generated. the value is
        expressed in iso 8601 format: yyyy-mm-ddt00:00:00z (e.g., '2021-01-01t14:00:00z'
        or '2021-01-01t14:00:00+02:00'). Only one parameter of valuation_date and
        valuation_date_time must be specified.
    """

    def __init__(
        self,
        interest_calculation_method: Optional[DayCountBasis] = None,
        calendar_adjustment: Optional[CalendarAdjustment] = None,
        calendars: Strings = None,
        compounding_type: Optional[CompoundingType] = None,
        convexity_adjustment: Optional[ConvexityAdjustment] = None,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[ZcInterpolationMode] = None,
        market_data_access_denied_fallback: Optional[MarketDataAccessDeniedFallback] = None,
        pivot_curve_parameters: Optional[InterestRateCurveParameters] = None,
        price_side: Optional[SwapPriceSide] = None,
        reference_curve_parameters: Optional[InterestRateCurveParameters] = None,
        steps: Iterable[Step] = None,
        turns: Iterable[Turn] = None,
        ignore_existing_definition: OptBool = None,
        reference_tenor: OptStr = None,
        use_convexity_adjustment: OptBool = None,
        use_multi_dimensional_solver: OptBool = None,
        use_steps: OptBool = None,
        valuation_date: "OptDateTime" = None,
        valuation_time: Optional[ValuationTime] = None,
        ignore_invalid_instrument: OptBool = None,
        use_delayed_data_if_denied: OptBool = None,
        valuation_date_time: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.interest_calculation_method = interest_calculation_method
        self.calendar_adjustment = calendar_adjustment
        self.calendars = try_copy_to_list(calendars)
        self.compounding_type = compounding_type
        self.convexity_adjustment = convexity_adjustment
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.market_data_access_denied_fallback = market_data_access_denied_fallback
        self.pivot_curve_parameters = pivot_curve_parameters
        self.price_side = price_side
        self.reference_curve_parameters = reference_curve_parameters
        self.steps = try_copy_to_list(steps)
        self.turns = try_copy_to_list(turns)
        self.ignore_existing_definition = ignore_existing_definition
        self.reference_tenor = reference_tenor
        self.use_convexity_adjustment = use_convexity_adjustment
        self.use_multi_dimensional_solver = use_multi_dimensional_solver
        self.use_steps = use_steps
        self.valuation_date = valuation_date
        self.valuation_time = valuation_time
        self.ignore_invalid_instrument = ignore_invalid_instrument
        self.use_delayed_data_if_denied = use_delayed_data_if_denied
        self.valuation_date_time = valuation_date_time

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)

    def _get_items(self):
        return [
            enum_param_item.to_kv("calendarAdjustment", self.calendar_adjustment),
            param_item.to_kv("calendars", self.calendars),
            enum_param_item.to_kv("compoundingType", self.compounding_type),
            serializable_param_item.to_kv("convexityAdjustment", self.convexity_adjustment),
            enum_param_item.to_kv("extrapolationMode", self.extrapolation_mode),
            enum_param_item.to_kv("interestCalculationMethod", self.interest_calculation_method),
            enum_param_item.to_kv("interpolationMode", self.interpolation_mode),
            enum_param_item.to_kv("marketDataAccessDeniedFallback", self.market_data_access_denied_fallback),
            serializable_param_item.to_kv("pivotCurveParameters", self.pivot_curve_parameters),
            enum_param_item.to_kv("priceSide", self.price_side),
            serializable_param_item.to_kv("referenceCurveParameters", self.reference_curve_parameters),
            list_serializable_param_item.to_kv("steps", self.steps),
            list_serializable_param_item.to_kv("turns", self.turns),
            param_item.to_kv("referenceTenor", self.reference_tenor),
            param_item.to_kv("useConvexityAdjustment", self.use_convexity_adjustment),
            param_item.to_kv("useMultiDimensionalSolver", self.use_multi_dimensional_solver),
            param_item.to_kv("useSteps", self.use_steps),
            date_param_item.to_kv("valuationDate", self.valuation_date),
            serializable_param_item.to_kv("valuationTime", self.valuation_time),
            param_item.to_kv("ignoreInvalidInstrument", self.ignore_invalid_instrument),
            param_item.to_kv("useDelayedDataIfDenied", self.use_delayed_data_if_denied),
            datetime_param_item.to_kv("valuationDateTime", self.valuation_date_time),
        ]
