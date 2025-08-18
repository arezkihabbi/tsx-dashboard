from typing import Optional

from ._session_type import SessionType
from ... import _configure as configure


def _retrieve_config_and_set_type(session_name, session_type):
    if session_type == SessionType.PLATFORM:
        session_config = configure.get(configure.keys.platform_session(session_name), {})
    elif session_type == SessionType.DESKTOP:
        session_config = configure.get(configure.keys.desktop_session(session_name), {})
    else:
        raise TypeError(f"Invalid session type: {session_type}, please set 'desktop' or 'platform'.")

    if not session_config:
        raise ValueError(f"Can't get config by name: {session_name}. Please check config name")

    return session_config


def _get_session_type_and_name(config_path: str):
    from ._session_provider import get_session_type

    try:
        config_path = config_path or configure.get("sessions.default")
        session_type, session_name = config_path.split(".")

    except ValueError:
        raise ValueError(
            "Please check your 'session_name'. It should be in the following way: 'session_type.session_name'"
        )

    except AttributeError:
        raise AttributeError("Invalid type, please provide string")

    return session_name, get_session_type(session_type)


class Definition(object):
    """
    Defines the sessions (either desktop sessions or platform sessions).

    Parameters
    ----------
    name: str, optional
        Name of the session to create. This name must refer to a session and the
        related parameters defined in the configuration file of the library.
        For example:
            platform.my-session

    Raises
    ----------
    Exception
        1. If user provided invalid session type in session name.
            Type should be 'platform' or 'desktop'
        2. If app-key not found in config and arguments.

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> platform_session = rd.session.Definition(name="platform.my-session").get_session()
    """

    def __init__(self, name: Optional[str] = None) -> None:
        from ._session_provider import _make_session_provider_by_arguments

        self._create_session = _make_session_provider_by_arguments(name)

    def get_session(self):
        """
        Creates and returns the session.

        Returns
        -------
        The instance of the defined session.
        """
        session = self._create_session()
        return session
