from dataclasses import dataclass
from typing import Any, Callable, List, TYPE_CHECKING

import numpy as np

from ._models._curve import Curve, ForwardCurve, ZcCurve
from .._content_validator import CurvesAndSurfacesContentValidator
from .._request_factory import CurvesAndSurfacesRequestFactory, get_type_by_axis
from ..curves._cross_currency_curves._request_factory import CrossCurrencyCurvesDefinitionsRequestFactory
from ..curves._cross_currency_curves.definitions._data_classes import CurveDefinitionData
from ..curves._cross_currency_curves.triangulate_definitions._data_provider import TriangulateDefinitionsData
from ..._content_data import Data
from ..._content_data_provider import ContentDataProvider
from ..._content_response_factory import ContentResponseFactory
from ...._content_type import ContentType
from ...._tools import cached_property
from ....delivery._data._data_provider import DataProvider, ValidatorContainer
from ....delivery._data._response_factory import ResponseFactory

if TYPE_CHECKING:
    from ....delivery._data._data_provider import ParsedData


# ---------------------------------------------------------------------------
#   ContentValidator
# ---------------------------------------------------------------------------


class CurvesContentValidator(CurvesAndSurfacesContentValidator):
    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [self.content_data_is_not_none, self.any_element_have_no_error]


class CurveDefinitionContentValidator(CurvesContentValidator):
    _NAME_DATA = "curveDefinition"


class ForwardCurvesContentValidator(CurvesContentValidator):
    @classmethod
    def any_forward_curves_have_no_error(cls, data: "ParsedData") -> bool:
        elements = data.content_data.get(cls._NAME_DATA)
        if isinstance(elements, list):
            counter = len(elements) or 1
            for element in elements:
                for forward_curve in element.get("forwardCurves", []):
                    error = forward_curve.get("error")
                    if error:
                        counter -= 1
                        data.error_codes.append(error.get("code"))
                        data.error_messages.append(error.get("message"))

            if counter == 0:
                return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [self.content_data_is_not_none, self.any_element_have_no_error, self.any_forward_curves_have_no_error]


# ---------------------------------------------------------------------------
#   Content data
# ---------------------------------------------------------------------------


@dataclass
class OneCurveData(Data):
    _create_curves: Callable = None
    _curve: Curve = None

    @property
    def curve(self) -> Curve:
        if self._curve is None:
            curve = self._create_curves(self.raw)
            self._curve = curve[0]
        return self._curve


@dataclass
class CurvesData(Data):
    _create_curves: Callable = None
    _curves: List[Curve] = None

    @property
    def curves(self) -> List[Curve]:
        if self._curves is None:
            self._curves = self._create_curves(self.raw)
        return self._curves


def make_create_forward_curves(x_axis: str, y_axis: str) -> Callable:
    """
    Parameters
    ----------
    x_axis: str
        Name of key in curve point data for build X axis
    y_axis: str
        Name of key in curve point data for build Y axis

    Returns
    -------
    Callable
    """

    def create_forward_curves(raw: dict) -> list:
        """
        Curve point in "curvePoints":
        {
            "discountFactor": 1.0,
            "endDate": "2021-02-01",
            "ratePercent": -2.330761285491212,
            "startDate": "2021-02-01",
            "tenor": "0D"
        }
        Parameters
        ----------
        raw

        Returns
        -------
        list of ForwardCurve
        """
        curves = []
        for data in raw.get("data", []):
            for forward_curve in data.get("forwardCurves", []):
                x, y = [], []
                for point in forward_curve.get("curvePoints"):
                    end_date = point.get(x_axis)
                    x.append(end_date)
                    discount_factor = point.get(y_axis)
                    y.append(discount_factor)

                x = np.array(x, dtype=get_type_by_axis(x_axis))
                y = np.array(y, dtype=get_type_by_axis(y_axis))
                curve = ForwardCurve(x, y, **forward_curve)
                curves.append(curve)

        return curves

    return create_forward_curves


def make_create_bond_curves(x_axis: str, y_axis: str) -> Callable:
    """
    Parameters
    ----------
    x_axis: str
        Name of key in curve point data for build X axis
    y_axis: str
        Name of key in curve point data for build Y axis

    Returns
    -------
    Callable
    """

    def create_bond_curves(raw: dict) -> list:
        """
        Curve point in "curvePoints":
        {
            "discountFactor": 1.0,
            "endDate": "2021-02-01",
            "ratePercent": -2.330761285491212,
            "startDate": "2021-02-01",
            "tenor": "0D"
        }
        Parameters
        ----------
        raw

        Returns
        -------
        list of Curve
        """
        curves = []
        for data in raw.get("data", []):
            x, y = [], []
            for point in data.get("curvePoints"):
                end_date = point.get(x_axis)
                x.append(end_date)
                discount_factor = point.get(y_axis)
                y.append(discount_factor)

            x = np.array(x, dtype=get_type_by_axis(x_axis))
            y = np.array(y, dtype=get_type_by_axis(y_axis))
            curve = Curve(x, y)
            curves.append(curve)

        return curves

    return create_bond_curves


