from typing import TYPE_CHECKING

from ._credit_constituents import CreditConstituents
from ...._object_definition import ObjectDefinition
from ._credit_curve_definition import CreditCurveDefinition
from ._credit_curve_parameters import CreditCurveParameters


if TYPE_CHECKING:
    from ......_types import OptStr
    from .._types import CurveDefinition, CurveParameters, OptCreditConstituents


class RequestItem(ObjectDefinition):
    """
    Generates the credit curves for the definition provided

    Parameters
    ----------
    constituents : CreditConstituents, optional

    curve_definition : CreditCurveDefinition, optional

    curve_parameters : CreditCurveParameters, optional

    curve_tag : str, optional
        A user-defined string to identify the interest rate curve. it can be used to
        link output results to the curve definition. limited to 40 characters. only
        alphabetic, numeric and '- _.#=@' characters are supported.
    """

    def __init__(
        self,
        constituents: "OptCreditConstituents" = None,
        curve_definition: "CurveDefinition" = None,
        curve_parameters: "CurveParameters" = None,
        curve_tag: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.constituents = constituents
        self.curve_definition = curve_definition
        self.curve_parameters = curve_parameters
        self.curve_tag = curve_tag

    @property
    def constituents(self):
        """
        :return: object CreditConstituents
        """
        return self._get_object_parameter(CreditConstituents, "constituents")

    @constituents.setter
    def constituents(self, value):
        self._set_object_parameter(CreditConstituents, "constituents", value)

    @property
    def curve_definition(self):
        """
        :return: object CreditCurveDefinition
        """
        return self._get_object_parameter(CreditCurveDefinition, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(CreditCurveDefinition, "curveDefinition", value)

    @property
    def curve_parameters(self):
        """
        :return: object CreditCurveParameters
        """
        return self._get_object_parameter(CreditCurveParameters, "curveParameters")

    @curve_parameters.setter
    def curve_parameters(self, value):
        self._set_object_parameter(CreditCurveParameters, "curveParameters", value)

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
