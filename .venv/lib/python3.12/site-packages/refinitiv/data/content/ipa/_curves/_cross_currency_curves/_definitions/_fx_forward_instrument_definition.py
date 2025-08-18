from typing import Optional, TYPE_CHECKING

from ...._object_definition import ObjectDefinition
from ._enums import QuotationMode

if TYPE_CHECKING:
    from ......_types import OptStr, OptBool


class FxForwardInstrumentDefinition(ObjectDefinition):
    """
    Creates the Cross Currency curve definition with the definition provided.

    Parameters
    ----------
    instrument_code : str, optional
        The code used to define the instrument.
    tenor : str, optional
        The code indicating the instrument tenor (e.g., '6m', '1y').
    quotation_mode : QuotationMode, optional
        The quotation defining the price type of the instrument. the possible values
        are:   * swappoint   * outright
    is_non_deliverable : bool, optional
        True if the instrument is non deliverable
    synthetic_instrument_code : str, optional
        The code used to define the formula.
    template : str, optional
        A reference to a style used to define the instrument.
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        tenor: "OptStr" = None,
        quotation_mode: Optional[QuotationMode] = None,
        is_non_deliverable: "OptBool" = None,
        synthetic_instrument_code: "OptStr" = None,
        template: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code
        self.tenor = tenor
        self.quotation_mode = quotation_mode
        self.is_non_deliverable = is_non_deliverable
        self.synthetic_instrument_code = synthetic_instrument_code
        self.template = template

    @property
    def quotation_mode(self):
        """
        The quotation defining the price type of the instrument. the possible values
        are:   * swappoint   * outright
        :return: enum QuotationMode
        """
        return self._get_enum_parameter(QuotationMode, "quotationMode")

    @quotation_mode.setter
    def quotation_mode(self, value):
        self._set_enum_parameter(QuotationMode, "quotationMode", value)

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
    def is_non_deliverable(self):
        """
        True if the instrument is non deliverable
        :return: bool
        """
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

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

    @property
    def tenor(self):
        """
        The code indicating the instrument tenor (e.g., '6m', '1y').
        :return: str
        """
        return self._get_parameter("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_parameter("tenor", value)
