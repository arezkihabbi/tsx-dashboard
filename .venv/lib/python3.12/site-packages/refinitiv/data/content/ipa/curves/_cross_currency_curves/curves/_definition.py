from typing import TYPE_CHECKING

from ...._curves._cross_currency_curves._curves._request import RequestItem
from ......_content_type import ContentType
from ......_tools import create_repr
from ....._content_provider_layer import ContentProviderLayer, PosArgsWarnMixin


if TYPE_CHECKING:
    from ......_types import OptStr, ExtendedParams, OptStrStrs
    from ...._curves._cross_currency_curves._curves._types import (
        CurveDefinition,
        CurveParameters,
        ShiftScenarios,
        FxConstituents,
    )


class Definition(ContentProviderLayer, PosArgsWarnMixin):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    constituents : FxForwardConstituents, optional
        FxForwardConstituents object.
    curve_definition : FxForwardCurveDefinition, optional
        FxForwardCurveDefinition object.
    curve_parameters : FxForwardCurveParameters, optional
        FxForwardCurveParameters object.
    shift_scenarios : FxShiftScenario, optional
        The list of attributes applied to the curve shift scenarios.
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    extended_params : dict, optional
        If necessary other parameters.

    Examples
    --------
    >>> import refinitiv.data.content.ipa.curves._cross_currency_curves as crs_currency
    >>> definition = crs_currency.curves.Definition(
    ...    curve_definition=crs_currency.curves.FxForwardCurveDefinition(
    ...        base_currency="EUR",
    ...        base_index_name="ESTR",
    ...        quoted_currency="USD",
    ...        quoted_index_name="SOFR"
    ...    ),
    ...    curve_parameters=crs_currency.curves.FxForwardCurveParameters(
    ...        valuation_date="2021-10-06"
    ...    )
    ... )
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        constituents: "FxConstituents" = None,
        curve_definition: "CurveDefinition" = None,
        curve_parameters: "CurveParameters" = None,
        shift_scenarios: "ShiftScenarios" = None,
        curve_tag: "OptStr" = None,
        outputs: "OptStrStrs" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        request_item = RequestItem(
            constituents=constituents,
            curve_definition=curve_definition,
            curve_parameters=curve_parameters,
            shift_scenarios=shift_scenarios,
            curve_tag=curve_tag,
        )
        super().__init__(
            content_type=ContentType.CROSS_CURRENCY_CURVES_CURVES,
            universe=request_item,
            outputs=outputs,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self, middle_path="_cross_currency_curves.curves")
