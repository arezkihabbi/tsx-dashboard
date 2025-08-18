from ..._param_item import param_item
from ..._serializable import Serializable


class Instrument(Serializable):
    def __init__(self, instrument_code=None, value=None):
        super().__init__()
        self.instrument_code = instrument_code
        self.value = value

    def _get_items(self):
        return [
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("value", self.value),
        ]
