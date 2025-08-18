from typing import Optional, Union

from ..._enums import FxSwapCalculationMethod, PriceSide, PricingModelType, VolatilityModel
from ..._models import BidAskMid
from ..._param_item import param_item, enum_param_item, serializable_param_item
from ..._serializable import Serializable


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

    price_side : PriceSide, optional
        The quoted price side of the instrument.
    pricing_model_type : PricingModelType, optional
        The model type of the option pricing. Optional. the default value depends on the option type.
    risk_reversal10_d_object : BidAskMid, optional

    risk_reversal25_d_object : BidAskMid, optional

    volatility_model : VolatilityModel, optional
        The model used to build the volatility surface. the possible values are:
        - sabr,
        - cubicspline,
        - svi,
        - twinlognormal,
        - vannavolga10d,
        - vannavolga25d.
    cutoff_time : str, optional
        The cutoff time
    cutoff_time_zone : str, optional
        The cutoff time zone
    market_data_date : str, optional
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
    report_ccy : str, optional
        The reporting currency code, expressed in iso 4217 alphabetical format (e.g.,
        'usd'). it is set for the fields ending with 'xxxinreportccy'. optional. the
        default value is the notional currency.
    report_ccy_rate : float, optional
        The rate of the reporting currency against the option currency. it can be used
        to calculate optionprice and marketvalueindealccy if marketvalueinreportccy is
        defined. optional.by default, it is retrieved from the market data.
    simulate_exercise : bool, optional
        Tells if payoff-linked cashflow should be returned. possible values:
        - true
        - false
    valuation_date : str, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    """

    def __init__(
        self,
        atm_volatility_object: Optional[BidAskMid] = None,
        butterfly10_d_object: Optional[BidAskMid] = None,
        butterfly25_d_object: Optional[BidAskMid] = None,
        cutoff_time: Optional[str] = None,
        cutoff_time_zone: Optional[str] = None,
        domestic_deposit_rate_percent_object: Optional[BidAskMid] = None,
        foreign_deposit_rate_percent_object: Optional[BidAskMid] = None,
        forward_points_object: Optional[BidAskMid] = None,
        fx_spot_object: Optional[BidAskMid] = None,
        fx_swap_calculation_method: Union[FxSwapCalculationMethod, str] = None,
        implied_volatility_object: Optional[BidAskMid] = None,
        market_data_date: Optional[str] = None,
        market_value_in_deal_ccy: Optional[float] = None,
        price_side: Union[PriceSide, str] = None,
        pricing_model_type: Union[PricingModelType, str] = None,
        report_ccy: Optional[str] = None,
        report_ccy_rate: Optional[float] = None,
        risk_reversal10_d_object: Optional[BidAskMid] = None,
        risk_reversal25_d_object: Optional[BidAskMid] = None,
        simulate_exercise: Optional[bool] = None,
        valuation_date: Optional[str] = None,
        volatility_model: Union[VolatilityModel, str] = None,
    ) -> None:
        super().__init__()
        self.atm_volatility_object = atm_volatility_object
        self.butterfly10_d_object = butterfly10_d_object
        self.butterfly25_d_object = butterfly25_d_object
        self.cutoff_time = cutoff_time
        self.cutoff_time_zone = cutoff_time_zone
        self.domestic_deposit_rate_percent_object = domestic_deposit_rate_percent_object
        self.foreign_deposit_rate_percent_object = foreign_deposit_rate_percent_object
        self.forward_points_object = forward_points_object
        self.fx_spot_object = fx_spot_object
        self.fx_swap_calculation_method = fx_swap_calculation_method
        self.implied_volatility_object = implied_volatility_object
        self.market_data_date = market_data_date
        self.market_value_in_deal_ccy = market_value_in_deal_ccy
        self.price_side = price_side
        self.pricing_model_type = pricing_model_type
        self.report_ccy = report_ccy
        self.report_ccy_rate = report_ccy_rate
        self.risk_reversal10_d_object = risk_reversal10_d_object
        self.risk_reversal25_d_object = risk_reversal25_d_object
        self.simulate_exercise = simulate_exercise
        self.valuation_date = valuation_date
        self.volatility_model = volatility_model

    def _get_items(self):
        return [
            serializable_param_item.to_kv("atmVolatilityObject", self.atm_volatility_object),
            serializable_param_item.to_kv("butterfly10DObject", self.butterfly10_d_object),
            serializable_param_item.to_kv("butterfly25DObject", self.butterfly25_d_object),
            param_item.to_kv("cutoffTime", self.cutoff_time),
            param_item.to_kv("cutoffTimeZone", self.cutoff_time_zone),
            serializable_param_item.to_kv(
                "domesticDepositRatePercentObject", self.domestic_deposit_rate_percent_object
            ),
            serializable_param_item.to_kv("foreignDepositRatePercentObject", self.foreign_deposit_rate_percent_object),
            serializable_param_item.to_kv("forwardPointsObject", self.forward_points_object),
            serializable_param_item.to_kv("fxSpotObject", self.fx_spot_object),
            enum_param_item.to_kv("fxSwapCalculationMethod", self.fx_swap_calculation_method),
            serializable_param_item.to_kv("impliedVolatilityObject", self.implied_volatility_object),
            param_item.to_kv("marketDataDate", self.market_data_date),
            param_item.to_kv("marketValueInDealCcy", self.market_value_in_deal_ccy),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("pricingModelType", self.pricing_model_type),
            param_item.to_kv("reportCcy", self.report_ccy),
            param_item.to_kv("reportCcyRate", self.report_ccy_rate),
            serializable_param_item.to_kv("riskReversal10DObject", self.risk_reversal10_d_object),
            serializable_param_item.to_kv("riskReversal25DObject", self.risk_reversal25_d_object),
            param_item.to_kv("simulateExercise", self.simulate_exercise),
            param_item.to_kv("valuationDate", self.valuation_date),
            enum_param_item.to_kv("volatilityModel", self.volatility_model),
        ]
