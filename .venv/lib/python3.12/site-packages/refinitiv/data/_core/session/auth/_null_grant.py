from typing import Any

from ._grant import Grant


class NullGrant(Grant):
    def is_valid(self) -> bool:
        return False

    def __eq__(self, other: Any):
        if not isinstance(other, NullGrant):
            return False
        return True
