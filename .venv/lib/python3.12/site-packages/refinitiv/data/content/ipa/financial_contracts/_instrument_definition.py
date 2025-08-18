import abc

from .._object_definition import ObjectDefinition


class InstrumentDefinition(ObjectDefinition, abc.ABC):
    """
    This class is designed to represent
    the instrument definition templates for QPS request.
    """

    def get_instrument_type(self):
        return ""

    def __init__(self, instrument_tag=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument_tag = instrument_tag

    @property
    def instrument_tag(self):
        """
        User defined string to identify the instrument.It can be used to link output
        results to the instrument definition. Only alphabetic, numeric and '- _.#=@'
        characters are supported. Optional.
        :return: str
        """
        return self._get_parameter("instrumentTag")

    @instrument_tag.setter
    def instrument_tag(self, value):
        try:
            value = value.value
        except Exception:
            # silently
            pass
        self._set_parameter("instrumentTag", value)
