from typing import Optional, List, Union

from ..._enums import OptionVolatilityType, PriceSide, PricingModelType, TimeStamp
from ..._models import PayoutScaling
from ..._param_item import (
    param_item,
    enum_param_item,
    list_serializable_param_item,
    serializable_param_item,
    datetime_param_item,
)
from ..._serializable import Serializable
from ....._tools import try_copy_to_list
from ....._types import OptDateTime


class PricingParameters(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------

    option_price_side : PriceSide or str, optional
        The quoted price side of the instrument. Optional. the default values for listed options are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided. the default value for otc options is 'mid'.
    option_time_stamp : TimeStamp, optional
        The mode of the instrument's timestamp selection. Optional.the default value is 'default'.
    payout_custom_dates : string, optional
        The array of dates set by a user for the payout/volatility chart. optional.no
        default value applies.
    payout_scaling_interval : PayoutScaling, optional

    underlying_price_side : PriceSide or str, optional
        The quoted price side of the underlying asset. Optional. the default values are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided.
    underlying_time_stamp : TimeStamp or str, optional
        The mode of the underlying asset's timestamp selection. Optional.the default value is
          'default'.
    volatility_type : OptionVolatilityType or str, optional
        The type of volatility for the option pricing. Optional. the default value is 'implied'.
    market_data_date : str, optional
    compute_payout_chart : bool, optional
        Define whether the payout chart must be computed or not
    compute_volatility_payout : bool, optional
        Define whether the volatility payout chart must be computed or not
    cutoff_time : str, optional
        The cutoff time
    cutoff_time_zone : str, optional
        The cutoff time zone
    market_data_date : str or date or datetime or timedelta, optional
        The date at which the market data is retrieved. the value is expressed in iso
        8601 format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). it
        should be less or equal tovaluationdate). optional. by
        default,marketdatadateisvaluationdateor today.
    market_value_in_deal_ccy : float, optional
        The market value (premium) of the instrument. the value is expressed in the deal
        currency. it is used to define optionprice and compute volatilitypercent. if
        marketvalueindealccy is defined, optionpriceside and volatilitypercent are not
        taken into account; marketvalueindealccy and marketvalueinreportccy cannot be
        overriden at a time. optional. by default, it is equal to optionprice for listed
        options or computed from volatilitypercent for otc options.
    market_value_in_report_ccy : float, optional
        The market value (premium) of the instrument. it is computed as
        [marketvalueindealccy  fxspot]. the value is expressed in the reporting
        currency. it is used to define optionprice and computevolatilitypercent.
        ifmarketvalueinreportccyis defined, optionpriceside and volatilitypercentinputs
        are not taken into account; marketvalueindealccy and marketvalueinreportccy
        cannot be overriden at a time. optional. by default, fxspot rate is retrieved
        from the market data.
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    report_ccy_rate : float, optional
        The rate of the reporting currency against the option currency. it can be used
        to calculate optionprice and marketvalueindealccy if marketvalueinreportccy is
        defined. optional.by default, it is retrieved from the market data.
    risk_free_rate_percent : float, optional
        A risk-free rate of the option currency used for the option pricing. optional.
        by default, the value is retrieved from the market data.
    underlying_price : float, optional
        The price of the underlying asset. the value is expressed in the deal currency.
        if underlyingprice is defined, underlyingpriceside is not taken into account.
        optional. by default, the value is retrieved from the market data.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    volatility_percent : float, optional
        The degree of the underlying asset's price variations over a specified time
        period, used for the option pricing. the value is expressed in percentages. it
        is used to compute marketvalueindealccy.if marketvalueindealccy is defined,
        volatilitypercent is not taken into account. optional. by default, it is
        computed from marketvalueindealccy. if volsurface fails to return a volatility,
        it defaults to '20'.
    """

    def __init__(
        self,
        *,
        valuation_date: "OptDateTime" = None,
        market_data_date: Optional[str] = None,
        report_ccy: Optional[str] = None,
        report_ccy_rate: Optional[float] = None,
        market_value_in_deal_ccy: Optional[float] = None,
        pricing_model_type: Union[PricingModelType, str] = None,
        payout_custom_dates: Optional[List[str]] = None,
        payout_scaling_interval: Optional[PayoutScaling] = None,
        market_value_in_report_ccy: Optional[float] = None,
        volatility_percent: Optional[float] = None,
        risk_free_rate_percent: Optional[float] = None,
        underlying_price: Optional[float] = None,
        volatility_type: Optional[OptionVolatilityType] = None,
        option_price_side: Union[PriceSide, str] = None,
        option_time_stamp: Union[TimeStamp, str] = None,
        underlying_price_side: Union[PriceSide, str] = None,
        underlying_time_stamp: Optional[TimeStamp] = None,
    ) -> None:
        super().__init__()
        self.option_price_side = option_price_side
        self.option_time_stamp = option_time_stamp
        self.payout_custom_dates = try_copy_to_list(payout_custom_dates)
        self.payout_scaling_interval = payout_scaling_interval
        self.pricing_model_type = pricing_model_type
        self.underlying_price_side = underlying_price_side
        self.underlying_time_stamp = underlying_time_stamp
        self.volatility_type = volatility_type
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.market_value_in_report_ccy = market_value_in_report_ccy
        self.report_ccy = report_ccy
        self.report_ccy_rate = report_ccy_rate
        self.risk_free_rate_percent = risk_free_rate_percent
        self.underlying_price = underlying_price
        self.valuation_date = valuation_date
        self.volatility_percent = volatility_percent

    def _get_items(self):
        return [
            enum_param_item.to_kv("optionPriceSide", self.option_price_side),
            enum_param_item.to_kv("optionTimeStamp", self.option_time_stamp),
            list_serializable_param_item.to_kv("payoutCustomDates", self.payout_custom_dates),
            serializable_param_item.to_kv("payoutScalingInterval", self.payout_scaling_interval),
            enum_param_item.to_kv("pricingModelType", self.pricing_model_type),
            enum_param_item.to_kv("underlyingPriceSide", self.underlying_price_side),
            enum_param_item.to_kv("underlyingTimeStamp", self.underlying_time_stamp),
            enum_param_item.to_kv("volatilityType", self.volatility_type),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("marketValueInReportCcy", self.market_value_in_report_ccy),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("reportCcyRate", self.report_ccy_rate),
            param_item.to_kv("riskFreeRatePercent", self.risk_free_rate_percent),
            param_item.to_kv("underlyingPrice", self.underlying_price),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
            param_item.to_kv("volatilityPercent", self.volatility_percent),
        ]
