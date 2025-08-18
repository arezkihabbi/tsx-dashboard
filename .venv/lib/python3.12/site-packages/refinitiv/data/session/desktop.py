"""
This type of session is used to connect to the Refinitiv Data Platform through Refinitiv Eikon or Refinitiv Workspace.
It requires Refinitiv Eikon or Refinitiv Workspace to be running alongside your application. This type of session does
not work with Refinitiv Eikon Web or Refinitiv Workspace for Web.
"""

__all__ = ("Definition",)


class Definition(object):
    """
    Desktop session.
    Can be defined indirectly using the name of a session defined in
    the configuration file or directly by specifying the app_key parameter.

    Parameters
    ----------
    name: str, default "workspace"
        Name of the session in the config file.
    app_key: str, optional
        Application key.
    app_name: str, optional
        Application name.

    Raises
    ---------
    Exception
        If app-key is not found in the config file and in arguments.

    Examples
    --------
    >>> from refinitiv.data import session
    >>> definition = session.desktop.Definition(name="custom-session-name")
    >>> desktop_session = definition.get_session()
    """

    def __init__(
        self,
        name: str = "workspace",
        app_key: str = None,
        app_name: str = None,
    ):
        from .._core.session._session_provider import _make_desktop_session_provider_by_arguments

        if not isinstance(name, str):
            raise ValueError("Invalid session name type, please provide string.")

        self._create_session = _make_desktop_session_provider_by_arguments(
            session_name=name,
            app_key=app_key,
            app_name=app_name,
        )

    def get_session(self):
        """
        Creates and returns the session.

        Returns
        -------
        The desktop session instance.
        """
        session = self._create_session()
        return session
