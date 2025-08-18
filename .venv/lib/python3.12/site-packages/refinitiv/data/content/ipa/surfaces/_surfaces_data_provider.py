import warnings
from dataclasses import dataclass
from typing import Any, Callable, List, TYPE_CHECKING, Tuple

import numpy as np
import pandas as pd

from ._models import Surface
from .._content_validator import CurvesAndSurfacesContentValidator
from .._enums import Axis
from .._request_factory import CurvesAndSurfacesRequestFactory, get_type_by_axis
from ..._content_data import Data
from ..._content_data_provider import ContentDataProvider
from ..._error_parser import ErrorParser
from ...._tools import cached_property
from ....delivery._data._data_provider import ValidatorContainer
from ....delivery._data._endpoint_data import EndpointData
from ....delivery._data._response_factory import ResponseFactory

if TYPE_CHECKING:
    from ....delivery._data._data_provider import ParsedData

SURFACE_WARNING = "Surface cannot be built for rd.content.ipa.surfaces.swaption."
DF_WARNING = "Dataframe cannot be built for rd.content.ipa.surfaces.swaption."


# ---------------------------------------------------------------------------
#   ContentValidator
# ---------------------------------------------------------------------------


class SurfacesContentValidator(CurvesAndSurfacesContentValidator):
    @classmethod
    def content_data_status_is_not_error(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        if isinstance(content_data.get("data"), list) and content_data.get("status") == "Error":
            data.error_codes = content_data.get("code")
            data.error_messages = content_data.get("message")
            return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [
            self.content_data_is_not_none,
            self.content_data_status_is_not_error,
            self.any_element_have_no_error,
        ]


# ---------------------------------------------------------------------------
#   Data
# ---------------------------------------------------------------------------


def parse_axis(
    universe: dict,
    x_axis: Axis,
    y_axis: Axis,
) -> (np.array, np.array, np.array):
    """
      This method parsing the surface into lists row, column and matrix

      >>> from refinitiv.data.content import ipa
      >>> definition = ipa.surfaces.eti.Definition(
      ...     underlying_definition=ipa.surfaces.eti.EtiSurfaceDefinition(
      ...         instrument_code="BNPP.PA@RIC"
      ...     ),
      ...     surface_parameters=ipa.surfaces.eti.EtiCalculationParams(
      ...         price_side=ipa.surfaces.eti.PriceSide.MID,
      ...         volatility_model=ipa.surfaces.eti.VolatilityModel.SVI,
      ...         x_axis=ipa.surfaces.eti.Axis.STRIKE,
      ...         y_axis=ipa.surfaces.eti.Axis.DATE,
      ...     ),
      ...     surface_tag="1",
      ...     surface_layout=ipa.surfaces.eti.SurfaceLayout(
      ...         format=ipa.surfaces.eti.Format.MATRIX, y_point_count=10
      ...     ),
      ... )

      This example for surface_parameters with
      x_axis = Axis.STRIKE and y_axis = Axis.DATE

      |--→ column=Y
      ↓
    row=X

      >>> surface = universe.get("surface")
      >>> surface
      ... [
      ...   [None,    '2021-08-20', '2021-09-17', '2021-12-17', '2022-03-18'],
      ...   ['25.36',  63.76680855, 76.566676686, 514160483847, 45.563136028],
      ...   ['30.432', 56.20802369, 64.051912234, 46.118622487, 41.540289743],
      ...   ['35.504', 49.91436068, 51.916645386, 41.495311424, 37.870408673],
      ... ]

      Parameters
      ----------
      universe : dict
          dict with surface
      x_axis : Axis

      y_axis : Axis

      Returns
      -------
      (np.array, np.array, np.array)
          row, column, matrix or x, y, z

      Raises
      -------
      ValueError
          If x_axis or y_axis not correct
    """

    if not x_axis or not y_axis:
        raise ValueError(f"Cannot parse surface without information about x_axis={x_axis} or y_axis={y_axis}")

    surface = universe.get("surface")

    if surface is None:
        # column is ["-2.00", "-1.00", "-0.50"]
        column = universe.get("x")
        # row is ["1Y", "2Y", "3Y"]
        row = universe.get("y")
        # universe has z axis too: ["1M", "2M", "3M"]
        matrix = []
        # z_dimension is [["129.03", "121.85", "123.85"]]
        for z_dimension in universe.get("ndimensionalArray", []):
            # Y dimension is ["129.03", "121.85", "123.85"]
            # X dimension is "129.03"
            # matrix is [["129.03", "121.85", "123.85"]]
            matrix.extend(z_dimension)

    else:
        # column is ['2021-08-20', '2021-09-17', '2021-12-17', '2022-03-18', '2022-06-17']
        column = surface[0][1:]
        row = []
        matrix = []
        # curve is ['25.36',  63.76680855, 76.566676686, 514160483847, 41.187204258]
        for curve in surface[1:]:
            # row is '25.36'
            row.append(curve[0])
            # matrix is [63.76680855, 76.566676686, 514160483847, 41.187204258]
            matrix.append(curve[1:])

    try:
        column = np.array(column, dtype=get_type_by_axis(y_axis))
    except ValueError:
        column = np.array(column, dtype=object)

    try:
        row = np.array(row, dtype=get_type_by_axis(x_axis))
    except ValueError:
        row = np.array(row, dtype=object)

    matrix = np.array(matrix, dtype=float)

    return row, column, matrix


def create_surfaces(raw, axes_params) -> List[Surface]:
    surfaces = []

    if raw and axes_params:
        for i, universe in enumerate(raw.get("data")):
            x_axis, y_axis = axes_params[i]
            row, column, matrix = parse_axis(universe, x_axis, y_axis)
            surface = Surface(row=row, column=column, matrix=matrix)
            surfaces.append(surface)

    return surfaces


@dataclass
class BaseData(EndpointData):
    _dataframe: "pd.DataFrame" = None
    _axes_params: List = None

    @property
    def df(self):
        if self._dataframe is None and self.raw:
            data = self.raw.get("data")

            if data:
                surface = data[0].get("surface")
                if isinstance(surface, dict):
                    data_frame = pd.DataFrame([])
                else:
                    data_frame = pd.DataFrame(data)
                    data_frame.set_index("surfaceTag", inplace=True)

            else:
                data_frame = pd.DataFrame([])

            if not data_frame.empty:
                data_frame = data_frame.convert_dtypes()

            self._dataframe = data_frame

        return self._dataframe


@dataclass
class OneSurfaceData(BaseData):
    _surface: Surface = None

    @property
    def surface(self) -> Surface:
        if self._surface is None:
            surfaces = create_surfaces(self.raw, self._axes_params)
            self._surface = surfaces[0]
        return self._surface

    @property
    def df(self):
        if self._dataframe is None:
            data = {x: z for x, z in zip(self.surface.x, self.surface.z)}

            if data:
                data_frame = pd.DataFrame(data, index=self.surface.y)
            else:
                data_frame = super().df

            if not data_frame.empty:
                data_frame.fillna(pd.NA, inplace=True)
                data_frame = data_frame.convert_dtypes()

            self._dataframe = data_frame

        return self._dataframe


@dataclass
class OneSwaptionSurfaceData(Data):
    @property
    def surface(self):
        warnings.warn(SURFACE_WARNING)
        return Surface([], [], [[]])

    @property
    def df(self):
        warnings.warn(DF_WARNING)
        return pd.DataFrame()


@dataclass
class SurfacesData(BaseData):
    _surfaces: List[Surface] = None

    @property
    def surfaces(self) -> List[Surface]:
        if self._surfaces is None:
            self._surfaces = create_surfaces(self.raw, self._axes_params)
        return self._surfaces


@dataclass
class SwaptionSurfacesData(Data):
    @property
    def df(self):
        warnings.warn(DF_WARNING)
        return pd.DataFrame()

    @property
    def surfaces(self):
        warnings.warn(SURFACE_WARNING)
        return []


# ---------------------------------------------------------------------------
#   ResponseFactory
# ---------------------------------------------------------------------------


def get_surface_parameters(obj):
    if hasattr(obj, "_kwargs"):
        request_item = obj._kwargs.get("universe")

    else:
        request_item = obj

    return request_item.surface_parameters


def get_names_axis(surface_parameters) -> Tuple[str, str]:
    return surface_parameters.x_axis, surface_parameters.y_axis


def get_axis_params(obj, axis_params: list = None) -> List[Tuple[str, str]]:
    if axis_params is None:
        axis_params = []

    surface_parameters = get_surface_parameters(obj)
    axis_params.append(get_names_axis(surface_parameters))
    return axis_params


class SurfaceResponseFactory(ResponseFactory):
    def create_data_success(self, raw: Any, **kwargs) -> EndpointData:
        return self._do_create_data(raw, **kwargs)

    def create_data_fail(self, raw: Any, **kwargs) -> EndpointData:
        return self._do_create_data({}, **kwargs)

    def _do_create_data(self, raw: Any, universe=None, **kwargs):
        if universe:
            if isinstance(universe, list):
                axes_params = []
                for definition in universe:
                    get_axis_params(definition, axes_params)

                return SurfacesData(raw, _axes_params=axes_params)

            surface_parameters = get_surface_parameters(universe)
            if surface_parameters and all(get_names_axis(surface_parameters)):
                axes_params = get_axis_params(universe)
                return OneSurfaceData(raw, _axes_params=axes_params)

        return BaseData(raw)


class SwaptionSurfaceResponseFactory(SurfaceResponseFactory):
    def _do_create_data(self, raw: Any, universe=None, **kwargs):
        if universe:
            if isinstance(universe, list):
                return SwaptionSurfacesData(raw)

            surface_parameters = get_surface_parameters(universe)
            if surface_parameters and all(get_names_axis(surface_parameters)):
                return OneSwaptionSurfaceData(raw)

        return BaseData(raw)


# ---------------------------------------------------------------------------
#   DataProvider
# ---------------------------------------------------------------------------

surfaces_data_provider = ContentDataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=SurfaceResponseFactory(),
    validator=ValidatorContainer(content_validator=SurfacesContentValidator()),
    parser=ErrorParser(),
)

swaption_surfaces_data_provider = ContentDataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=SwaptionSurfaceResponseFactory(),
    validator=ValidatorContainer(content_validator=SurfacesContentValidator()),
    parser=ErrorParser(),
)
