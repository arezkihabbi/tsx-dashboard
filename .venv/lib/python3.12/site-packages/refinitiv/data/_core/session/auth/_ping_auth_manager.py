from ._ping_access_token_updater import PingAccessTokenUpdater
from ._ping_refresh_token_updater import PingRefreshTokenUpdater
from ._ping_token_info import PingTokenInfo
from ._auth_manager import AuthManager


class PingAuthManager(AuthManager):
    token_info_class = PingTokenInfo
    access_token_updater_class = PingAccessTokenUpdater
    refresh_token_updater_class = PingRefreshTokenUpdater
