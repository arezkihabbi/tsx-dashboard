from typing import Iterable

from ._volatility_surface_point import VolatilitySurfacePoint
from ..._enums import Format
from ..._param_item import enum_param_item, list_serializable_param_item, param_item
from ..._serializable import Serializable
from ....._tools import create_repr, try_copy_to_list
from ....._types import OptStrings, OptInt


class SurfaceLayout(Serializable):
    """
    This class property contains the properties that may be used to control how the
    surface is displayed.

    Parameters
    ---------
    data_points : list of VolatilitySurfacePoint, optional
        Specifies the list of specific data points to be returned
    format : Format, option
        Specifies whether the calculated volatilities are returned as a list or a matrix
    x_values : list of str, optional
        Specifies a list of discrete values for the x-axis
    y_values : list of str, optional
        Specifies a list of discrete values for the y-axis
    z_values : list of str, optional
        Specifies a list of discrete values for the z-axis
    x_point_count : int, optional
        Specifies the number of values that will be generated along the x-axis.
        These values will distributed depending on the available input data and the type
        of volatility
    y_point_count : int, optional
        Specifies the number of values that will be generated along the y-axis.
        These values will distributed depending on the available input data and the type
        of volatility
    z_point_count : int, optional
        Specifies the number of values that will be generated along the z-axis.
        These values will distributed depending on the available input data and the type
        of volatility

    Examples
    -------
    >>> from refinitiv.data.content.ipa.surfaces.fx import SurfaceLayout
    >>> from refinitiv.data.content.ipa.surfaces import fx
    >>> SurfaceLayout(format=fx.Format.MATRIX)
    """

    def __init__(
        self,
        data_points: Iterable["VolatilitySurfacePoint"] = None,
        format: Format = None,
        x_values: OptStrings = None,
        y_values: OptStrings = None,
        z_values: OptStrings = None,
        x_point_count: OptInt = None,
        y_point_count: OptInt = None,
        z_point_count: OptInt = None,
    ):
        super().__init__()
        self.data_points = try_copy_to_list(data_points)
        self.format = format
        self.x_values = try_copy_to_list(x_values)
        self.y_values = try_copy_to_list(y_values)
        self.z_values = try_copy_to_list(z_values)
        self.x_point_count = x_point_count
        self.y_point_count = y_point_count
        self.z_point_count = z_point_count

    def __repr__(self):
        return create_repr(self, middle_path="fx", class_name="SurfaceLayout")

    def _get_items(self):
        return [
            list_serializable_param_item.to_kv("dataPoints", self.data_points),
            enum_param_item.to_kv("format", self.format),
            param_item.to_kv("xValues", self.x_values),
            param_item.to_kv("yValues", self.y_values),
            param_item.to_kv("zValues", self.z_values),
            param_item.to_kv("xPointCount", self.x_point_count),
            param_item.to_kv("yPointCount", self.y_point_count),
            param_item.to_kv("zPointCount", self.z_point_count),
        ]
