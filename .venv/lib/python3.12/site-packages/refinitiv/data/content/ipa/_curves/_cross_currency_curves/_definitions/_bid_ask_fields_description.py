from typing import Optional

from ._field_formula_description import FieldFormulaDescription
from ...._object_definition import ObjectDefinition


class BidAskFieldsDescription(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    bid : FieldFormulaDescription, optional

    ask : FieldFormulaDescription, optional

    """

    def __init__(
        self,
        bid: Optional[FieldFormulaDescription] = None,
        ask: Optional[FieldFormulaDescription] = None,
    ) -> None:
        super().__init__()
        self.bid = bid
        self.ask = ask

    @property
    def ask(self):
        """
        :return: object FieldFormulaDescription
        """
        return self._get_object_parameter(FieldFormulaDescription, "ask")

    @ask.setter
    def ask(self, value):
        self._set_object_parameter(FieldFormulaDescription, "ask", value)

    @property
    def bid(self):
        """
        :return: object FieldFormulaDescription
        """
        return self._get_object_parameter(FieldFormulaDescription, "bid")

    @bid.setter
    def bid(self, value):
        self._set_object_parameter(FieldFormulaDescription, "bid", value)
