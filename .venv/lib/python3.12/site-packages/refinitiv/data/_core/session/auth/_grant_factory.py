from typing import TYPE_CHECKING

from ._grant_client_credentials import ClientCredentials
from ._grant_password import GrantPassword
from ._null_grant import NullGrant

if TYPE_CHECKING:
    from . import GrantType


def create_grant(config: dict) -> "GrantType":
    username = config.get("username")
    password = config.get("password")
    client_id = config.get("client_id")
    client_secret = config.get("client_secret")

    if username and password:
        grant = GrantPassword(username, password)

    elif client_id and client_secret:
        grant = ClientCredentials(client_id, client_secret)

    else:
        grant = NullGrant()

    return grant
