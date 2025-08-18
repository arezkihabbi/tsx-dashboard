from typing import TYPE_CHECKING

from ._grant_client_credentials import ClientCredentials
from ._grant_password import GrantPassword
from ._ping_auth_manager import PingAuthManager
from ._sts_auth_manager import STSAuthManager

if TYPE_CHECKING:
    from ._auth_manager import AuthManager
    from .._platform_session import PlatformSession


def create_auth_manager(session: "PlatformSession", server_mode: bool) -> "AuthManager":
    grant = session._grant
    if isinstance(grant, GrantPassword):
        return STSAuthManager(session, server_mode)
    elif isinstance(grant, ClientCredentials):
        return PingAuthManager(session, server_mode)
    else:
        raise ValueError(f"Cannot create auth manager, unknown grant type {type(grant)}")
