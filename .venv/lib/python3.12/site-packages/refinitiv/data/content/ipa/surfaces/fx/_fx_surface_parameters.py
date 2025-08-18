from typing import Optional

from ..._enums import FxVolatilityModel, FxSwapCalculationMethod, PriceSide, TimeStamp, Axis
from ..._models import BidAskMid, InterpolationWeight
from ..._param_item import datetime_param_item, enum_param_item, param_item, serializable_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class FxSurfaceParameters(Serializable):
    """
    This class property contains the properties that may be used to control the
    calculation. It mainly covers dates, market data assumptions (e.g. interpolation),
    and pricing model preferences. Some Parameters are common to all volatility surfaces
    contracts, while others are specific to a particular type of volatility.

    Parameters
    ----------
    atm_volatility_object : BidAskMid, optional

    butterfly10_d_object : BidAskMid, optional

    butterfly25_d_object : BidAskMid, optional

    domestic_deposit_rate_percent_object : BidAskMid, optional

    foreign_deposit_rate_percent_object : BidAskMid, optional

    forward_points_object : BidAskMid, optional

    fx_spot_object : BidAskMid, optional

    fx_swap_calculation_method : FxSwapCalculationMethod, optional
        The method used to calculate an outright price or deposit rates.
        The possible values are:
            FxSwapImpliedFromDeposit: implied FX swap points are computed from deposit
            rates,
            DepositCcy1ImpliedFromFxSwap: the currency 1 deposit rates are computed
            using swap points,
            DepositCcy2ImpliedFromFxSwap: the currency 2 deposit rates are computed
            using swap points.
    implied_volatility_object : BidAskMid, optional

    interpolation_weight : InterpolationWeight, optional

    price_side : PriceSide, optional
        Specifies whether bid, ask, mid or settle is used to build the surface. if not
        precised, default to mid.
    risk_reversal10_d_object : BidAskMid, optional

    risk_reversal25_d_object : BidAskMid, optional

    time_stamp : TimeStamp, optional
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
    volatility_model : VolatilityModel, optional
        The quantitative model used to generate the volatility surface. this may depend
        on the asset class. for fx volatility surface, we currently support the svi
        model.
    x_axis : Axis, optional
        Specifies the unit for the x axis (e.g. date, tenor)
    y_axis : Axis, optional
        Specifies the unit for the y axis (e.g. strike, delta). this may depend on the
        asset class. for fx volatility surface, we support both delta and strike.
    calculation_date : str or date or datetime or timedelta, optional
        The date the volatility surface is generated.
    cutoff_time : str, optional
        The cutoff time
    cutoff_time_zone : str, optional
        The cutoff time zone
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
        fx_swap_calculation_method: Optional[FxSwapCalculationMethod] = None,
        implied_volatility_object: Optional[BidAskMid] = None,
        interpolation_weight: Optional[InterpolationWeight] = None,
        price_side: Optional[PriceSide] = None,
        risk_reversal10_d_object: Optional[BidAskMid] = None,
        risk_reversal25_d_object: Optional[BidAskMid] = None,
        time_stamp: Optional[TimeStamp] = None,
        volatility_model: Optional[FxVolatilityModel] = None,
        x_axis: Optional[Axis] = None,
        y_axis: Optional[Axis] = None,
        calculation_date: "OptDateTime" = None,
        cutoff_time: Optional[str] = None,
        cutoff_time_zone: Optional[str] = None,
    ):
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
        self.price_side = price_side
        self.risk_reversal10_d_object = risk_reversal10_d_object
        self.risk_reversal25_d_object = risk_reversal25_d_object
        self.time_stamp = time_stamp
        self.volatility_model = volatility_model
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.calculation_date = calculation_date
        self.cutoff_time = cutoff_time
        self.cutoff_time_zone = cutoff_time_zone

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
            enum_param_item.to_kv("priceSide", self.price_side),
            serializable_param_item.to_kv("riskReversal10DObject", self.risk_reversal10_d_object),
            serializable_param_item.to_kv("riskReversal25DObject", self.risk_reversal25_d_object),
            enum_param_item.to_kv("timeStamp", self.time_stamp),
            enum_param_item.to_kv("volatilityModel", self.volatility_model),
            enum_param_item.to_kv("xAxis", self.x_axis),
            enum_param_item.to_kv("yAxis", self.y_axis),
            datetime_param_item.to_kv("calculationDate", self.calculation_date),
            param_item.to_kv("cutoffTime", self.cutoff_time),
            param_item.to_kv("cutoffTimeZone", self.cutoff_time_zone),
        ]
