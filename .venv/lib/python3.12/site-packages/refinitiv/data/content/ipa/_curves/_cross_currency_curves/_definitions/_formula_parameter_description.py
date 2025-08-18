from typing import Optional, TYPE_CHECKING

from ._bid_ask_fields_formula_description import BidAskFieldsFormulaDescription
from ...._object_definition import ObjectDefinition
from ....curves._enums import InstrumentType

if TYPE_CHECKING:
    from ......_types import OptStr


class FormulaParameterDescription(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    instrument_type : InstrumentType, optional

    instrument_code : str, optional

    fields : BidAskFieldsFormulaDescription, optional

    name : str, optional

    """

    def __init__(
        self,
        instrument_type: Optional[InstrumentType] = None,
        instrument_code: "OptStr" = None,
        fields: Optional[BidAskFieldsFormulaDescription] = None,
        name: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.instrument_type = instrument_type
        self.instrument_code = instrument_code
        self.fields = fields
        self.name = name

    @property
    def fields(self):
        """
        :return: object BidAskFieldsFormulaDescription
        """
        return self._get_object_parameter(BidAskFieldsFormulaDescription, "fields")

    @fields.setter
    def fields(self, value):
        self._set_object_parameter(BidAskFieldsFormulaDescription, "fields", value)

    @property
    def instrument_type(self):
        """
        :return: enum InstrumentType
        """
        return self._get_enum_parameter(InstrumentType, "instrumentType")

    @instrument_type.setter
    def instrument_type(self, value):
        self._set_enum_parameter(InstrumentType, "instrumentType", value)

    @property
    def instrument_code(self):
        """
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def name(self):
        """
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)
