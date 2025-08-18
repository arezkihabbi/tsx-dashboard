from typing import Optional, Union

from ..._enums import BinaryType, UpOrDown
from ..._param_item import param_item, enum_param_item
from ..._serializable import Serializable


class EtiBinaryDefinition(Serializable):
    """
    Parameters
    ----------
    notional_amount : float, optional

    binary_type : BinaryType or str, optional

    up_or_down : UpOrDown or str, optional

    level : float, optional

    """

    def __init__(
        self,
        notional_amount: Optional[float] = None,
        binary_type: Union[BinaryType, str] = None,
        up_or_down: Union[UpOrDown, str] = None,
        level: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.notional_amount = notional_amount
        self.binary_type = binary_type
        self.up_or_down = up_or_down
        self.level = level

    def _get_items(self):
        return [
            enum_param_item.to_kv("binaryType", self.binary_type),
            enum_param_item.to_kv("upOrDown", self.up_or_down),
            param_item.to_kv("level", self.level),
            param_item.to_kv("notionalAmount", self.notional_amount),
        ]
