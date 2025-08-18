from ._refresh_token_updater import RefreshTokenUpdater


class PingRefreshTokenUpdater(RefreshTokenUpdater):
    def _get_request_data(self) -> dict:
        grant = self._grant
        return {
            "scope": grant.token_scope,
            "grant_type": "client_credentials",
            "client_id": grant.client_id,
            "client_secret": grant.client_secret,
        }
