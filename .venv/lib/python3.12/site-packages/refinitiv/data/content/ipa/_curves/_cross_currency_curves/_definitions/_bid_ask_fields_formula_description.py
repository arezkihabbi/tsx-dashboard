from typing import Optional

from ._field_description import FieldDescription
from ...._object_definition import ObjectDefinition


class BidAskFieldsFormulaDescription(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    bid : FieldDescription, optional

    ask : FieldDescription, optional

    """

    def __init__(
        self,
        bid: Optional[FieldDescription] = None,
        ask: Optional[FieldDescription] = None,
    ) -> None:
        super().__init__()
        self.bid = bid
        self.ask = ask

    @property
    def ask(self):
        """
        :return: object FieldDescription
        """
        return self._get_object_parameter(FieldDescription, "ask")

    @ask.setter
    def ask(self, value):
        self._set_object_parameter(FieldDescription, "ask", value)

    @property
    def bid(self):
        """
        :return: object FieldDescription
        """
        return self._get_object_parameter(FieldDescription, "bid")

    @bid.setter
    def bid(self, value):
        self._set_object_parameter(FieldDescription, "bid", value)
