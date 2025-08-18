from typing import Optional

from . import CrossCurrencyCurveDefinitionKeys
from ....._object_definition import ObjectDefinition


class GetRequest(ObjectDefinition):
    """
    Get a Commodity & Energy curve definition

    Parameters
    ----------
    curve_definition : CrossCurrencyCurveDefinitionKeys, optional

    """

    def __init__(
        self,
        curve_definition: Optional[CrossCurrencyCurveDefinitionKeys] = None,
    ) -> None:
        super().__init__()
        self.curve_definition = curve_definition

    @property
    def curve_definition(self):
        """
        :return: object CrossCurrencyCurveDefinitionKeys
        """
        return self._get_object_parameter(CrossCurrencyCurveDefinitionKeys, "curveDefinition")

    @curve_definition.setter
    def curve_definition(self, value):
        self._set_object_parameter(CrossCurrencyCurveDefinitionKeys, "curveDefinition", value)
