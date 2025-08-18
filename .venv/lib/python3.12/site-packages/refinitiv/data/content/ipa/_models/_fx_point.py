from .._enums import Status
from .._param_item import enum_param_item, param_item
from .._serializable import Serializable


class FxPoint(Serializable):
    def __init__(
        self,
        bid=None,
        ask=None,
        mid=None,
        status: Status = None,
        instrument=None,
        processing_information=None,
        spot_decimals=None,
    ):
        super().__init__()
        self.bid = bid
        self.ask = ask
        self.mid = mid
        self.status = status
        self.instrument = instrument
        self.processing_information = processing_information
        self.spot_decimals = spot_decimals

    def _get_items(self):
        return [
            enum_param_item.to_kv("status", self.status),
            param_item.to_kv("ask", self.ask),
            param_item.to_kv("bid", self.bid),
            param_item.to_kv("instrument", self.instrument),
            param_item.to_kv("mid", self.mid),
            param_item.to_kv("processingInformation", self.processing_information),
            param_item.to_kv("spotDecimals", self.spot_decimals),
        ]
