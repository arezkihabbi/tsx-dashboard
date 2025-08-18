from typing import Optional, Union

from ..._enums import PriceSide, FxSwapCalculationMethod, ImpliedDepositDateConvention
from ..._param_item import enum_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    fx_swap_calculation_method : FxSwapCalculationMethod or str, optional
        The method used to calculate an outright price or deposit rates. The possible
        values are. Optional. defaults to 'fxswap'.
    implied_deposit_date_convention : ImpliedDepositDateConvention or str, optional
        An indicator for the "depositccy1impliedfromfxswap",
        "depositccy2impliedfromfxswap" calculation methods, used to check whether dts or
        dtm period is selected for the implied deposits calculation. By default, for the
        implied deposits calculation we use the dts(day to spot) period, while for the
        deposits the dtm(day to money market) period is used.
    price_side : PriceSide or str, optional
        The quoted price side of the instrument. Optional. defaults to 'mid'.
    adjust_all_deposit_points_to_cross_calendars : bool, optional
        An indicator if depositccy1marketdata and depositccy2marketdata are adjusted to
        the cross calendar dates. the possible values are:
        - true: the market data is adjusted according to the cross calendar dates,
        - false: unmodified market data is returned, cross calendar is ignored.
          optional. defaults to 'false'.
    adjust_all_swap_points_to_cross_calendars : bool, optional
        An indicator if fxswapsccy1 and fxswapsccy2 are adjusted to the cross calendar
        dates. the possible values are:
        - true: the market data is adjusted according to the cross calendar dates,
        - false: unmodified market data is returned, cross calendar is ignored.
          optional. defaults to 'false'.
    ignore_ref_ccy_holidays : bool, optional
        An indicator if holidays of the reference currency are included or not in the
        pricing when dates are computed. by default, the reference currency is usd. the
        possible values are:
        - true: holidays are ignored,
        - false: holidays are included in pricing. optional. defaults to 'false'.
    market_data_date : str or date or datetime or timedelta, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    use_direct_quote : bool, optional
        An indicator if the spot and the swap points should be retrieved without a pivot
        currency
        - true: the market data is retrieved directly
        - false: unmodified market data is returned. optional. defaults to 'false'.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing.  Optional. If not set the valuation date is
        equal to market_data_date or Today. For assets that contains a
        settlementConvention, the default valuation date  is equal to the settlementdate
        of the Asset that is usually the TradeDate+SettlementConvention.
    """

    def __init__(
        self,
        fx_swap_calculation_method: Union[FxSwapCalculationMethod, str] = None,
        implied_deposit_date_convention: Union[ImpliedDepositDateConvention, str] = None,
        price_side: Union[PriceSide, str] = None,
        adjust_all_deposit_points_to_cross_calendars: Optional[bool] = None,
        adjust_all_swap_points_to_cross_calendars: Optional[bool] = None,
        ignore_ref_ccy_holidays: Optional[bool] = None,
        market_data_date: OptDateTime = None,
        report_ccy: Optional[str] = None,
        use_direct_quote: Optional[bool] = None,
        valuation_date: OptDateTime = None,
    ) -> None:
        super().__init__()
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_deposit_date_convention = implied_deposit_date_convention
        self.price_side = price_side
        self.adjust_all_deposit_points_to_cross_calendars = adjust_all_deposit_points_to_cross_calendars
        self.adjust_all_swap_points_to_cross_calendars = adjust_all_swap_points_to_cross_calendars
        self.ignore_ref_ccy_holidays = ignore_ref_ccy_holidays
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.use_direct_quote = use_direct_quote
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("fxSwapCalculationMethod", self.fx_swap_calculation_method),
            enum_param_item.to_kv("impliedDepositDateConvention", self.implied_deposit_date_convention),
            enum_param_item.to_kv("priceSide", self.price_side),
            param_item.to_kv(
                "adjustAllDepositPointsToCrossCalendars", self.adjust_all_deposit_points_to_cross_calendars
            ),
            param_item.to_kv("adjustAllSwapPointsToCrossCalendars", self.adjust_all_swap_points_to_cross_calendars),
            param_item.to_kv("ignoreRefCcyHolidays", self.ignore_ref_ccy_holidays),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("useDirectQuote", self.use_direct_quote),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
