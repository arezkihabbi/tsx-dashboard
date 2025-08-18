from typing import TYPE_CHECKING

from ...._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ......_types import OptFloat


class FxForwardTurnFields(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    bid : float, optional

    ask : float, optional

    """

    def __init__(self, bid: "OptFloat" = None, ask: "OptFloat" = None) -> None:
        super().__init__()
        self.bid = bid
        self.ask = ask

    @property
    def ask(self):
        """
        :return: float
        """
        return self._get_parameter("ask")

    @ask.setter
    def ask(self, value):
        self._set_parameter("ask", value)

    @property
    def bid(self):
        """
        :return: float
        """
        return self._get_parameter("bid")

    @bid.setter
    def bid(self, value):
        self._set_parameter("bid", value)
