from typing import Union

from ._desktop_session import DesktopSession
from ._platform_session import PlatformSession
from ._session_type import SessionType
from .auth import GrantType, create_grant
from ... import _configure as configure
from ..._external_libraries import python_configuration as ext_config_mod  # noqa

CANNOT_FIND_APP_KEY = "Can't find 'app-key' in config object."

DEPLOYED_PLATFORM_URL_CONFIG_KEY = "realtime-distribution-system.url"
DEPLOYED_PLATFORM_USER_CONFIG_KEY = "realtime-distribution-system.dacs.username"
DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY = "realtime-distribution-system.dacs.position"
DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY = "realtime-distribution-system.dacs.application-id"

PLATFORM_ARGUMENT_KEY_TO_CONFIG_KEY = {
    "app_key": "app-key",
    "signon_control": "signon_control",
    "deployed_platform_host": DEPLOYED_PLATFORM_URL_CONFIG_KEY,
    "deployed_platform_username": DEPLOYED_PLATFORM_USER_CONFIG_KEY,
    "dacs_position": DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY,
    "dacs_application_id": DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY,
    "realtime_distribution_system_url": DEPLOYED_PLATFORM_URL_CONFIG_KEY,
    "auto_reconnect": "auto-reconnect",
    "server_mode": "server-mode",
    "base_url": "base-url",
    "revoke_url": "auth.revoke",
    "app_name": "app-name",
}

DESKTOP_ARGUMENT_KEY_TO_CONFIG_KEY = {
    "app_key": "app-key",
    "token": "token",
    "dacs_position": DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY,
    "dacs_application_id": DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY,
    "base_url": "base-url",
    "platform_path_rdp": "platform-paths.rdp",
    "platform_path_udf": "platform-paths.udf",
    "handshake_url": "handshake-url",
    "app_name": "app-name",
}

session_class_by_session_type = {
    SessionType.DESKTOP: DesktopSession,
    SessionType.PLATFORM: PlatformSession,
}

session_alias_by_session_type = {
    "platform": SessionType.PLATFORM,
    "desktop": SessionType.DESKTOP,
}


def get_session_type(value: Union[SessionType, str]):
    session_type = None

    if isinstance(value, SessionType):
        session_type = value

    elif isinstance(value, str):
        session_type = session_alias_by_session_type.get(value)

    if not session_type:
        raise ValueError(f"Cannot get session type by value:{value}")

    return session_type


def _retrieve_values_from_config(config, session_type, grant):
    arguments = {}
    if session_type == SessionType.PLATFORM:
        grant = grant or create_grant(config)
        arguments["grant"] = grant

        grant._update_session_arguments(arguments, config)
        for argument, value in PLATFORM_ARGUMENT_KEY_TO_CONFIG_KEY.items():
            arguments[argument] = config.get(value)

    else:
        for argument, value in DESKTOP_ARGUMENT_KEY_TO_CONFIG_KEY.items():
            arguments[argument] = config.get(value)

    return arguments


def _validate_platform_session_arguments(
    app_key: str = None,
    grant: "GrantType" = None,
    deployed_platform_host=None,
    deployed_platform_username=None,
):
    if app_key == "":
        raise AttributeError(CANNOT_FIND_APP_KEY)

    if app_key is None:
        raise AttributeError(
            "Please, set app-key in [session.platform.default] section of "
            "the config file or provide 'app-key' attribute to the definition."
        )

    if not grant.is_valid() and (not deployed_platform_host or not deployed_platform_username):
        raise AttributeError(
            "To create platform session, please provide 'grant' attribute to the "
            "definition or set 'username' and 'password' or 'client_id' and 'client_secret' in the config file. "
            "To create deployed session, please provide 'deployed_platform_host' "
            "and 'deployed_platform_username' to the definition or the config file."
        )


def _make_platform_session_provider_by_arguments(
    session_name,
    app_key=None,
    signon_control=None,
    deployed_platform_host=None,
    deployed_platform_username=None,
    dacs_position=None,
    dacs_application_id=None,
    grant=None,
    proxies=None,
    app_name=None,
):
    session_config = configure.get(configure.keys.platform_session(session_name), {})
    default_session_config = configure.get(configure.keys.platform_session("default"), {})

    if isinstance(session_config, dict) and len(session_config) == 0:
        raise ValueError(f"Session name: {session_name} is invalid or session_name object is empty")

    arguments = {
        "app-key": app_key,
        "app-name": app_name,
        "signon_control": signon_control,
        DEPLOYED_PLATFORM_URL_CONFIG_KEY: deployed_platform_host,
        DEPLOYED_PLATFORM_USER_CONFIG_KEY: deployed_platform_username,
        DEPLOYED_PLATFORM_DACS_POS_CONFIG_KEY: dacs_position,
        DEPLOYED_PLATFORM_DACS_ID_CONFIG_KEY: dacs_application_id,
    }
    filtered_arguments = {key: value for key, value in arguments.items() if value is not None}

    merged_config = ext_config_mod.ConfigurationSet(
        ext_config_mod.config_from_dict(filtered_arguments),
        session_config,
        default_session_config,
    )

    app_key = merged_config.get("app-key")
    app_name = merged_config.get("app-name")
    deployed_platform_host = merged_config.get(DEPLOYED_PLATFORM_URL_CONFIG_KEY)
    deployed_platform_username = merged_config.get(DEPLOYED_PLATFORM_USER_CONFIG_KEY)
    grant = grant or create_grant(merged_config)

    _validate_platform_session_arguments(
        app_key=app_key,
        grant=grant,
        deployed_platform_host=deployed_platform_host,
        deployed_platform_username=deployed_platform_username,
    )

    return make_session_provider(SessionType.PLATFORM, merged_config, grant, session_name, proxies, app_name)


