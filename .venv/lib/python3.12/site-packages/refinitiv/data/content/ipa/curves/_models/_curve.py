from typing import Union

import numpy as np
from scipy import interpolate

from . import CurvePoint
from ..._request_factory import value_arg_parser
from ..._enums import Axis


class Curve:
    """
    Methods
    -------
        get_point(x, y): CurvePoint

    Examples
    -------
    >>> from refinitiv.data.content.ipa.curves import forward_curve
    >>> definition = forward_curve.Definition(
    ...    curve_definition=forward_curve.SwapZcCurveDefinition(
    ...        currency="EUR",
    ...        index_name="EURIBOR",
    ...        name="EUR EURIBOR Swap ZC Curve",
    ...        discounting_tenor="OIS",
    ...
    ...    ),
    ...    forward_curve_definitions=[
    ...        forward_curve.ForwardCurveDefinition(
    ...            index_tenor="3M",
    ...            forward_curve_tag="ForwardTag",
    ...            forward_start_date="2021-02-01",
    ...            forward_curve_tenors=[
    ...                "0D",
    ...                "1D",
    ...                "2D",
    ...                "3M",
    ...                "6M",
    ...                "9M",
    ...                "1Y",
    ...                "2Y",
    ...                "3Y",
    ...                "4Y",
    ...                "5Y",
    ...                "6Y",
    ...                "7Y",
    ...                "8Y",
    ...                "9Y",
    ...                "10Y",
    ...                "15Y",
    ...                "20Y",
    ...                "25Y"
    ...            ]
    ...        )
    ...    ]
    ...)
    >>> response = definition.get_data()
    >>> curve = response.data.curve
    >>> point = curve.get_point("2021-02-02", Axis.X)
    """

    def __init__(self, x: np.array, y: np.array) -> None:
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def get_point(
        self,
        value: Union[str, float, np.datetime64],
        axis: Union[Axis, str],
    ) -> CurvePoint:
        """
        Parameters
        ----------
        value: str, float, np.datetime64

        axis: Axis

        Returns
        -------
        CurvePoint

        Raises
        -------
        ValueError
            If cannot identify axis
        """
        value = value_arg_parser.parse(value)

        is_value_on_axis_x = axis == Axis.X
        is_value_on_axis_y = axis == Axis.Y

        value_as_float = value_arg_parser.get_float(value)

        if is_value_on_axis_x:
            f = interpolate.interp1d(
                x=self._x.astype(float),
                y=self._y.astype(float),
            )
            x = value
            y = f(x=value_as_float)
            y = float(y)

        elif is_value_on_axis_y:
            f = interpolate.interp1d(
                x=self._y.astype(float),
                y=self._x.astype(float),
            )
            x = f(x=value_as_float)
            x = float(x)
            y = value

        else:
            raise ValueError(f"Cannot identify axis={axis}")

        return CurvePoint(x, y)

    def __str__(self) -> str:
        x = self._x
        if np.iterable(self._x):
            x = ", ".join(str(i) for i in self._x)

        y = self._y
        if np.iterable(self._y):
            y = ", ".join(str(i) for i in self._y)

        return f"X={x}\nY={y}"


class ForwardCurve(Curve):
    def __init__(self, x: np.array, y: np.array, **kwargs) -> None:
        super().__init__(x, y)
        self.forward_curve_tag = kwargs.get("forwardCurveTag")
        self.forward_start = kwargs.get("forwardStart")
        self.index_tenor = kwargs.get("indexTenor")


class ZcCurve(Curve):
    def __init__(self, x: np.array, y: np.array, index_tenor, **kwargs) -> None:
        super().__init__(x, y)
        self.index_tenor = index_tenor
        self.is_discount_curve = kwargs.get("isDiscountCurve")
