from .._param_item import param_item
from .._serializable import Serializable


class BasketItem(Serializable):
    def __init__(self, instrument_code=None, currency=None):
        super().__init__()
        self.instrument_code = instrument_code
        self.currency = currency

    def _get_items(self):
        return [
            param_item.to_kv("currency", self.currency),
            param_item.to_kv("instrumentCode", self.instrument_code),
        ]
