from typing import List, Tuple, Union

from ..._serializable import Serializable


class Constituents(Serializable):
    def __init__(self):
        super().__init__()

    def _get_items(self) -> List[Tuple[str, Union[str, float, int, None]]]:
        return []
