from typing import TYPE_CHECKING, Optional

from .._models import SurfaceFilters
from ..._enums import InputVolatilityType, VolatilityAdjustmentType, Axis, PriceSide, TimeStamp
from ..._param_item import datetime_param_item, enum_param_item, param_item, serializable_param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr, OptFloat, OptDateTime


class IIrVolModelPricingParameters(Serializable):
    # new name CapletsStrippingSurfaceParameters in version 1.0.130
    """
    This class property contains the properties that may be used to control the
    calculation. It mainly covers dates, market data assumptions (e.g. interpolation),
    and pricing model preferences. Some Parameters are common to all volatility surfaces
    contracts, while others are specific to a particular type of volatility.

    Parameters
    ----------
    input_volatility_type : InputVolatilityType, optional
        User can specify whether calibration is based on normal or lognorma vol. however
        it would be preferrable to let the service determine the most appropriate one
    volatility_adjustment_type : VolatilityAdjustmentType, optional
        Volatility adjustment method applied to caplets surface before stripping. the
        default value is 'constantcap'.
    x_axis : Axis, optional
        The enumerate that specifies the unit for the x axis.
    y_axis : Axis, optional
        The enumerate that specifies the unit for the y axis.
    z_axis : Axis, optional
        Specifies the unit for the z axis (e.g. strike, expiry, tenor). this applies to
        swaption sabr cube.
    market_data_date : DEPRECATED
        This attribute doesn't use anymore.
    shift_percent : float, optional
        Shift applied to calibrated strikes allowing negative rates. the value is
        expressed in percentages. the default value is selected based oninstrumentcode
    source : str, optional
        Requested volatility data contributor.
    stripping_shift_percent : float, optional
        Shift value applied to strikes allowing the stripped caplets surface to include
        volatility even when some strikes are negative. the value is expressed in
        percentages. the default value is '0.0'.
    valuation_date : str or date or datetime or timedelta, optional
        The date at which the instrument is valued. the value is expressed in iso 8601
        format: yyyy-mm-ddt[hh]:[mm]:[ss]z (e.g., '2021-01-01t00:00:00z'). by default,
        marketdatadate is used. if marketdatadate is not specified, the default value is
        today.
    filters : SurfaceFilters, optional
    price_side : PriceSide, optional
        Specifies whether bid, ask, mid or settle is used to build the surface. if not
        precised, default to mid.
    time_stamp : TimeStamp, optional
        Define how the timestamp is selected:
        - open: the opening value of the valuationdate or if not available the close of
          the previous day is used.
        - default: the latest snapshot is used when valuationdate is today, the close
          price when valuationdate is in the past.
    calculation_date : str or date or datetime or timedelta, optional
        The date the volatility surface is generated.
    """

    def __init__(
        self,
        input_volatility_type: Optional[InputVolatilityType] = None,
        volatility_adjustment_type: Optional[VolatilityAdjustmentType] = None,
        x_axis: Optional[Axis] = None,
        y_axis: Optional[Axis] = None,
        z_axis: Optional[Axis] = None,
        market_data_date=None,
        shift_percent: "OptFloat" = None,
        source: "OptStr" = None,
        stripping_shift_percent: "OptFloat" = None,
        valuation_date: "OptDateTime" = None,
        filters: Optional[SurfaceFilters] = None,
        price_side: Optional[PriceSide] = None,
        time_stamp: Optional[TimeStamp] = None,
        calculation_date: "OptDateTime" = None,
    ):
        super().__init__()
        self.input_volatility_type = input_volatility_type
        self.volatility_adjustment_type = volatility_adjustment_type
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis
        self.market_data_date = market_data_date
        self.shift_percent = shift_percent
        self.source = source
        self.stripping_shift_percent = stripping_shift_percent
        self.valuation_date = valuation_date
        self.filters = filters
        self.price_side = price_side
        self.time_stamp = time_stamp
        self.calculation_date = calculation_date

    def _get_items(self):
        return [
            enum_param_item.to_kv("inputVolatilityType", self.input_volatility_type),
            enum_param_item.to_kv("volatilityAdjustmentType", self.volatility_adjustment_type),
            enum_param_item.to_kv("xAxis", self.x_axis),
            enum_param_item.to_kv("yAxis", self.y_axis),
            enum_param_item.to_kv("zAxis", self.z_axis),
            param_item.to_kv("shiftPercent", self.shift_percent),
            param_item.to_kv("source", self.source),
            param_item.to_kv("strippingShiftPercent", self.stripping_shift_percent),
            datetime_param_item.to_kv("valuationDate", self.valuation_date),
            serializable_param_item.to_kv("filters", self.filters),
            enum_param_item.to_kv("priceSide", self.price_side),
            enum_param_item.to_kv("timeStamp", self.time_stamp),
            datetime_param_item.to_kv("calculationDate", self.calculation_date),
        ]
