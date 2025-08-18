import abc
import time
from dataclasses import dataclass, field
from typing import Set, Union

from ...._tools import MINUTES_10, MINUTES_15

DEFAULT_LATENCY_SEC = 20


@dataclass
class TokenInfo(abc.ABC):
    access_token: str = ""
    expires_in: Union[float, str] = 0
    expires_at: float = field(init=False)
    scope: Set[str] = field(default_factory=set)
    token_type: str = ""

    DEFAULT_EXPIRES_IN_SEC = MINUTES_10

    def __post_init__(self):
        self.expires_in = self.calc_expires_in(self.expires_in)
        self.expires_at = time.time() + self.expires_in

    def calc_expires_in(self, expires_in: Union[float, str]) -> float:
        try:
            expires_in = float(expires_in)
            if expires_in <= 0:
                # null and negative values shouldn't be received
                raise ValueError()
        except ValueError:
            expires_in = self.DEFAULT_EXPIRES_IN_SEC
        return expires_in

    def calc_token_update_time(self, latency: float) -> int:
        latency = min(latency, DEFAULT_LATENCY_SEC)

        if self.expires_in < 2 * MINUTES_15:
            expires_secs = self.expires_in / 2
        else:
            expires_secs = self.expires_in - MINUTES_15

        if expires_secs - latency > 0:
            expires_secs = expires_secs - latency

        return int(expires_secs)

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, json_content: dict) -> "TokenInfo":
        pass

    def update(self, other: "TokenInfo") -> None:
        self.access_token = other.access_token
        self.expires_in = other.expires_in
        self.expires_at = other.expires_at
        self.scope = other.scope
        self.token_type = other.token_type
