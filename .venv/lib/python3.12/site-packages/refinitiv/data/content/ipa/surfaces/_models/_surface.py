from typing import Union

import numpy as np
from scipy import interpolate

from ._surface_point import SurfacePoint
from ..._enums import Axis
from ..._request_factory import value_arg_parser, x_arg_parser, y_arg_parser
from ...curves._models._curve import Curve
from ....._tools import cached_property


class Surface:
    """
    The actual volatility surface

    Parameters
    -------
    row : np.array
        Specifies a data of discrete values for the y-axis
    column : np.array
        Specifies a data of discrete values for the x-axis
    matrix : np.array
        Specifies whether the calculated volatilities a matrix.

    Methods
    -------
        get_curve(value, axis): Curve

        get_point(x, y): SurfacePoint

    Examples
    -------
    >>> from refinitiv.data.content.ipa.surfaces import eti
    >>> definition = eti.Definition(
    ...     underlying_definition=eti.EtiSurfaceDefinition(
    ...         instrument_code="BNPP.PA@RIC"
    ...     ),
    ...     surface_parameters=eti.EtiCalculationParams(
    ...         price_side=eti.PriceSide.MID,
    ...         volatility_model=eti.VolatilityModel.SVI,
    ...         x_axis=eti.Axis.STRIKE,
    ...         y_axis=eti.Axis.DATE,
    ...     ),
    ...     surface_tag="1_MATRIX",
    ...     surface_layout=eti.SurfaceLayout(
    ...         format=eti.Format.MATRIX,
    ...         y_point_count=10
    ...     ),
    ... )
    >>> response = definition.get_data()
    >>> surface = response.data.surface
    >>> curve = surface.get_curve("25.35", eti.Axis.X)
    >>> curve = surface.get_curve("2021-08-20", eti.Axis.Y)
    >>> point = surface.get_point(25.35, "2020-08-20")

    """

    def __init__(self, row: np.array, column: np.array, matrix: np.array) -> None:
        self._row = row
        self._column = column
        self._matrix = matrix

    @cached_property
    def _values_by_axis(self):
        return {
            Axis.X: self.x,
            Axis.Y: self.y,
            Axis.Z: self.z,
        }

    @cached_property
    def _interp(self):
        """
        For interpolate.interp2d axes are:

           |--→ column=x
           ↓
         row=y

        """
        return interpolate.interp2d(
            x=self._column.astype(float),
            y=self._row.astype(float),
            z=self._matrix.astype(float),
        )

    @property
    def x(self):
        return self._row

    @property
    def y(self):
        return self._column

    @property
    def z(self):
        return self._matrix

    def get_curve(
        self,
        value: Union[str, float, int, np.datetime64],
        axis: Union[Axis, str],
    ) -> Curve:
        """
        Get curve

        Parameters
        ----------
        value: str, float, int, np.datetime64
            Establishment value
        axis: Axis
            The enumerate that specifies the unit for the axis

        Returns
        -------
        Curve
        """
        values = self._values_by_axis.get(axis, [])

        value = value_arg_parser.parse(value)

        axis_x, axis_y = [], []

        is_axis_x = axis == Axis.X
        is_axis_y = axis == Axis.Y
        is_axis_z = axis == Axis.Z

        # interpolate
        if value not in values and not is_axis_z:
            value = value_arg_parser.get_float(value)

            if is_axis_x:
                axis_x = self._column
                axis_y = self._interp(
                    x=self._column.astype(float),
                    y=value,
                )

            elif is_axis_y:
                axis_x = self._interp(
                    x=value,
                    y=self._row.astype(float),
                )
                axis_x = axis_x[:, 0]
                axis_y = self._row

        else:
            index = np.where(values == value)

            if is_axis_x:
                axis_x = self.z[index, :]
                axis_x = axis_x[0][0]
                axis_y = self.y

            elif is_axis_y:
                axis_x = self.x
                axis_y = self.z[:, index]
                axis_y = axis_y[:, 0][:, 0]

            elif is_axis_z:
                axis_x = self.x
                axis_y = self.y

        return Curve(axis_x, axis_y)

    def get_point(
        self,
        x: Union[str, int, float, np.datetime64],
        y: Union[str, int, float, np.datetime64],
    ) -> SurfacePoint:
        """
        Get SurfacePoint

        Parameters
        ----------
        x: str, float, int, np.datetime64
            X axis
        y: str, float, int, np.datetime64
            Y axis

        Returns
        -------
        SurfacePoint
        """

        x = x_arg_parser.parse(x)
        y = y_arg_parser.parse(y)

        if x in self.x and y in self.y:
            (row,) = np.where(self._row == x)
            (column,) = np.where(self._column == y)
            z = self._matrix[row, column]
            z = z[0]

        # interpolate
        else:
            x_as_float = value_arg_parser.get_float(x)
            y_as_float = value_arg_parser.get_float(y)
            z = self._interp(x=y_as_float, y=x_as_float)
            z = z[0]

        return SurfacePoint(x, y, z)
