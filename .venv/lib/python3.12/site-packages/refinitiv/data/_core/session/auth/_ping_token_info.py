from dataclasses import dataclass

from ._token_info import TokenInfo
from ...._tools._delays import HOURS_2


@dataclass
class PingTokenInfo(TokenInfo):
    DEFAULT_EXPIRES_IN_SEC = HOURS_2

    @classmethod
    def from_dict(cls, json_content: dict) -> "TokenInfo":
        return cls(
            access_token=json_content["access_token"],
            expires_in=json_content.get("expires_in", ""),
            scope=set(json_content.get("scope", "").split()),
            token_type=json_content.get("token_type", ""),
        )
