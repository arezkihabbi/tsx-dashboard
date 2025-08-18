"""
This type of session is used to connect directly to the Refinitiv Data Platform or through a Real-Time Distribution
System. If you would like to connect directly to RDP, you require a Refinitiv Data account (either a user account or
a machine account). In both instances, you need to provide Refinitiv data credentials to create the session. If you
would like to work through a Real-Time Distribution System, you need the IP of the local platform and a username (in
other words, a DACS username).
"""

__all__ = ("Definition", "GrantPassword", "ClientCredentials")

from typing import Union as _Union

from .._core.session.auth import GrantPassword, ClientCredentials


class Definition(object):
    """
    Platform session.
    Can be defined indirectly using the name of a session defined
    in the configuration file or directly by specifying the other Definition parameters.

    Parameters
    ----------
    name: str, default "default"
        Session name
    app_key: str, optional
        Application key
    grant: GrantPassword or ClientCredentials object, optional
        Grants objects containing the credentials used to authenticate the user
        (or the machine) when connecting to the data platform.
        Several kind of grant objects can be used, GrantPassword is for STS and ClientCredentials is for Ping.
    signon_control: bool, default True
        Controls the exclusive sign-on behavior when the user account
        (or computer account) for this session is concurrently used by another
        application. When this parameter is set to True, opening this session
        automatically disconnects the other application. When this parameter is set to
        False, the opening of this session fails preserving the other application.
    deployed_platform_host: str, optional
        Host name (or IP) and port to be used to connect to Real-Time Distribution
        System.
    deployed_platform_username: str, optional
        DACS username identifying the user when to connect
        to a Real-Time Distribution System
    dacs_position: str, optional
        DACS position identifying the terminal when connecting to a Real-Time
        Distribution System.
    dacs_application_id: str, optional
        Must contain the user's Data Access Control System application ID.
        For more information, refer to the DACS documentation on my.refinitiv.com
    proxies: str or dict, optional
        Proxies configuration. If string, should be the URL of the proxy
        (e.g. 'https://proxy.com:8080'). If a dict, the keys are the protocol
        name (e.g. 'http', 'https') and the values are the proxy URLs.
    app_name: str, optional
        Application name

    Raises
    ----------
    Exception
        If app-key is not found in the config file and in arguments.

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> definition = rd.session.platform.Definition(name="custom-session-name")
    >>> platform_session = definition.get_session()
    """

    def __init__(
        self,
        name: str = "default",
        app_key: str = None,
        grant: _Union[GrantPassword, ClientCredentials] = None,
        signon_control: bool = None,
        deployed_platform_host: str = None,
        deployed_platform_username: str = None,
        dacs_position: str = None,
        dacs_application_id: str = None,
        proxies: _Union[str, dict] = None,
        app_name: str = None,
    ) -> None:
        from .._core.session._session_provider import _make_platform_session_provider_by_arguments

        if not isinstance(name, str):
            raise ValueError("Invalid session name type, please provide string.")

        if signon_control is None:
            import warnings

            warnings.warn(
                "\nYou open a platform session using the default value of the signon_control parameter (signon_control=True).\n"
                "In future library version v2.0, this default will be changed to False.\n"
                "If you want to keep the same behavior as today, "
                "you will need to set the signon_control parameter to True either in the library configuration file\n"
                "({'sessions':{'platform':{'your_session_name':{'signon_control':true}}}}) or "
                "in your code where you create the Platform Session.\n"
                "These alternative options are already supported in the current version of the library.",
                category=FutureWarning,
            )
            signon_control = True

        self._create_session = _make_platform_session_provider_by_arguments(
            session_name=name,
            app_key=app_key,
            signon_control=signon_control,
            deployed_platform_host=deployed_platform_host,
            deployed_platform_username=deployed_platform_username,
            dacs_position=dacs_position,
            dacs_application_id=dacs_application_id,
            grant=grant,
            proxies=proxies,
            app_name=app_name,
        )

    def get_session(self):
        """
        Creates and returns the session.

        Returns
        -------
        The platform session instance.
        """
        session = self._create_session()
        return session
