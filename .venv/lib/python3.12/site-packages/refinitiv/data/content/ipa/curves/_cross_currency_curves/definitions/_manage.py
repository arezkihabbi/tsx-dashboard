from typing import Union, TYPE_CHECKING

from ...._curves._cross_currency_curves._definitions._create import CreateRequest
from ...._curves._cross_currency_curves._definitions._delete import DeleteRequest
from ...._curves._cross_currency_curves._definitions._get import (
    CrossCurrencyCurveDefinitionKeys,
    GetRequest,
)
from ...._curves._cross_currency_curves._definitions._update import UpdateRequest

from ......_content_type import ContentType
from ......delivery._data import RequestMethod
from ......delivery._data._data_provider_layer import DataProviderLayer

if TYPE_CHECKING:
    from ...._curves._cross_currency_curves._definitions._types import (
        OptMainConstituentAssetClass,
        OptRiskType,
        Segments,
        OptTurns,
        CurveCreateDefinition,
        OptOverrides,
        CurveUpdateDefinition,
    )
    from ......delivery._data._data_provider import Response
    from ......_core.session import Session
    from ......_types import ExtendedParams, OptStr, OptBool


UnionSaveRequest = Union[CreateRequest, UpdateRequest]


def delete(id: str, session: "Session" = None) -> "Response":
    """
    Delete the Cross Currency curve definition for the definition Id provided.

    Parameters
    ----------
    id : str
        The identifier of the cross currency definition.
    session : Session, optional
        session=None. Means default session would be used.

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
    >>> response = definitions.manage.delete(id="334b89f6-e272-4900-ad1e-dfefv")
    """
    request_item = DeleteRequest(id)
    data_provider_layer = DataProviderLayer(
        data_type=ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_DELETE,
        request_items=request_item,
        method=RequestMethod.POST,
    )
    return data_provider_layer.get_data(session)


def get(
    id: "OptStr" = None,
    main_constituent_asset_class: "OptMainConstituentAssetClass" = None,
    risk_type: "OptRiskType" = None,
    base_currency: "OptStr" = None,
    base_index_name: "OptStr" = None,
    is_non_deliverable: "OptBool" = None,
    name: "OptStr" = None,
    quoted_currency: "OptStr" = None,
    quoted_index_name: "OptStr" = None,
    source: "OptStr" = None,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
) -> "Response":
    """
    Gets the Commodities curve definition for the definition provided.

    Parameters
    ----------
    id : str, optional
        The identifier of the cross currency definitions.
    main_constituent_asset_class : MainConstituentAssetClass, optional
        The asset class used to generate the zero coupon curve. the possible values are:
        * fxforward   * swap
    risk_type : RiskType, optional
        The risk type to which the generated cross currency curve is sensitive. the
        possible value is:   * 'crosscurrency'
    base_currency : str, optional
        The base currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'eur').
    base_index_name : str, optional
        The name of the floating rate index (e.g., 'estr') applied to the base currency.
    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable:   * true: the instrument
        is non-deliverable,   * false: the instrument is not non-deliverable. the
        property can be used to retrieve cross currency definition for the adjusted
        interest rate curve.
    name : str, optional
        The fxcross currency pair applied to the reference or pivot currency. it is
        expressed in iso 4217 alphabetical format (e.g., 'eur usd fxcross').
    quoted_currency : str, optional
        The quoted currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'usd').
    quoted_index_name : str, optional
        The name of the floating rate index (e.g., 'sofr') applied to the quoted
        currency.
    source : str, optional
        A user-defined string that is provided by the creator of a curve. curves created
        by refinitiv have the 'refinitiv' source.
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None - means default session would be used.

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
    >>> response = definitions.manage.get(
    ...     base_currency="EUR",
    ...     base_index_name="EURIBOR",
    ...     quoted_currency="USD",
    ...     quoted_index_name="LIBOR",
    >>> )
    """
    definition_obj = CrossCurrencyCurveDefinitionKeys(
        main_constituent_asset_class=main_constituent_asset_class,
        risk_type=risk_type,
        base_currency=base_currency,
        base_index_name=base_index_name,
        id=id,
        is_non_deliverable=is_non_deliverable,
        name=name,
        quoted_currency=quoted_currency,
        quoted_index_name=quoted_index_name,
        source=source,
    )
    request_item = GetRequest(curve_definition=definition_obj)
    content_provider_layer = DataProviderLayer(
        data_type=ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_GET,
        request_items=request_item,
        extended_params=extended_params,
    )
    response = content_provider_layer.get_data(session=session)
    return response