def make_create_zc_curves(x_axis: str, y_axis: str) -> Callable:
    """
    Parameters
    ----------
    x_axis: str
        Name of key in curve point data for build X axis
    y_axis: str
        Name of key in curve point data for build Y axis

    Returns
    -------
    Callable
    """

    def create_zc_curves(raw: dict) -> list:
        """
        Curve point in "curvePoints":
        {
            "discountFactor": 1.0,
            "endDate": "2021-07-27",
            "ratePercent": -0.7359148312458879,
            "startDate": "2021-07-27",
            "tenor": "ON",
            "instruments": [
                {
                    "instrumentCode": "SARON.S"
                }
            ]
        }
        Parameters
        ----------
        raw

        Returns
        -------
        list of ZcCurve
        """
        curves = []
        for data in raw.get("data", []):
            for index_tenor, zc_curve in data.get("curves", {}).items():
                x, y = [], []
                for point in zc_curve.get("curvePoints"):
                    end_date = point.get(x_axis)
                    x.append(end_date)
                    discount_factor = point.get(y_axis)
                    y.append(discount_factor)

                x = np.array(x, dtype=get_type_by_axis(x_axis))
                y = np.array(y, dtype=get_type_by_axis(y_axis))
                curve = ZcCurve(x, y, index_tenor, **zc_curve)
                curves.append(curve)

        return curves

    return create_zc_curves


curves_maker_by_content_type = {
    ContentType.FORWARD_CURVE: make_create_forward_curves(x_axis="endDate", y_axis="discountFactor"),
    ContentType.BOND_CURVE: make_create_bond_curves(x_axis="endDate", y_axis="discountFactor"),
    ContentType.ZC_CURVES: make_create_zc_curves(x_axis="endDate", y_axis="discountFactor"),
}


def get_curves_maker(content_type):
    curves_maker = curves_maker_by_content_type.get(content_type)

    if not curves_maker:
        raise ValueError(f"Cannot find curves_maker for content_type={content_type}")

    return curves_maker


# ---------------------------------------------------------------------------
#   Response factory
# ---------------------------------------------------------------------------


class CurvesResponseFactory(ContentResponseFactory):
    def create_data_success(self, raw: Any, **kwargs) -> Data:
        return self._do_create_data(raw, **kwargs)

    def create_data_fail(self, raw: Any, **kwargs) -> Data:
        return self._do_create_data({}, **kwargs)

    def _do_create_data(self, raw: Any, universe=None, **kwargs):
        content_type = kwargs.get("__content_type__")
        dfbuilder = self.get_dfbuilder(content_type, **kwargs)

        if content_type is ContentType.ZC_CURVE_DEFINITIONS:
            data = Data(raw, _dfbuilder=dfbuilder)

        else:
            curves_maker = get_curves_maker(content_type)
            if isinstance(universe, list):
                data = CurvesData(
                    raw=raw,
                    _dfbuilder=dfbuilder,
                    _create_curves=curves_maker,
                )

            else:
                data = OneCurveData(raw=raw, _dfbuilder=dfbuilder, _create_curves=curves_maker)

        return data


# ---------------------------------------------------------------------------
#   Data provider
# ---------------------------------------------------------------------------

curves_data_provider = ContentDataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=CurvesResponseFactory(),
    validator=ValidatorContainer(content_validator=CurvesContentValidator()),
)

forward_curves_data_provider = ContentDataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=CurvesResponseFactory(),
    validator=ValidatorContainer(content_validator=ForwardCurvesContentValidator()),
)

curve_data_provider = ContentDataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    validator=ValidatorContainer(content_validator=CurvesContentValidator()),
)

cross_currency_curves_triangulate_definitions_data_provider = DataProvider(
    request=CurvesAndSurfacesRequestFactory(),
    response=ResponseFactory(data_class=TriangulateDefinitionsData),
    validator=ValidatorContainer(content_validator=CurvesContentValidator()),
)

cross_currency_curves_definitions_data_provider = DataProvider(
    request=CrossCurrencyCurvesDefinitionsRequestFactory(),
    response=ResponseFactory(data_class=CurveDefinitionData),
    validator=ValidatorContainer(content_validator=CurveDefinitionContentValidator()),
)

cross_currency_curves_definitions_delete_data_provider = DataProvider(
    request=CrossCurrencyCurvesDefinitionsRequestFactory(),
)
