from dataclasses import dataclass
from typing import Any

from ._grant import Grant
from ..tools import Sensitive
from ....errors import RDError

_ARGUMENT_KEY_TO_CONFIG_KEY = {
    "auth_url": "auth.v2.url",
    "auth_token": "auth.v2.token",
}


@dataclass
class ClientCredentials(Grant):
    """
    Parameters
    ----------
    client_id: str
        The client_id to use for authentication
    client_secret: str
        The client_secret to use for authentication
    token_scope: str, list of str (default: trapi)
        The scope to use for authentication

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> rd.session.platform.ClientCredentials(
    ...     client_id="client_id",
    ...     client_secret="client_secret",
    ...     token_scope="token_scope"
    ... )
    or
    >>> import refinitiv.data as rd
    >>> rd.session.platform.ClientCredentials("client_id", "client_secret")
    """

    client_id: str = ""
    client_secret: str = ""
    token_scope: str = "trapi"
    _argument_key_to_config_key = _ARGUMENT_KEY_TO_CONFIG_KEY

    def __post_init__(self):
        if self.is_valid():
            self.client_secret = Sensitive(self.client_secret)
        else:
            raise RDError(-1, "client_id and client_secret can't be empty")

    def is_valid(self):
        return self.client_id and self.client_secret

    def __eq__(self, other: Any):
        if not isinstance(other, ClientCredentials):
            return False
        return self.client_id == other.client_id and self.client_secret == other.client_secret
