from typing import Optional, TYPE_CHECKING

from ._maturity_filter import MaturityFilter
from ._strike_filter_range import StrikeFilterRange
from ..._param_item import param_item, serializable_param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptBool, OptInt, OptFloat


class SurfaceFilters(Serializable):
    """
    Filter object for surface.

    Parameters
    ----------
    maturity_filter_range : MaturityFilter, optional
        The object allows to specify the range of expiry periods of options that are
        used to construct the surface.
    strike_range : StrikeFilterRange, optional
        The range allows to exclude strike levels that have implied volatilities which
        exceed upper bound or below lower bound.
    strike_range_percent : DEPRECATED
        This attribute doesn't use anymore.
    atm_tolerance_interval_percent : float, optional
        Filter on the atm tolerance interval percent
    ensure_prices_monotonicity : bool, optional
        Filter on the monotonicity of price options.
    max_of_median_bid_ask_spread : float, optional
        Spread mutltiplier to filter the options with the same expiry
    max_staleness_days : int, optional
        Max staleness past days to use for building the surface
    use_only_calls : bool, optional
        Select only teh calls to build the surface
    use_only_puts : bool, optional
        Select only the puts to build the surface
    use_weekly_options : bool, optional
        Filter on the weekly options.
    include_min_tick_prices : bool, optional
        Take into account the minimum tick prices to build the surface
    """

    def __init__(
        self,
        maturity_filter_range: Optional[MaturityFilter] = None,
        strike_range: Optional[StrikeFilterRange] = None,
        strike_range_percent=None,
        atm_tolerance_interval_percent: "OptFloat" = None,
        ensure_prices_monotonicity: "OptBool" = None,
        max_of_median_bid_ask_spread: "OptFloat" = None,
        max_staleness_days: "OptInt" = None,
        use_only_calls: "OptBool" = None,
        use_only_puts: "OptBool" = None,
        use_weekly_options: "OptBool" = None,
        include_min_tick_prices: "OptBool" = None,
    ):
        super().__init__()
        self.maturity_filter_range = maturity_filter_range
        self.strike_range = strike_range
        self.strike_range_percent = strike_range_percent
        self.atm_tolerance_interval_percent = atm_tolerance_interval_percent
        self.ensure_prices_monotonicity = ensure_prices_monotonicity
        self.max_of_median_bid_ask_spread = max_of_median_bid_ask_spread
        self.max_staleness_days = max_staleness_days
        self.use_only_calls = use_only_calls
        self.use_only_puts = use_only_puts
        self.use_weekly_options = use_weekly_options
        self.include_min_tick_prices = include_min_tick_prices

    def _get_items(self):
        return [
            serializable_param_item.to_kv("maturityFilterRange", self.maturity_filter_range),
            serializable_param_item.to_kv("strikeRange", self.strike_range),
            param_item.to_kv("atmToleranceIntervalPercent", self.atm_tolerance_interval_percent),
            param_item.to_kv("ensurePricesMonotonicity", self.ensure_prices_monotonicity),
            param_item.to_kv("maxOfMedianBidAskSpread", self.max_of_median_bid_ask_spread),
            param_item.to_kv("maxStalenessDays", self.max_staleness_days),
            param_item.to_kv("useOnlyCalls", self.use_only_calls),
            param_item.to_kv("useOnlyPuts", self.use_only_puts),
            param_item.to_kv("useWeeklyOptions", self.use_weekly_options),
            param_item.to_kv("includeMinTickPrices", self.include_min_tick_prices),
        ]
