from typing import TYPE_CHECKING, Optional, Union, Iterable

from numpy import iterable

from ._zc_curve_request_item import ZcCurveRequestItem
from ...._content_provider_layer import ContentProviderLayer, PosArgsWarnMixin
from ....._content_type import ContentType
from ....._tools import create_repr, try_copy_to_list

if TYPE_CHECKING:
    from . import ZcCurveDefinitions
    from ._zc_curve_parameters import ZcCurveParameters
    from .. import zc_curves
    from .._models import Constituents, ShiftScenario
    from ....._types import OptStr, ExtendedParams, OptStrStrs

    DefnDefns = Union["zc_curves.Definition", Iterable["zc_curves.Definition"]]


class Definition(ContentProviderLayer, PosArgsWarnMixin):
    """
    Parameters
    ----------
    constituents : Constituents, optional

    curve_definition : ZcCurveDefinitions, optional

    curve_parameters : ZcCurveParameters, optional

    curve_tag : str, optional

    extended_params : dict, optional
        If necessary other parameters.

    shift_scenarios : ShiftScenario, optional
        The list of attributes applied to the curve shift scenarios.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, async_mode=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> import refinitiv.data.content.ipa.curves.zc_curves as zc_curves
    >>> definition = zc_curves.Definition(
    ...     curve_definition=zc_curves.ZcCurveDefinitions(
    ...         currency="CHF",
    ...         name="CHF LIBOR Swap ZC Curve",
    ...         discounting_tenor="OIS",
    ...     ),
    ...     curve_parameters=zc_curves.ZcCurveParameters(
    ...         use_steps=True
    ...     )
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    _WARN_NAME = "curves.zc_curves.Definition"
    _WARN_EX = "use curves.zc_curves.Definition(curve_tag='TAG') instead of curves.zc_curves.Definition('TAG')"

    def __init__(
        self,
        constituents: "Constituents" = None,
        curve_definition: "ZcCurveDefinitions" = None,
        curve_parameters: "ZcCurveParameters" = None,
        curve_tag: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
        shift_scenarios: Optional["ShiftScenario"] = None,
        outputs: "OptStrStrs" = None,
    ):
        request_item = ZcCurveRequestItem(
            constituents=constituents,
            curve_definition=curve_definition,
            curve_parameters=curve_parameters,
            curve_tag=curve_tag,
            shift_scenarios=shift_scenarios,
        )
        super().__init__(
            content_type=ContentType.ZC_CURVES,
            universe=request_item,
            outputs=outputs,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self)


class Definitions(ContentProviderLayer):
    """
    Parameters
    ----------
    universe : zc_curves.Definition, list of zc_curves.Definition

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, async_mode=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> import refinitiv.data.content.ipa.curves.zc_curves as zc_curves
    >>> definition = zc_curves.Definition(
    ...     curve_definition=zc_curves.ZcCurveDefinitions(
    ...         currency="CHF",
    ...         name="CHF LIBOR Swap ZC Curve",
    ...         discounting_tenor="OIS",
    ...     ),
    ...     curve_parameters=zc_curves.ZcCurveParameters(
    ...         use_steps=True
    ...     )
    ... )
    >>> definition = zc_curves.Definitions(universe=definition)
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        universe: "DefnDefns",
        outputs: "OptStrStrs" = None,
    ):
        universe = try_copy_to_list(universe)
        if not iterable(universe):
            universe = [universe]

        super().__init__(
            content_type=ContentType.ZC_CURVES,
            universe=universe,
            outputs=outputs,
            __plural__=True,
        )

    def __repr__(self):
        return create_repr(self, class_name=self.__class__.__name__)
