from ._access_token_updater import AccessTokenUpdater


class PingAccessTokenUpdater(AccessTokenUpdater):
    def _get_request_data(self) -> dict:
        grant = self._grant
        return {
            "scope": grant.token_scope,
            "grant_type": "client_credentials",
            "client_id": grant.client_id,
            "client_secret": grant.client_secret,
        }
