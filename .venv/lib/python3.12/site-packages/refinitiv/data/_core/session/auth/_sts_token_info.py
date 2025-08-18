from dataclasses import dataclass

from ._token_info import TokenInfo


# STS = Security Token Service


@dataclass
class STSTokenInfo(TokenInfo):
    refresh_token: str = ""

    @classmethod
    def from_dict(cls, json_content: dict) -> "TokenInfo":
        return cls(
            access_token=json_content["access_token"],
            refresh_token=json_content["refresh_token"],
            expires_in=json_content.get("expires_in", ""),
            scope=set(json_content.get("scope", "").split()),
            token_type=json_content.get("token_type", ""),
        )

    def update(self, other: "STSTokenInfo") -> None:
        super().update(other)
        self.refresh_token = other.refresh_token
