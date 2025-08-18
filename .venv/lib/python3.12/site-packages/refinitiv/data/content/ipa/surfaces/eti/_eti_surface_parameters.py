from typing import Optional, TYPE_CHECKING, Iterable

from .._enums import MoneynessType
from .._models import MoneynessWeight, SurfaceFilters
from ..._enums import Axis, EtiInputVolatilityType, PriceSide, TimeStamp, VolatilityModel
from ..._param_item import (
    datetime_param_item,
    enum_param_item,
    param_item,
    serializable_param_item,
    list_serializable_param_item,
)
from ..._serializable import Serializable
from ....._tools import try_copy_to_list

if TYPE_CHECKING:
    from ....._types import OptBool, OptDateTime


class EtiSurfaceParameters(Serializable):
    """
    This class property contains the properties that may be used to control the
    calculation. It mainly covers dates, market data assumptions (e.g. interpolation),
    and pricing model preferences. Some Parameters are common to all volatility surfaces
    contracts, while others are specific to a particular type of volatility.

    Parameters
    ----------
    filters : SurfaceFilters, optional
        The parameters of options that should be used to construct the
        volatility surface.
    input_volatility_type : InputVolatilityType, optional
        Specifies the type of volatility used as an input of the model (calculated
        implied volatility, settlement)
        - settle: [deprecated] the service uses the settlement volatility to build the
          volatility surface
        - quoted: the service uses the quoted volatility to build the volatility surface
        - implied: the service internally calculates implied volatilities for the option
          universe before building the surface default value is "implied".
    moneyness_type : MoneynessType, optional
        The enumerate that specifies the moneyness type to use for calibration.
        - spot
        - fwd
        - sigma optional. default value is "spot".
    price_side : PriceSide, optional
        Specifies whether bid, ask or mid is used to build the surface.
    time_stamp : TimeStamp, optional
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
    volatility_model : VolatilityModel, optional
        The quantitative model used to generate the volatility surface. this may depend
        on the asset class.
    weights : MoneynessWeight, optional
        The list of calibration weights that should be applied to different
        MoneynessWeight.
    x_axis : Axis, optional
        Specifies the unit for the x axis (e.g. date, tenor)
    y_axis : Axis, optional
        Specifies the unit for the y axis (e.g. strike, delta). this may depend on the
        asset class. for fx volatility surface, we support both delta and strike.
    calculation_date : str or date or datetime or timedelta, optional
        The date the volatility surface is generated.
    svi_alpha_extrapolation : bool, optional
        Svi alpha extrapolation for building the surface default value : true
    """

    def __init__(
        self,
        filters: Optional[SurfaceFilters] = None,
        input_volatility_type: Optional[EtiInputVolatilityType] = None,
        moneyness_type: Optional[MoneynessType] = None,
        price_side: Optional[PriceSide] = None,
        time_stamp: Optional[TimeStamp] = None,
        volatility_model: Optional[VolatilityModel] = None,
        weights: Optional[Iterable[MoneynessWeight]] = None,
        x_axis: Optional[Axis] = None,
        y_axis: Optional[Axis] = None,
        calculation_date: "OptDateTime" = None,
        svi_alpha_extrapolation: "OptBool" = None,
    ):
        super().__init__()
        self.filters = filters
        self.input_volatility_type = input_volatility_type
        self.moneyness_type = moneyness_type
        self.price_side = price_side
        self.time_stamp = time_stamp
        self.volatility_model = volatility_model
        self.weights = try_copy_to_list(weights)
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.calculation_date = calculation_date
        self.svi_alpha_extrapolation = svi_alpha_extrapolation

    def _get_items(self):
        return [
            serializable_param_item.to_kv("filters", self.filters),
            enum_param_item.to_kv("inputVolatilityType", self.input_volatility_type),
            enum_param_item.to_kv("moneynessType", self.moneyness_type),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("timeStamp", self.time_stamp),
            enum_param_item.to_kv("volatilityModel", self.volatility_model),
            list_serializable_param_item.to_kv("weights", self.weights),
            enum_param_item.to_kv("xAxis", self.x_axis),
            enum_param_item.to_kv("yAxis", self.y_axis),
            datetime_param_item.to_kv("calculationDate", self.calculation_date),
            param_item.to_kv("sviAlphaExtrapolation", self.svi_alpha_extrapolation),
        ]
