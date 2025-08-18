from typing import Optional, Union

from ..._enums import (
    IndexConvexityAdjustmentIntegrationMethod,
    IndexConvexityAdjustmentMethod,
    PriceSide,
    TenorReferenceDate,
)
from ..._param_item import enum_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    index_convexity_adjustment_integration_method : IndexConvexityAdjustmentIntegrationMethod or str, optional
        The integration method used for static replication method. the possible values
        are: riemannsum, rungekutta. the default value is 'riemannsum'.
    index_convexity_adjustment_method : IndexConvexityAdjustmentMethod or str, optional
        The convexity adjustment type for constant maturity swaps (cms) and libor
        in-arrears swaps. the possible values are: none, blackscholes, linearswapmodel,
        replication. the default value is 'blackscholes'.
    price_side : PriceSide or str, optional
        The quoted price side of the instrument. optional. default value is 'mid'.
    tenor_reference_date : TenorReferenceDate or str, optional
        In case the swap definition uses 'starttenor', 'starttenor' defines whether the
        swap start date is calculated from valuation date or from spot date
    discounting_ccy : str, optional
        The currency code, which defines the choice of the discounting curve. the value
        is expressed in iso 4217 alphabetical format (e.g. 'usd'). by default,
        settlementccy or the paid leg currency is used.
    discounting_tenor : str, optional

    market_data_date : str or date or datetime or timedelta, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The dirty market value of the instrument computed as
        [cleanmarketvalueindealccy+accruedamountindealccy]. the value is expressed in
        the deal currency. the default value is '0'.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    use_legs_signing : bool, optional
        Enable the signing of "risk measures" and "valuation" outputs based on leg's
        direction the default value is false.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    """

    def __init__(
        self,
        index_convexity_adjustment_integration_method: Union[IndexConvexityAdjustmentIntegrationMethod, str] = None,
        index_convexity_adjustment_method: Union[IndexConvexityAdjustmentMethod, str] = None,
        price_side: Union[PriceSide, str] = None,
        tenor_reference_date: Union[TenorReferenceDate, str] = None,
        discounting_ccy: Optional[str] = None,
        discounting_tenor: Optional[str] = None,
        market_data_date: "OptDateTime" = None,
        market_value_in_deal_ccy: Optional[float] = None,
        report_ccy: Optional[str] = None,
        use_legs_signing: Optional[bool] = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.index_convexity_adjustment_integration_method = index_convexity_adjustment_integration_method
        self.index_convexity_adjustment_method = index_convexity_adjustment_method
        self.price_side = price_side
        self.tenor_reference_date = tenor_reference_date
        self.discounting_ccy = discounting_ccy
        self.discounting_tenor = discounting_tenor
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.report_ccy = report_ccy
        self.use_legs_signing = use_legs_signing
        self.valuation_date = valuation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv(
                "indexConvexityAdjustmentIntegrationMethod", self.index_convexity_adjustment_integration_method
            ),
            enum_param_item.to_kv("indexConvexityAdjustmentMethod", self.index_convexity_adjustment_method),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("tenorReferenceDate", self.tenor_reference_date),
            param_item.to_kv("discountingCcy", self.discounting_ccy),
            param_item.to_kv("discountingTenor", self.discounting_tenor),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("useLegsSigning", self.use_legs_signing),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
        ]