def create(
    curve_definition: "CurveCreateDefinition",
    segments: "Segments",
    *,
    overrides: "OptOverrides" = None,
    turns: "OptTurns" = None,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
) -> "Response":
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    curve_definition : CrossCurrencyCurveDefinitionDescription
        CrossCurrencyCurveDefinitionDescription object
    segments : list of CrossCurrencyInstrumentsSegment
        list of CrossCurrencyInstrumentsSegment objects
    overrides : list of OverrideBidAsk, optional
        OverrideBidAsk object.
    turns : list of OverrideFxForwardTurn, optional
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None - means default session would be used

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
    >>> response = definitions.manage.create(
    ...     curve_definition=definitions.CrossCurrencyCurveCreateDefinition(
    ...         source="SourceName",
    ...         name="Name of the Curve854",
    ...         base_currency="EUR",
    ...         base_index_name="ESTR",
    ...         quoted_currency="USD",
    ...         quoted_index_name="SOFR",
    ...         is_non_deliverable=False
    ...     ),
    ...     segments=[
    ...         definitions.CrossCurrencyInstrumentsSegment(
    ...             start_date="2021-01-01",
    ...             constituents=definitions.CrossCurrencyConstituentsDescription(
    ...                 fx_forwards=[
    ...                     definitions.FxForwardInstrumentDescription(
    ...                         instrument_definition=definitions.FxForwardInstrumentDefinition(
    ...                             instrument_code="EUR1M=",
    ...                             tenor="1M",
    ...                             is_non_deliverable=False,
    ...                             quotation_mode=definitions.QuotationMode.OUTRIGHT
    ...                         )
    ...                     )
    ...                 ]
    ...             ),
    ...         )
    ...     ]
    >>> )
    """
    request_items = CreateRequest(
        curve_definition=curve_definition,
        overrides=overrides,
        segments=segments,
        turns=turns,
    )

    response = _save(
        ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_CREATE,
        request_items=request_items,
        extended_params=extended_params,
        session=session,
    )
    return response


def update(
    curve_definition: "CurveUpdateDefinition",
    segments: "Segments",
    *,
    overrides: "OptOverrides" = None,
    turns: "OptTurns" = None,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
) -> "Response":
    """
    Updates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    curve_definition : CrossCurrencyCurveUpdateDefinition
        CrossCurrencyCurveUpdateDefinition object.
    segments : list of CrossCurrencyInstrumentsSegment
        list of CrossCurrencyInstrumentsSegment objects
    overrides : list of OverrideBidAsk, optional
        OverrideBidAsk object.
    turns : list of OverrideFxForwardTurn, optional
    extended_params : ExtendedParams, optional
        If necessary other parameters.
    session : Session, optional
        session=None - means default session would be used

    Examples
    --------
    >>> from refinitiv.data.content.ipa.curves._cross_currency_curves import definitions
    >>> response = definitions.manage.update(
    ...     curve_definition=definitions.CrossCurrencyCurveUpdateDefinition(
    ...         id="7bdb00f3-0a48-40be-ace2-6d3cfd0e8e59",
    ...         source="SourceName",
    ...         name="rename curve",
    ...         base_currency="EUR",
    ...         base_index_name="ESTR",
    ...         quoted_currency="USD",
    ...         quoted_index_name="SOFR",
    ...         is_non_deliverable=False
    ...     ),
    ...     segments=[
    ...         definitions.CrossCurrencyInstrumentsSegment(
    ...             start_date="2021-01-01",
    ...             constituents=definitions.CrossCurrencyConstituentsDescription(
    ...                 fx_forwards=[
    ...                     definitions.FxForwardInstrumentDescription(
    ...                         instrument_definition=definitions.FxForwardInstrumentDefinition(
    ...                             instrument_code="EUR1M=",
    ...                             tenor="1M",
    ...                             is_non_deliverable=False,
    ...                             quotation_mode=definitions.QuotationMode.OUTRIGHT
    ...                         )
    ...                     )
    ...                 ]
    ...             ),
    ...         )
    ...     ]
    >>> )
    """
    request_items = UpdateRequest(
        curve_definition=curve_definition,
        overrides=overrides,
        segments=segments,
        turns=turns,
    )

    response = _save(
        ContentType.CROSS_CURRENCY_CURVES_DEFINITIONS_UPDATE,
        request_items=request_items,
        extended_params=extended_params,
        session=session,
    )
    return response


def _save(
    content_type: ContentType,
    request_items: UnionSaveRequest,
    extended_params: "ExtendedParams" = None,
    session: "Session" = None,
) -> "Response":
    data_provider_layer = DataProviderLayer(
        data_type=content_type,
        request_items=request_items,
        method=RequestMethod.POST,
        extended_params=extended_params,
    )

    return data_provider_layer.get_data(session=session)
