"""Session functions."""
import warnings
from typing import Optional, TYPE_CHECKING

from .._configure import load_config, get_config
from .._core.session import Definition
from .._core.session import get_default, set_default, is_open, is_closed
from .._core.session.tools import is_platform_session
from .._log import root_logger

if TYPE_CHECKING:
    from .._core.session import Session


def open_session(
    name: Optional[str] = None,
    app_key: Optional[str] = None,
    config_name: Optional[str] = None,
) -> "Session":
    """
    Opens and returns a session.

    Parameters
    ----------
    name: str, optional
        Session name from the config file.
    app_key: str, optional
        The application key.
    config_name: str, optional
        The config name. If provided, overrides default config.

    Returns
    -------
    Session
    """
    # Because it's a path in configuration profile, not a session name,
    # but we can't change argument name, because it's a public API
    config_path = name
    del name

    if config_name:
        config_object = load_config(config_name)

    else:
        config_object = get_config()

    name = config_path or config_object.get_param("sessions.default")

    try:
        config_object.get_param(f"sessions.{name}")
    except Exception:
        config_name = f" {config_name}" if config_name else ""
        raise NameError(
            f"Cannot open session {name}\nThis session is not defined in the{config_name} configuration file"
        )

    if app_key:
        config_object.set_param(param=f"sessions.{name}.app-key", value=app_key, auto_create=True)

    new_session = Definition(name=name).get_session()

    if is_platform_session(new_session):
        signon_control_key = f"sessions.{name}.signon_control"
        is_raise_warn = True
        for cfg in config_object.configs[:-1]:
            if signon_control_key in cfg:
                is_raise_warn = False
                break

        if is_raise_warn:
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

    try:
        default_session = get_default()
        if default_session != new_session:
            set_default(new_session)
            default_session = new_session
    except AttributeError:
        set_default(new_session)
        default_session = new_session

    default_session.open()

    return default_session


def close_session() -> None:
    """
    Closes the previously opened session.

    Returns
    -------
    None
    """
    try:
        default_session = get_default()
    except AttributeError:
        root_logger().info("Nо default session to close")
    else:
        if is_open(default_session):
            default_session.info("Closing session")
            default_session.close()
        if is_closed(default_session):
            default_session.info("Session is closed")
