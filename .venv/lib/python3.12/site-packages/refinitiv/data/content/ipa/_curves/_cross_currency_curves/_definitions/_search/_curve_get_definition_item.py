from typing import TYPE_CHECKING

from ....._object_definition import ObjectDefinition
from ..._enums import MainConstituentAssetClass, RiskType


if TYPE_CHECKING:
    from ..._types import OptMainConstituentAssetClass, OptRiskType
    from ......._types import OptStr, OptBool, OptDateTime


class CrossCurrencyCurveGetDefinitionItem(ObjectDefinition):
    """
    Returns the definitions of the available commodity and energy forward curves for
    the filters selected (e.g. currency, source…).

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
    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    id : str, optional
        The identifier of the cross currency definitions.
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
    valuation_date : str or date or datetime or timedelta, optional
        The date used to define a list of curves or a unique cross currency curve that
        can be priced at this date. the value is expressed in iso 8601 format:
        yyyy-mm-dd (e.g., '2021-01-01').
    """

    def __init__(
        self,
        main_constituent_asset_class: "OptMainConstituentAssetClass" = None,
        risk_type: "OptRiskType" = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        curve_tag: "OptStr" = None,
        id: "OptStr" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.curve_tag = curve_tag
        self.id = id
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source
        self.valuation_date = valuation_date

    @property
    def main_constituent_asset_class(self):
        """
        The asset class used to generate the zero coupon curve. the possible values are:
        * fxforward   * swap
        :return: enum MainConstituentAssetClass
        """
        return self._get_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass")

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(MainConstituentAssetClass, "mainConstituentAssetClass", value)

    @property
    def risk_type(self):
        """
        The risk type to which the generated cross currency curve is sensitive. the
        possible value is:   * 'crosscurrency'
        :return: enum RiskType
        """
        return self._get_enum_parameter(RiskType, "riskType")

    @risk_type.setter
    def risk_type(self, value):
        self._set_enum_parameter(RiskType, "riskType", value)

    @property
    def base_currency(self):
        """
        The base currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'eur').
        :return: str
        """
        return self._get_parameter("baseCurrency")

    @base_currency.setter
    def base_currency(self, value):
        self._set_parameter("baseCurrency", value)

    @property
    def base_index_name(self):
        """
        The name of the floating rate index (e.g., 'estr') applied to the base currency.
        :return: str
        """
        return self._get_parameter("baseIndexName")

    @base_index_name.setter
    def base_index_name(self, value):
        self._set_parameter("baseIndexName", value)

    @property
    def curve_tag(self):
        """
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
        :return: str
        """
        return self._get_parameter("curveTag")

    @curve_tag.setter
    def curve_tag(self, value):
        self._set_parameter("curveTag", value)

    @property
    def id(self):
        """
        The identifier of the cross currency definitions.
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)

    @property
    def is_non_deliverable(self):
        """
        An indicator whether the instrument is non-deliverable:   * true: the instrument
        is non-deliverable,   * false: the instrument is not non-deliverable. the
        property can be used to retrieve cross currency definition for the adjusted
        interest rate curve.
        :return: bool
        """
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

    @property
    def name(self):
        """
        The fxcross currency pair applied to the reference or pivot currency. it is
        expressed in iso 4217 alphabetical format (e.g., 'eur usd fxcross').
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def quoted_currency(self):
        """
        The quoted currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'usd').
        :return: str
        """
        return self._get_parameter("quotedCurrency")

    @quoted_currency.setter
    def quoted_currency(self, value):
        self._set_parameter("quotedCurrency", value)

    @property
    def quoted_index_name(self):
        """
        The name of the floating rate index (e.g., 'sofr') applied to the quoted
        currency.
        :return: str
        """
        return self._get_parameter("quotedIndexName")

    @quoted_index_name.setter
    def quoted_index_name(self, value):
        self._set_parameter("quotedIndexName", value)

    @property
    def source(self):
        """
        A user-defined string that is provided by the creator of a curve. curves created
        by refinitiv have the 'refinitiv' source.
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)

    @property
    def valuation_date(self):
        """
        The date used to define a list of curves or a unique cross currency curve that
        can be priced at this date. the value is expressed in iso 8601 format:
        yyyy-mm-dd (e.g., '2021-01-01').
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)
