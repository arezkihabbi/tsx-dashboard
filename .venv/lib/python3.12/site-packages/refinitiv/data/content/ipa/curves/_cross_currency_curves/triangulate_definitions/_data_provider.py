from dataclasses import dataclass
from typing import List, TYPE_CHECKING

from .._arg_enums import main_constituent_asset_class_arg_parser, risk_type_arg_parser
from .._base_data_class import BaseData
from ......delivery._data._endpoint_data import EndpointData

if TYPE_CHECKING:
    from ...._curves._cross_currency_curves._types import (
        OptMainConstituentAssetClass,
        OptRiskType,
    )
    from ......_types import OptStr, OptBool

_camel_to_snake = {
    "mainConstituentAssetClass": "main_constituent_asset_class",
    "riskType": "risk_type",
    "baseCurrency": "base_currency",
    "baseIndexName": "base_index_name",
    "id": "id",
    "isFallbackForFxCurveDefinition": "is_fallback_for_fx_curve_definition",
    "isNonDeliverable": "is_non_deliverable",
    "name": "name",
    "quotedCurrency": "quoted_currency",
    "quotedIndexName": "quoted_index_name",
    "source": "source",
}


def convert_camel_to_snake(data: dict) -> dict:
    return {_camel_to_snake.get(name, name): value for name, value in data.items()}


class CurveDefinitionTriangulate(BaseData):
    """
    Gets the Cross Currency curve definitions who can be used with provided criterias.

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
    id : str, optional
        The identifier of the cross currency definitions.
    is_fallback_for_fx_curve_definition : bool, optional

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
        self.id = id
        self.is_fallback_for_fx_curve_definition = is_fallback_for_fx_curve_definition
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source
        super().__init__(**kwargs)


class CurveDefinition:
    def __init__(self, **kwargs):
        self._direct_curve_definitions = None
        self._indirect_curve_definitions = None
        self._kwargs = kwargs

    @property
    def direct_curve_definitions(self):
        if self._direct_curve_definitions is None:
            self._direct_curve_definitions = []
            direct_curves = self._kwargs.get("directCurveDefinitions")
            self._direct_curve_definitions = self._create_list_definition_triangulates(direct_curves)
        return self._direct_curve_definitions

    @property
    def indirect_curve_definitions(self):
        if self._indirect_curve_definitions is None:
            self._indirect_curve_definitions = []
            indirect_curves = self._kwargs.get("indirectCurveDefinitions")
            for indirect_curve in indirect_curves:
                cross_currencies = indirect_curve.get("crossCurrencyDefinitions", [])
                list_triangulates = self._create_list_definition_triangulates(cross_currencies)
                self._indirect_curve_definitions.append(list_triangulates)
        return self._indirect_curve_definitions

    @property
    def curve_tag(self):
        return self._kwargs.get("curveTag")

    def _create_list_definition_triangulates(self, items: list):
        return [CurveDefinitionTriangulate(**convert_camel_to_snake(item)) for item in items]


@dataclass
class TriangulateDefinitionsData(EndpointData):
    _curve_definitions: List[CurveDefinition] = None

    @property
    def curve_definitions(self):
        if self._curve_definitions is None:
            self._curve_definitions = [CurveDefinition(**item) for item in self.raw.get("data", [])]
        return self._curve_definitions
