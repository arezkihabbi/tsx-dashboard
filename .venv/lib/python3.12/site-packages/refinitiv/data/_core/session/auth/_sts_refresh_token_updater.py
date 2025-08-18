from ._refresh_token_updater import RefreshTokenUpdater


class STSRefreshTokenUpdater(RefreshTokenUpdater):
    def _get_request_data(self) -> dict:
        return {
            "client_id": self._app_key,
            "grant_type": "refresh_token",
            "username": self._grant.get_username(),
            "refresh_token": self._token_info.refresh_token,
        }
