from typing import Optional, Union

from ..._enums import IndexConvexityAdjustmentIntegrationMethod, IndexConvexityAdjustmentMethod, PriceSide
from ..._param_item import enum_param_item, datetime_param_item, param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    index_convexity_adjustment_integration_method : IndexConvexityAdjustmentIntegrationMethod, optional

    index_convexity_adjustment_method : IndexConvexityAdjustmentMethod, optional

    price_side : PriceSide or str, optional
        The quoted price side of the instrument. optional. default value is 'mid'.
    market_data_date : str or date or datetime or timedelta, optional
        The market data date for pricing. Optional. By default, the marketDataDate date
        is the ValuationDate or Today
    market_value_in_deal_ccy : float, optional
        MarketValueInDealCcy to override and that will be used as pricing analysis input
        to compute VolatilityPercent. Optional. No override is applied by default. Note
        that Premium takes priority over Volatility input.
    report_ccy : str, optional
        Valuation is performed in deal currency. If a report currency is set, valuation
        is done in that report currency.
    skip_first_cap_floorlet : bool, optional
        Indicates whether to take in consideration the first caplet
    valuation_date : str or date or datetime or timedelta, optional
        The valuation date for pricing.  Optional. If not set the valuation date is
        equal to MarketDataDate or Today. For assets that contains a
        settlementConvention, the default valuation date  is equal to the settlementdate
        of the Asset that is usually the TradeDate+SettlementConvention.
    implied_volatility_bp : float, optional
        User defined implied normal volatility, expressed in basis points.
    implied_volatility_percent : float, optional
        User defined implied lognormal volatility, expressed in percent.
    """

    def __init__(
        self,
        index_convexity_adjustment_integration_method: Optional[IndexConvexityAdjustmentIntegrationMethod] = None,
        index_convexity_adjustment_method: Optional[IndexConvexityAdjustmentMethod] = None,
        price_side: Union[PriceSide, str] = None,
        market_data_date: OptDateTime = None,
        market_value_in_deal_ccy: Optional[float] = None,
        report_ccy: Optional[str] = None,
        skip_first_cap_floorlet: Optional[bool] = None,
        valuation_date: OptDateTime = None,
        implied_volatility_bp: Optional[float] = None,
        implied_volatility_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.index_convexity_adjustment_integration_method = index_convexity_adjustment_integration_method
        self.index_convexity_adjustment_method = index_convexity_adjustment_method
        self.price_side = price_side
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.report_ccy = report_ccy
        self.skip_first_cap_floorlet = skip_first_cap_floorlet
        self.valuation_date = valuation_date
        self.implied_volatility_bp = implied_volatility_bp
        self.implied_volatility_percent = implied_volatility_percent

    def _get_items(self):
        return [
            enum_param_item.to_kv(
                "indexConvexityAdjustmentIntegrationMethod", self.index_convexity_adjustment_integration_method
            ),
            enum_param_item.to_kv("indexConvexityAdjustmentMethod", self.index_convexity_adjustment_method),
            enum_param_item.to_kv("priceSide", self.price_side),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("skipFirstCapFloorlet", self.skip_first_cap_floorlet),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
            param_item.to_kv("impliedVolatilityBp", self.implied_volatility_bp),
            param_item.to_kv("impliedVolatilityPercent", self.implied_volatility_percent),
        ]
