from typing import Optional, TYPE_CHECKING, List

from ._curve_definition_pricing import CrossCurrencyCurveDefinitionPricing
from ...._object_definition import ObjectDefinition
from ....curves.zc_curve_definitions._zc_curve_definition import ZcCurveDefinition
from ......_tools import try_copy_to_list

if TYPE_CHECKING:
    from ......_types import OptStr, OptBool, OptStrings


class FxForwardCurveDefinition(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    cross_currency_definitions : list of CrossCurrencyCurveDefinitionPricing, optional

    curve_tenors : string, optional
        List of user-defined curve tenors or dates to be computed.
    interest_rate_curve_definitions : list of ZcCurveDefinition, optional

    base_currency : str, optional

    base_index_name : str, optional

    is_non_deliverable : bool, optional
        If true, non deliverable cross currency definition is used. default value is
        false
    pivot_currency : str, optional

    pivot_index_name : str, optional

    quoted_currency : str, optional

    quoted_index_name : str, optional

    """

    def __init__(
        self,
        cross_currency_definitions: Optional[List[CrossCurrencyCurveDefinitionPricing]] = None,
        curve_tenors: "OptStrings" = None,
        interest_rate_curve_definitions: Optional[List[ZcCurveDefinition]] = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        is_non_deliverable: "OptBool" = None,
        pivot_currency: "OptStr" = None,
        pivot_index_name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.cross_currency_definitions = try_copy_to_list(cross_currency_definitions)
        self.curve_tenors = curve_tenors
        self.interest_rate_curve_definitions = try_copy_to_list(interest_rate_curve_definitions)
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.is_non_deliverable = is_non_deliverable
        self.pivot_currency = pivot_currency
        self.pivot_index_name = pivot_index_name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name

    @property
    def cross_currency_definitions(self):
        """
        :return: list CrossCurrencyCurveDefinitionPricing
        """
        return self._get_list_parameter(CrossCurrencyCurveDefinitionPricing, "crossCurrencyDefinitions")

    @cross_currency_definitions.setter
    def cross_currency_definitions(self, value):
        self._set_list_parameter(CrossCurrencyCurveDefinitionPricing, "crossCurrencyDefinitions", value)

    @property
    def curve_tenors(self):
        """
        List of user-defined curve tenors or dates to be computed.
        :return: list string
        """
        return self._get_list_parameter(str, "curveTenors")

    @curve_tenors.setter
    def curve_tenors(self, value):
        self._set_list_parameter(str, "curveTenors", value)

    @property
    def interest_rate_curve_definitions(self):
        """
        :return: list ZcCurveDefinition
        """
        return self._get_list_parameter(ZcCurveDefinition, "interestRateCurveDefinitions")

    @interest_rate_curve_definitions.setter
    def interest_rate_curve_definitions(self, value):
        self._set_list_parameter(ZcCurveDefinition, "interestRateCurveDefinitions", value)

    @property
    def base_currency(self):
        """
        :return: str
        """
        return self._get_parameter("baseCurrency")

    @base_currency.setter
    def base_currency(self, value):
        self._set_parameter("baseCurrency", value)

    @property
    def base_index_name(self):
        """
        :return: str
        """
        return self._get_parameter("baseIndexName")

    @base_index_name.setter
    def base_index_name(self, value):
        self._set_parameter("baseIndexName", value)

    @property
    def is_non_deliverable(self):
        """
        If true, non deliverable cross currency definition is used. default value is
        false
        :return: bool
        """
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

    @property
    def pivot_currency(self):
        """
        :return: str
        """
        return self._get_parameter("pivotCurrency")

    @pivot_currency.setter
    def pivot_currency(self, value):
        self._set_parameter("pivotCurrency", value)

    @property
    def pivot_index_name(self):
        """
        :return: str
        """
        return self._get_parameter("pivotIndexName")

    @pivot_index_name.setter
    def pivot_index_name(self, value):
        self._set_parameter("pivotIndexName", value)

    @property
    def quoted_currency(self):
        """
        :return: str
        """
        return self._get_parameter("quotedCurrency")

    @quoted_currency.setter
    def quoted_currency(self, value):
        self._set_parameter("quotedCurrency", value)

    @property
    def quoted_index_name(self):
        """
        :return: str
        """
        return self._get_parameter("quotedIndexName")

    @quoted_index_name.setter
    def quoted_index_name(self, value):
        self._set_parameter("quotedIndexName", value)
