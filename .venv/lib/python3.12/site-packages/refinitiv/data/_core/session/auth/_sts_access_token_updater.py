from ._access_token_updater import AccessTokenUpdater


class STSAccessTokenUpdater(AccessTokenUpdater):
    def _get_request_data(self) -> dict:
        grant = self._grant
        data = {
            "scope": grant.get_token_scope(),
            "grant_type": "password",
            "username": grant.get_username(),
            "password": grant.get_password(),
            "takeExclusiveSignOnControl": "true" if self._signon_control else "false",
        }
        app_key = self._app_key
        if app_key is not None:
            data["client_id"] = app_key
        return data
