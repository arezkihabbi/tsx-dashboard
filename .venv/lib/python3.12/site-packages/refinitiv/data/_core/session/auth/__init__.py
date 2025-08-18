from typing import Union

from ._auth_manager import AuthManager
from ._auth_manager_factory import create_auth_manager
from ._grant_client_credentials import ClientCredentials
from ._grant_factory import create_grant
from ._grant_password import GrantPassword
from ._null_grant import NullGrant

GrantType = Union[GrantPassword, ClientCredentials, NullGrant]
