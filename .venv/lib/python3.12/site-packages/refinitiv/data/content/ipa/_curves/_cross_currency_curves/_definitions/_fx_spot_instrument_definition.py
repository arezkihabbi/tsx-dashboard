from typing import TYPE_CHECKING

from ...._object_definition import ObjectDefinition

if TYPE_CHECKING:
    from ......_types import OptStr


class FxSpotInstrumentDefinition(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    instrument_code : str, optional
        The code used to define the instrument.
    synthetic_instrument_code : str, optional
        The code used to define the formula.
    template : str, optional
        A reference to a style used to define the instrument.
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        synthetic_instrument_code: "OptStr" = None,
        template: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code
        self.synthetic_instrument_code = synthetic_instrument_code
        self.template = template

    @property
    def instrument_code(self):
        """
        The code used to define the instrument.
        :return: str
        """
        return self._get_parameter("instrumentCode")

    @instrument_code.setter
    def instrument_code(self, value):
        self._set_parameter("instrumentCode", value)

    @property
    def synthetic_instrument_code(self):
        """
        The code used to define the formula.
        :return: str
        """
        return self._get_parameter("syntheticInstrumentCode")

    @synthetic_instrument_code.setter
    def synthetic_instrument_code(self, value):
        self._set_parameter("syntheticInstrumentCode", value)

    @property
    def template(self):
        """
        A reference to a style used to define the instrument.
        :return: str
        """
        return self._get_parameter("template")

    @template.setter
    def template(self, value):
        self._set_parameter("template", value)
