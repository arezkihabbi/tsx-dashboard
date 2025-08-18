from ._sts_access_token_updater import STSAccessTokenUpdater
from ._sts_refresh_token_updater import STSRefreshTokenUpdater
from ._sts_token_info import STSTokenInfo
from ._auth_manager import AuthManager
from .revoke_token import revoke_token
from ..event import UpdateEvent


class STSAuthManager(AuthManager):
    token_info_class = STSTokenInfo
    access_token_updater_class = STSAccessTokenUpdater
    refresh_token_updater_class = STSRefreshTokenUpdater

    def close(self):
        """
        The method stops refresh token updater and access token updater
        """
        if self._disposed:
            raise RuntimeError("AuthManager disposed")

        if self.is_closed():
            return

        self.is_debug() and self.debug("AuthManager: close")
        self._result_evt.set()
        self._start_evt.clear()
        self._access_token_updater.stop()
        self._refresh_token_updater.stop()
        self.is_authorized() and revoke_token(self._token_info, self._session)
        self._closed = True
        self._authorized = False
        self._ee.emit(UpdateEvent.CLOSE_AUTH_MANAGER, self)