def _validate_desktop_session_app_key(session_config=None, app_key=None, session_name=None):
    if not session_config and not app_key:
        raise ValueError(f"Can't get config by name: {session_name}. Please check config name or provide app_key")

    if not app_key:
        raise AttributeError(CANNOT_FIND_APP_KEY)


def _make_desktop_session_provider_by_arguments(session_name, app_key=None, app_name=None):
    session_config = configure.get(configure.keys.desktop_session(session_name), {})
    default_session_config = configure.get(configure.keys.desktop_session("workspace"), {})

    if isinstance(session_config, dict) and len(session_config) == 0:
        raise ValueError(f"Session name: {session_name} is invalid or session_name object is empty")

    arguments = {"app-key": app_key}
    filtered_arguments = {key: value for key, value in arguments.items() if value is not None}

    merged_config = ext_config_mod.ConfigurationSet(
        ext_config_mod.config_from_dict(filtered_arguments),
        session_config,
        default_session_config,
    )

    _validate_desktop_session_app_key(
        session_config=session_config,
        app_key=merged_config.get("app-key"),
        session_name=session_name,
    )

    return make_session_provider(SessionType.DESKTOP, merged_config, session_name=session_name, app_name=app_name)


def _validate_session_arguments(app_key, session_type, grant, deployed_platform_host, deployed_platform_username):
    if app_key is None:
        raise AttributeError(CANNOT_FIND_APP_KEY)

    if (
        session_type == SessionType.PLATFORM
        and not grant.is_valid()
        and (not deployed_platform_host or not deployed_platform_username)
    ):
        raise AttributeError(
            "Please provide 'grant' attribute "
            "or set 'username' and 'password' in config. "
            "Or provide deployed parameters in config file "
            "to create deployed platform session"
        )


def _make_session_provider_by_arguments(session_name):
    from ._session_definition import _get_session_type_and_name, _retrieve_config_and_set_type

    config_path = session_name  # can't rename argument, because public API, make it right at least in function body
    session_name, session_type = _get_session_type_and_name(config_path)
    session_config = _retrieve_config_and_set_type(session_name, session_type)

    if session_type == SessionType.DESKTOP:
        default_session_config = configure.get(configure.keys.desktop_session("workspace"), {})
    else:
        default_session_config = configure.get(configure.keys.platform_session("default"), {})

    merged_config = ext_config_mod.ConfigurationSet(session_config, default_session_config)
    app_key = merged_config.get("app-key")
    deployed_platform_host = merged_config.get(DEPLOYED_PLATFORM_URL_CONFIG_KEY)
    deployed_platform_username = merged_config.get(DEPLOYED_PLATFORM_USER_CONFIG_KEY)

    grant = None
    if session_type == SessionType.PLATFORM:
        grant = create_grant(merged_config)

    _validate_session_arguments(
        app_key=app_key,
        session_type=session_type,
        grant=grant,
        deployed_platform_host=deployed_platform_host,
        deployed_platform_username=deployed_platform_username,
    )

    return make_session_provider(session_type, merged_config, grant, session_name)


def make_session_provider(session_type, config=None, grant=None, session_name="default", proxies=None, app_name=None):
    config = config or {}
    session_class = session_class_by_session_type.get(session_type)
    if not session_class:
        raise ValueError(f"Cannot find session class by session type {session_type}")
    session_class = get_session_class(session_type)

    def session_provider():
        params = _retrieve_values_from_config(config, session_type, grant)
        params["name"] = session_name
        params["proxies"] = proxies
        if app_name:
            params["app_name"] = app_name
        sessions_inst = session_class(**params)
        sessions_inst._is_debug() and sessions_inst.debug(f" + Session created: {sessions_inst}")
        return sessions_inst

    return session_provider


def get_session_class(session_type):
    session_class = session_class_by_session_type.get(session_type, None)

    if session_class is None:
        raise ValueError(f"Cannot find session class by session type {session_type}")

    return session_class
