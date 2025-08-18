from typing import Optional, TYPE_CHECKING

from ._bid_ask_fields_description import BidAskFieldsDescription
from ._formula_parameter_description import FormulaParameterDescription
from ._fx_forward_instrument_definition import FxForwardInstrumentDefinition
from ...._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ......_types import OptStr


class FxForwardInstrumentDescription(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    fields : BidAskFieldsDescription, optional

    formula_parameters : FormulaParameterDescription, optional

    instrument_definition : FxForwardInstrumentDefinition, optional

    formula : str, optional

    """

    def __init__(
        self,
        fields: Optional[BidAskFieldsDescription] = None,
        formula_parameters: Optional[FormulaParameterDescription] = None,
        instrument_definition: Optional[FxForwardInstrumentDefinition] = None,
        formula: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.fields = fields
        self.formula_parameters = formula_parameters
        self.instrument_definition = instrument_definition
        self.formula = formula

    @property
    def fields(self):
        """
        :return: object BidAskFieldsDescription
        """
        return self._get_object_parameter(BidAskFieldsDescription, "fields")

    @fields.setter
    def fields(self, value):
        self._set_object_parameter(BidAskFieldsDescription, "fields", value)

    @property
    def formula_parameters(self):
        """
        :return: list FormulaParameterDescription
        """
        return self._get_list_parameter(FormulaParameterDescription, "formulaParameters")

    @formula_parameters.setter
    def formula_parameters(self, value):
        self._set_list_parameter(FormulaParameterDescription, "formulaParameters", value)

    @property
    def instrument_definition(self):
        """
        :return: object FxForwardInstrumentDefinition
        """
        return self._get_object_parameter(FxForwardInstrumentDefinition, "instrumentDefinition")

    @instrument_definition.setter
    def instrument_definition(self, value):
        self._set_object_parameter(FxForwardInstrumentDefinition, "instrumentDefinition", value)

    @property
    def formula(self):
        """
        :return: str
        """
        return self._get_parameter("formula")

    @formula.setter
    def formula(self, value):
        self._set_parameter("formula", value)
