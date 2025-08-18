from typing import TYPE_CHECKING

from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptStr, OptDateTime


class RequestItem(ObjectDefinition):
    """
    Gets the Cross Currency curve definitions who can be used with provided criterias.

    Parameters
    ----------
    base_currency : str, optional

    base_index_name : str, optional

    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    quoted_currency : str, optional

    quoted_index_name : str, optional

    valuation_date : str or date or datetime or timedelta, optional
        The date used to define a list of curves or a unique curve that can be priced
        at this date. The value is expressed in ISO 8601 format: YYYY-MM-DD

    """

    def __init__(
        self,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        curve_tag: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        valuation_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.curve_tag = curve_tag
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.valuation_date = valuation_date

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

    @property
    def valuation_date(self):
        """
        :return: str
        """
        return self._get_parameter("valuationDate")

    @valuation_date.setter
    def valuation_date(self, value):
        self._set_date_parameter("valuationDate", value)
