from typing import Optional, Iterable

from ._step import Step
from ._turn import Turn
from .._enums import (
    CalendarAdjustment,
    CompoundingType,
    MarketDataAccessDeniedFallback,
    SwapPriceSide,
    ZcInterpolationMode,
)
from .._models import ConvexityAdjustment
from ..._enums import DayCountBasis
from ..._enums._extrapolation_mode import ExtrapolationMode
from ..._param_item import enum_param_item, param_item, serializable_param_item
from ..._serializable import Serializable
from ....._types import OptStr, OptBool


class InterestRateCurveParameters(Serializable):
    """
    Parameters
    ----------
    interest_calculation_method : InterestCalculationMethod, optional
        Day count basis of the calculated zero coupon rates
    calendar_adjustment : CalendarAdjustment, optional
        Cash flow adjustment according to a calendar.
        - No: for analytic pricing (i.e. from the bond structure)
        - Null: for cash flow pricing using the calendar NULL
        - Weekend: for cash flow pricing using the calendar Weekend
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
        - Hermite: Hermite (Bessel) interpolation
        - AkimaMethod: the Akima method
            (a smoother variant of local cubic interpolation)
        - FritschButlandMethod: the Fritsch-Butland method (a monotonic cubic variant)
        - KrugerMethod: the Kruger method (a monotonic cubic variant)
        - MonotonicCubicNaturalSpline: a monotonic natural cubic spline
        - MonotonicHermiteCubic: monotonic Hermite (Bessel) cubic interpolation
        - TensionSpline: a tension spline
    market_data_access_denied_fallback : MarketDataAccessDeniedFallback, optional
        - ReturnError: dont price the surface and return an error (Default value)
        - IgnoreConstituents: price the surface without the error market data
        - UseDelayedData: use delayed Market Data if possible
    price_side : SwapPriceSide, optional
        Price side of the instrument to be used. Default value is: Mid
    steps : Step, optional

    turns : Turn, optional
        Used to include end period rates/turns when calculating swap rate surfaces
    reference_tenor : str, optional
        Root tenor(s) for the xIbor dependencies
    use_convexity_adjustment : bool, optional

    use_multi_dimensional_solver : bool, optional
        Specifies the use of the multi-dimensional solver for yield curve bootstrapping.
        This solving method is required because the bootstrapping method
        sometimes creates a ZC curve which does not accurately reprice the input
        instruments used to build it.
        The multi-dimensional solver is recommended when cubic interpolation methods
        are used in building the curve (in other cases, performance might be inferior
        to the regular bootstrapping method). When use for Credit Curve it is only
        used when the calibrationModel is set to Bootstrap.
        - true: to use multi-dimensional solver for yield curve bootstrapping
        - false: not to use multi-dimensional solver for yield curve bootstrapping
    use_steps : bool, optional

    """

    def __init__(
        self,
        interest_calculation_method: Optional[DayCountBasis] = None,
        calendar_adjustment: Optional[CalendarAdjustment] = None,
        calendars: OptStr = None,
        compounding_type: Optional[CompoundingType] = None,
        convexity_adjustment: Optional[ConvexityAdjustment] = None,
        extrapolation_mode: Optional[ExtrapolationMode] = None,
        interpolation_mode: Optional[ZcInterpolationMode] = None,
        market_data_access_denied_fallback: Optional[MarketDataAccessDeniedFallback] = None,
        price_side: Optional[SwapPriceSide] = None,
        steps: Iterable[Step] = None,
        turns: Iterable[Turn] = None,
        reference_tenor: OptStr = None,
        use_convexity_adjustment: OptBool = None,
        use_multi_dimensional_solver: OptBool = None,
        use_steps: OptBool = None,
    ) -> None:
        super().__init__()
        self.interest_calculation_method = interest_calculation_method
        self.calendar_adjustment = calendar_adjustment
        self.calendars = calendars
        self.compounding_type = compounding_type
        self.convexity_adjustment = convexity_adjustment
        self.extrapolation_mode = extrapolation_mode
        self.interpolation_mode = interpolation_mode
        self.market_data_access_denied_fallback = market_data_access_denied_fallback
        self.price_side = price_side
        self.steps = steps
        self.turns = turns
        self.reference_tenor = reference_tenor
        self.use_convexity_adjustment = use_convexity_adjustment
        self.use_multi_dimensional_solver = use_multi_dimensional_solver
        self.use_steps = use_steps

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
            enum_param_item.to_kv("priceSide", self.price_side),
            param_item.to_kv("steps", self.steps),
            param_item.to_kv("turns", self.turns),
            param_item.to_kv("useConvexityAdjustment", self.use_convexity_adjustment),
            param_item.to_kv("useMultiDimensionalSolver", self.use_multi_dimensional_solver),
            param_item.to_kv("referenceTenor", self.reference_tenor),
            param_item.to_kv("useSteps", self.use_steps),
        ]
