from .._param_item import param_item, datetime_param_item

from .._serializable import Serializable


class DayWeight(Serializable):
    def __init__(self, date=None, weight=None):
        super().__init__()
        self.date = date
        self.weight = weight

    def _get_items(self):
        return [
            datetime_param_item.to_kv("date", self.date),
            param_item.to_kv("weight", self.weight),
        ]
