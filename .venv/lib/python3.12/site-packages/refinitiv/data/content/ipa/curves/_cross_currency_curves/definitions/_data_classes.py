from dataclasses import dataclass
from typing import TYPE_CHECKING

from .._arg_enums import main_constituent_asset_class_arg_parser, risk_type_arg_parser
from .._base_data_class import BaseData
from ......delivery._data._endpoint_data import EndpointData

if TYPE_CHECKING:
    from ......_types import OptStr, OptBool, OptDateTime
    from ...._curves._cross_currency_curves._types import (
        OptMainConstituentAssetClass,
        OptRiskType,
    )


curve_info_camel_to_snake = {
    "creationDateTime": "creation_date_time",
    "creationUserId": "creation_user_id",
    "updateDateTime": "update_date_time",
    "updateUserId": "update_user_id",
    "version": "version",
}

curve_definition_camel_to_snake = {
    "mainConstituentAssetClass": "main_constituent_asset_class",
    "riskType": "risk_type",
    "baseCurrency": "base_currency",
    "baseIndexName": "base_index_name",
    "definitionExpiryDate": "definition_expiry_date",
    "firstHistoricalAvailabilityDate": "first_historical_availability_date",
    "id": "id",
    "isFallbackForFxCurveDefinition": "is_fallback_for_fx_curve_definition",
    "isNonDeliverable": "is_non_deliverable",
    "name": "name",
    "quotedCurrency": "quoted_currency",
    "quotedIndexName": "quoted_index_name",
    "source": "source",
}


def convert_camel_to_snake(mapper: dict, data: dict) -> dict:
    return {mapper.get(name, name): value for name, value in data.items()}


class CurveInfo(BaseData):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    creation_date_time : str, optional

    creation_user_id : str, optional

    update_date_time : str, optional

    update_user_id : str, optional

    version : str, optional

    """

    def __init__(
        self,
        creation_date_time: "OptStr" = None,
        creation_user_id: "OptStr" = None,
        update_date_time: "OptStr" = None,
        update_user_id: "OptStr" = None,
        version: "OptStr" = None,
        **kwargs,
    ):
        self.creation_date_time = creation_date_time
        self.creation_user_id = creation_user_id
        self.update_date_time = update_date_time
        self.update_user_id = update_user_id
        self.version = version
        super().__init__(**kwargs)


class CrossCurrencyCurveDefinition(BaseData):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
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
    definition_expiry_date : str or date or datetime or timedelta, optional
        The date after which curvedefinitions can not be used. the value is expressed in
        iso 8601 format: yyyy-mm-dd (e.g., '2021-01-01').
    first_historical_availability_date : str, optional
        The date starting from which cross currency curve definition can be used. the
        value is expressed in iso 8601 format: yyyy-mm-dd (e.g., '2021-01-01').
    id : str, optional
        The identifier of the cross currency curve.
    is_fallback_for_fx_curve_definition : bool, optional
        The indicator used to define the fallback logic for the fx curve definition. the
        possible values are:   * true: there's a fallback logic to use cross currency
        curve definition for fx curve definition,   * false: there's no fallback logic
        to use cross currency curve definition for fx curve definition.
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
    """

    def __init__(
        self,
        main_constituent_asset_class: "OptMainConstituentAssetClass" = None,
        risk_type: "OptRiskType" = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        definition_expiry_date: "OptDateTime" = None,
        first_historical_availability_date: "OptStr" = None,
        id: "OptStr" = None,
        is_fallback_for_fx_curve_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
        **kwargs,
    ):
        self.main_constituent_asset_class = main_constituent_asset_class_arg_parser.get_enum(
            main_constituent_asset_class
        )
        self.risk_type = risk_type_arg_parser.get_enum(risk_type)
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.definition_expiry_date = definition_expiry_date
        self.first_historical_availability_date = first_historical_availability_date
        self.id = id
        self.is_fallback_for_fx_curve_definition = is_fallback_for_fx_curve_definition
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source
        super().__init__(**kwargs)


@dataclass
class CurveDefinitionData(EndpointData):
    _curve_definition: CrossCurrencyCurveDefinition = None
    _curve_info: CurveInfo = None

    @property
    def curve_definition(self):
        if self._curve_definition is None:
            curve_definition = self.raw.get("curveDefinition")
            if curve_definition:
                curve_definition = convert_camel_to_snake(curve_definition_camel_to_snake, curve_definition)
            self._curve_definition = CrossCurrencyCurveDefinition(**curve_definition)
        return self._curve_definition

    @property
    def curve_info(self):
        if self._curve_info is None:
            curve_info = self.raw.get("curveInfo")
            if curve_info:
                curve_info = convert_camel_to_snake(curve_info_camel_to_snake, curve_info)
            self._curve_info = CurveInfo(**curve_info)
        return self._curve_info
