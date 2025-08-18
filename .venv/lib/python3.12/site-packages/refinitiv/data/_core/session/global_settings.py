class GlobalSettings(object):
    def __init__(self, *args, **kwargs):
        self._edp_user = kwargs.get("edp_user")
        self._edp_pwd = kwargs.get("edp_password")
        self._app_key = kwargs.get("app_key")
        self._trep_host = kwargs.get("trep_host")

    def edp_user(self):
        return self._edp_user

    def edp_password(self):
        return self._edp_pwd

    def app_key(self):
        return self._app_key

    def trep_host(self):
        return self._trep_host
