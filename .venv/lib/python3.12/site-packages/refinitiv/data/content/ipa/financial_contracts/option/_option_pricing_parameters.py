from typing import Optional, List, Union

from ..._enums import (
    FxSwapCalculationMethod,
    OptionVolatilityType,
    PriceSide,
    PricingModelType,
    TimeStamp,
    VolatilityModel,
)
from ..._models import BidAskMid, InterpolationWeight, PayoutScaling
from ..._param_item import (
    param_item,
    datetime_param_item,
    serializable_param_item,
    enum_param_item,
    list_serializable_param_item,
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
    atm_volatility_object : BidAskMid, optional

    butterfly10_d_object : BidAskMid, optional

    butterfly25_d_object : BidAskMid, optional

    domestic_deposit_rate_percent_object : BidAskMid, optional

    foreign_deposit_rate_percent_object : BidAskMid, optional

    forward_points_object : BidAskMid, optional

    fx_spot_object : BidAskMid, optional

    fx_swap_calculation_method : FxSwapCalculationMethod or str, optional
        The method used to calculate an outright price or deposit rates.
    implied_volatility_object : BidAskMid, optional

    interpolation_weight : InterpolationWeight, optional

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

    price_side : PriceSide, optional
        The quoted price side of the instrument.
    pricing_model_type : PricingModelType, optional
        The model type of the option pricing. Optional. the default value depends on the option type.
    risk_reversal10_d_object : BidAskMid, optional

    risk_reversal25_d_object : BidAskMid, optional

    underlying_price_side : PriceSide or str, optional
        The quoted price side of the underlying asset. Optional. the default values are:
        - ask: if buysell is set to 'buy',
        - bid: if buysell is set to 'sell',
        - last: if buysell is not provided.
    underlying_time_stamp : TimeStamp or str, optional
        The mode of the underlying asset's timestamp selection. Optional.the default value is
          'default'.
    volatility_model : VolatilityModel, optional
        The model used to build the volatility surface. the possible values are:
        - sabr,
        - cubicspline,
        - svi,
        - twinlognormal,
        - vannavolga10d,
        - vannavolga25d.
    volatility_type : OptionVolatilityType or str, optional
        The type of volatility for the option pricing. Optional. the default value is 'implied'.
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
    simulate_exercise : bool, optional
        Tells if payoff-linked cashflow should be returned. possible values:
        - true
        - false
    underlying_price : float, optional
        The price of the underlying asset. the value is expressed in the deal currency.
        if underlyingprice is defined, underlyingpriceside is not taken into account.
        optional. by default, the value is retrieved from the market data.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    volatility : float, optional
        Volatility(without unity) to override and that will be used as pricing analysis
        input to compute marketvalueindealccy. introduced due to bachelier model, for
        more details please have a look at apqps-13558 optional. no override is applied
        by default. note that if premium is defined, volatility is not taken into
        account.
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
        atm_volatility_object: Optional[BidAskMid] = None,
        butterfly10_d_object: Optional[BidAskMid] = None,
        butterfly25_d_object: Optional[BidAskMid] = None,
        domestic_deposit_rate_percent_object: Optional[BidAskMid] = None,
        foreign_deposit_rate_percent_object: Optional[BidAskMid] = None,
        forward_points_object: Optional[BidAskMid] = None,
        fx_spot_object: Optional[BidAskMid] = None,
        fx_swap_calculation_method: Union[FxSwapCalculationMethod, str] = None,
        implied_volatility_object: Optional[BidAskMid] = None,
        interpolation_weight: Optional[InterpolationWeight] = None,
        option_price_side: Union[PriceSide, str] = None,
        option_time_stamp: Union[TimeStamp, str] = None,
        payout_custom_dates: Optional[List[str]] = None,
        payout_scaling_interval: Optional[PayoutScaling] = None,
        price_side: Union[PriceSide, str] = None,
        pricing_model_type: Union[PricingModelType, str] = None,
        risk_reversal10_d_object: Optional[BidAskMid] = None,
        risk_reversal25_d_object: Optional[BidAskMid] = None,
        underlying_price_side: Union[PriceSide, str] = None,
        underlying_time_stamp: Optional[TimeStamp] = None,
        volatility_model: Union[VolatilityModel, str] = None,
        volatility_type: Optional[OptionVolatilityType] = None,
        compute_payout_chart: Optional[bool] = None,
        compute_volatility_payout: Optional[bool] = None,
        cutoff_time: Optional[str] = None,
        cutoff_time_zone: Optional[str] = None,
        market_data_date: "OptDateTime" = None,
        market_value_in_deal_ccy: Optional[float] = None,
        market_value_in_report_ccy: Optional[float] = None,
        report_ccy: Optional[str] = None,
        report_ccy_rate: Optional[float] = None,
        risk_free_rate_percent: Optional[float] = None,
        simulate_exercise: Optional[bool] = None,
        underlying_price: Optional[float] = None,
        valuation_date: "OptDateTime" = None,
        volatility: Optional[float] = None,
        volatility_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.atm_volatility_object = atm_volatility_object
        self.butterfly10_d_object = butterfly10_d_object
        self.butterfly25_d_object = butterfly25_d_object
        self.domestic_deposit_rate_percent_object = domestic_deposit_rate_percent_object
        self.foreign_deposit_rate_percent_object = foreign_deposit_rate_percent_object
        self.forward_points_object = forward_points_object
        self.fx_spot_object = fx_spot_object
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_volatility_object = implied_volatility_object
        self.interpolation_weight = interpolation_weight
        self.option_price_side = option_price_side
        self.option_time_stamp = option_time_stamp
        self.payout_custom_dates = try_copy_to_list(payout_custom_dates)
        self.payout_scaling_interval = payout_scaling_interval
        self.price_side = price_side
        self.pricing_model_type = pricing_model_type
        self.risk_reversal10_d_object = risk_reversal10_d_object
        self.risk_reversal25_d_object = risk_reversal25_d_object
        self.underlying_price_side = underlying_price_side
        self.underlying_time_stamp = underlying_time_stamp
        self.volatility_model = volatility_model
        self.volatility_type = volatility_type
        self.compute_payout_chart = compute_payout_chart
        self.compute_volatility_payout = compute_volatility_payout
        self.cutoff_time = cutoff_time
        self.cutoff_time_zone = cutoff_time_zone
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.market_value_in_report_ccy = market_value_in_report_ccy
        self.report_ccy = report_ccy
        self.report_ccy_rate = report_ccy_rate
        self.risk_free_rate_percent = risk_free_rate_percent
        self.simulate_exercise = simulate_exercise
        self.underlying_price = underlying_price
        self.valuation_date = valuation_date
        self.volatility = volatility
        self.volatility_percent = volatility_percent

    def _get_items(self):
        return [
            serializable_param_item.to_kv("atmVolatilityObject", self.atm_volatility_object),
            serializable_param_item.to_kv("butterfly10DObject", self.butterfly10_d_object),
            serializable_param_item.to_kv("butterfly25DObject", self.butterfly25_d_object),
            serializable_param_item.to_kv(
                "domesticDepositRatePercentObject", self.domestic_deposit_rate_percent_object
            ),
            serializable_param_item.to_kv("foreignDepositRatePercentObject", self.foreign_deposit_rate_percent_object),
            serializable_param_item.to_kv("forwardPointsObject", self.forward_points_object),
            serializable_param_item.to_kv("fxSpotObject", self.fx_spot_object),
            enum_param_item.to_kv("fxSwapCalculationMethod", self.fx_swap_calculation_method),
            serializable_param_item.to_kv("impliedVolatilityObject", self.implied_volatility_object),
            serializable_param_item.to_kv("interpolationWeight", self.interpolation_weight),
            enum_param_item.to_kv("optionPriceSide", self.option_price_side),
            enum_param_item.to_kv("optionTimeStamp", self.option_time_stamp),
            list_serializable_param_item.to_kv("payoutCustomDates", self.payout_custom_dates),
            serializable_param_item.to_kv("payoutScalingInterval", self.payout_scaling_interval),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("pricingModelType", self.pricing_model_type),
            serializable_param_item.to_kv("riskReversal10DObject", self.risk_reversal10_d_object),
            serializable_param_item.to_kv("riskReversal25DObject", self.risk_reversal25_d_object),
            enum_param_item.to_kv("underlyingPriceSide", self.underlying_price_side),
            enum_param_item.to_kv("underlyingTimeStamp", self.underlying_time_stamp),
            enum_param_item.to_kv("volatilityModel", self.volatility_model),
            enum_param_item.to_kv("volatilityType", self.volatility_type),
            param_item.to_kv("computePayoutChart", self.compute_payout_chart),
            param_item.to_kv("computeVolatilityPayout", self.compute_volatility_payout),
            param_item.to_kv("cutoffTime", self.cutoff_time),
            param_item.to_kv("cutoffTimeZone", self.cutoff_time_zone),
            datetime_param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            param_item.to_kv("marketValueInReportCcy", self.market_value_in_report_ccy),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("reportCcyRate", self.report_ccy_rate),
            param_item.to_kv("riskFreeRatePercent", self.risk_free_rate_percent),
            param_item.to_kv("simulateExercise", self.simulate_exercise),
            param_item.to_kv("underlyingPrice", self.underlying_price),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
            param_item.to_kv("volatility", self.volatility),
            param_item.to_kv("volatilityPercent", self.volatility_percent),
        ]
