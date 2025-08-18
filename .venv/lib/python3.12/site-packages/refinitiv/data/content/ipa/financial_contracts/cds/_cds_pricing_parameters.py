from typing import Optional

from ..._param_item import param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    cash_amount_in_deal_ccy : float, optional
        cash_amount_in_deal_ccy to override and that will be used as pricing analysis
        input to compute the cds other outputs. Optional. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    clean_price_percent : float, optional
        clean_price_percent to override and that will be used as pricing analysis input
        to compute the cds other outputs. Optional. No override is applied by default.
        Note that only one pricing analysis input should be defined.
    conventional_spread_bp : float, optional
        conventional_spread_bp to override and that will be used as pricing analysis
        input to compute the cds other outputs. Optional. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    market_data_date : str or date or datetime or timedelta, optional
        The market data date for pricing. Optional. By default, the market_data_date
        date is the valuation_date or Today
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    upfront_amount_in_deal_ccy : float, optional
        upfront_amount_in_deal_ccy to override and that will be used as pricing analysis
        input to compute the cds other outputs. Optional. No override is applied by
        default. Note that only one pricing analysis input should be defined.
    upfront_percent : float, optional
        upfront_percent to override and that will be used as pricing analysis input to
        compute the cds other outputs. Optional. No override is applied by default. Note
        that only one pricing analysis input should be defined.
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing.  Optional. If not set the valuation date is
        equal to market_data_date or Today. For assets that contains a
        settlementConvention, the default valuation date  is equal to the settlementdate
        of the Asset that is usually the TradeDate+SettlementConvention.
    """

    def __init__(
        self,
        cash_amount_in_deal_ccy: Optional[float] = None,
        clean_price_percent: Optional[float] = None,
        conventional_spread_bp: Optional[float] = None,
        market_data_date: OptDateTime = None,
        report_ccy: Optional[str] = None,
        upfront_amount_in_deal_ccy: Optional[float] = None,
        upfront_percent: Optional[float] = None,
        valuation_date: OptDateTime = None,
    ) -> None:
        super().__init__()
        self.cash_amount_in_deal_ccy = cash_amount_in_deal_ccy
        self.clean_price_percent = clean_price_percent
        self.conventional_spread_bp = conventional_spread_bp
        self.market_data_date = market_data_date
        self.report_ccy = report_ccy
        self.upfront_amount_in_deal_ccy = upfront_amount_in_deal_ccy
        self.upfront_percent = upfront_percent
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            param_item.to_kv("cashAmountInDealCcy", self.cash_amount_in_deal_ccy),
            param_item.to_kv("cleanPricePercent", self.clean_price_percent),
            param_item.to_kv("conventionalSpreadBp", self.conventional_spread_bp),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("upfrontAmountInDealCcy", self.upfront_amount_in_deal_ccy),
            param_item.to_kv("upfrontPercent", self.upfront_percent),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
