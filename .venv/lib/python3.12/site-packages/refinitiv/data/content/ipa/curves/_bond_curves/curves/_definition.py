from typing import TYPE_CHECKING

from ...._curves._bond_curves._curves._request import RequestItem
from ......_content_type import ContentType
from ......_tools import create_repr
from ....._content_provider_layer import ContentProviderLayer, PosArgsWarnMixin

if TYPE_CHECKING:
    from ......_types import OptStr, ExtendedParams, OptStrStrs
    from ...._curves._bond_curves._types import CurveDefinition, CurveParameters, OptCreditConstituents


class Definition(ContentProviderLayer, PosArgsWarnMixin):
    """
    Generates the Bond curves for the definitions provided.

    Parameters
    ----------
    constituents : CreditConstituents, optional
        CreditConstituents object.
    curve_definition : CreditCurveDefinition, optional
        CreditCurveDefinition object.
    curve_parameters : CreditCurveParameters, optional
        CreditCurveParameters object.
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.

    extended_params : dict, optional
        If necessary other parameters.

    Methods
    -------
    get_data(session=session, on_response=on_response)
        Returns a response to the data platform
    get_data_async(session=None, on_response=None, async_mode=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._bond_curves import curves
    >>> definition = curves.Definition(
    ...     curve_definition=curves.CreditCurveDefinition(
    ...         reference_entity="0#EUGOVPBMK=R",
    ...         reference_entity_type=curves.ReferenceEntityType.CHAIN_RIC
    ...     ))
    >>> response = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        constituents: "OptCreditConstituents" = None,
        curve_definition: "CurveDefinition" = None,
        curve_parameters: "CurveParameters" = None,
        curve_tag: "OptStr" = None,
        outputs: "OptStrStrs" = None,
        extended_params: "ExtendedParams" = None,
    ):
        request_item = RequestItem(
            constituents=constituents,
            curve_definition=curve_definition,
            curve_parameters=curve_parameters,
            curve_tag=curve_tag,
        )
        super().__init__(
            content_type=ContentType.BOND_CURVE,
            universe=request_item,
            outputs=outputs,
            extended_params=extended_params,
        )

    def __repr__(self):
        return create_repr(self, middle_path="_bond_curves.curves")
