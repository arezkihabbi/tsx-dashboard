"""
This module contains necessary functions for session config manipulation.
"""
import atexit
import json
import logging
import os
import re
import sys
from json.decoder import WHITESPACE  # noqa
from typing import Any, Optional, Union, List

from pyee import EventEmitter
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from . import _config_defaults
from ._errors import RDError
from ._external_libraries import python_configuration as ext_config_mod  # noqa
from ._tools import get_from_path

_observer: Optional[Observer] = None


def _enable_watch():
    global _observer
    _observer = Observer()
    _event_handler = _RDPConfigChangedHandler(patterns=_config_files_paths)
    _dir_names = {os.path.dirname(f) for f in _config_files_paths}
    [_observer.schedule(_event_handler, dirname) for dirname in _dir_names]
    _observer.start()

    atexit.register(_disable_watch)


def _disable_watch():
    if _observer:
        _observer.stop()
        _observer.join()


def _dispose():
    _disable_watch()
    get_config().remove_all_listeners()


def _load_config_from_file(filepath):
    _configs = _create_configs([filepath] + _config_files_paths)
    _new_config = ext_config_mod.ConfigurationSet(*_configs)
    get_config().configs = _new_config.configs


def _get_filepath(rootdir, filename):
    if rootdir and filename:
        path = os.path.join(rootdir, filename)
        return path


_SUBS_PATTERN = re.compile(r".*?\${(\w+(-\w+)*(_\w+)*(:\w+)*)}.*?")


def _process_match(value, match, root: dict):
    match = match or []
    for g in match:
        path = g[0]
        old = f"${{{path}}}"
        new = get_from_path(root, path, ":")
        new = None if isinstance(new, list) else new
        value = value.replace(old, new or old)
    return value


def _substitute_values(data: dict, root: dict = None):
    if not data:
        return data

    for k, v in data.items():
        if hasattr(v, "get"):
            _substitute_values(v, root)
        elif isinstance(v, str):
            match = _SUBS_PATTERN.findall(v)
            v = _process_match(v, match, root)
            data[k] = v
    return data


def _read_config_file(path: str) -> dict:
    try:
        with open(path, "r") as f:
            data = json.load(f, cls=_JSONDecoder)
    except FileNotFoundError:
        return {}
    except Exception as exc:  # noqa
        raise RDError(0, f"Error happened during config file {path} read") from exc

    return _substitute_values(data, data)


def _create_configs(files_paths: List[str]):
    config_from_dict = ext_config_mod.config_from_dict
    dicts = [_read_config_file(f) for f in files_paths] + [_config_defaults.config]
    configs = [config_from_dict(d) for d in dicts]
    return configs


class ConfigEvent:
    UPDATE = "update"


class _RDPConfigChangedHandler(PatternMatchingEventHandler):
    def on_any_event(self, event):
        configs = _create_configs(_config_files_paths)
        _new_config = ext_config_mod.ConfigurationSet(*configs)
        config = get_config()
        if _new_config.as_dict() != config.as_dict():
            config.configs = _new_config.configs
            try:
                config.emit(ConfigEvent.UPDATE)
            except Exception:  # noqa
                pass


class _JSONDecoder(json.JSONDecoder):
    _ENV_SUBS_PATTERN = re.compile(r".*?\${(\w+)}.*?")

    def decode(self, s, _w=WHITESPACE.match):
        match = self._ENV_SUBS_PATTERN.findall(s)
        if match:
            for g in match:
                s = s.replace(f"${{{g}}}", os.environ.get(g, g))
            s = s.replace("\\", "\\\\")
        return super().decode(s, _w)


class keys:  # noqa
    endpoints = "endpoints"
    log_level = "logs.level"
    log_filename = "logs.transports.file.name"
    log_file_enabled = "logs.transports.file.enabled"
    log_console_enabled = "logs.transports.console.enabled"
    log_file_size = "logs.transports.file.size"
    log_filter = "logs.filter"
    log_max_files = "logs.transports.file.maxFiles"
    log_interval = "logs.transports.file.interval"
    watch_enabled = "config-change-notifications-enabled"

    http_request_timeout = "http.request-timeout"
    http_auto_retry_config = "http.auto-retry"
    http_max_connections = "http.max-connections"
    http_max_keepalive_connections = "http.max-keepalive-connections"

    desktop_sessions = "sessions.desktop"

    @staticmethod
    def desktop_session(session_name) -> str:
        return "sessions.desktop.%s" % session_name

    @staticmethod
    def desktop_base_uri(session_name) -> str:
        return "sessions.desktop.%s.base-url" % session_name

    @staticmethod
    def desktop_platform_paths(session_name) -> str:
        return "sessions.desktop.%s.platform-paths" % session_name

    @staticmethod
    def desktop_handshake_url(session_name) -> str:
        return "sessions.desktop.%s.handshake-url" % session_name

    @staticmethod
    def desktop_endpoints(session_name) -> str:
        return "sessions.desktop.%s.endpoints" % session_name

    platform_sessions = "sessions.platform"
    platform_session_default_server_mode = "sessions.platform.default.server-mode"

    @staticmethod
    def platform_session(session_name) -> str:
        return "sessions.platform.%s" % session_name

    @staticmethod
    def platform_endpoints(session_name) -> str:
        return "sessions.platform.%s.endpoints" % session_name

    @staticmethod
    def platform_base_uri(session_name) -> str:
        return "sessions.platform.%s.base-url" % session_name

    @staticmethod
    def platform_auth_uri(session_name) -> str:
        return "sessions.platform.%s.auth.url" % session_name

    @staticmethod
    def platform_token_uri(session_name) -> str:
        return "sessions.platform.%s.auth.token" % session_name

    @staticmethod
    def platform_auto_reconnect(session_name) -> str:
        return "sessions.platform.%s.auto-reconnect" % session_name

    @staticmethod
    def platform_server_mode(session_name) -> str:
        return "sessions.platform.%s.server-mode" % session_name

    @staticmethod
    def platform_realtime_distribution_system(session_name) -> str:
        return "sessions.platform.%s.realtime-distribution-system" % session_name

    @staticmethod
    def stream_connects_locations(streaming_name, endpoint_name) -> str:
        return f"apis.streaming.{streaming_name}.endpoints.{endpoint_name}.locations"

    @staticmethod
    def stream_protocols(streaming_name, endpoint_name) -> str:
        return f"apis.streaming.{streaming_name}.endpoints.{endpoint_name}.protocols"

    @staticmethod
    def get_stream_direct_url(streaming_name, endpoint_name) -> str:
        return f"apis.streaming.{streaming_name}.endpoints.{endpoint_name}.direct-url"


class _RDPConfig(ext_config_mod.ConfigurationSet):
    def __init__(self, *configs):
        super().__init__(*configs)
        self._emitter = EventEmitter()
        setattr(self, "on", self._emitter.on)
        setattr(self, "remove_listener", self._emitter.remove_listener)
        setattr(self, "remove_all_listeners", self._emitter.remove_all_listeners)
        setattr(self, "emit", self._emitter.emit)
        setattr(self, "listeners", self._emitter.listeners)

    def count(self, event: str = None):
        """
        Returns count of EventEmitter listeners

        Parameters
        ----------
            event: str
                Event name.

        Returns
        -------
        Count of listeners for event or all events listeners
        """
        if event:
            return len(self._emitter.listeners(event))

        count = 0
        for event in self._emitter.event_names():
            count += len(self._emitter.listeners(event))
        return count

    def set_param(self, param: str, value: Any, auto_create: bool = False) -> None:
        """
        Set param to the config.

        Parameters
        ----------
            param: str
                Parameter name.

            value: Any
                Parameter value.

            auto_create: bool
                Default value: False. We use auto_create to create new field in config

        Raises
        ----------
        Exception
            Raise exception if param name is not type 'str' .
        """
        if not isinstance(param, str):
            raise TypeError("Invalid type of parameter name, should be string")

        if not auto_create and not self._has_param(param):
            raise ValueError(
                f"'{param}' is not defined in config. To create new parameter please use 'auto_create' property."
            )

        self[param] = value

    def _has_param(self, param: str):
        return param in self

    def get_param(self, param: str) -> Any:
        """
        Get param to the config.

        Parameters
        ----------
            param: str
                Parameter name.

        Raises
        ----------
        Exception
            Raise exception if config doesn't has param.
        """

        try:
            return self[param]
        except KeyError:
            raise AttributeError(f"Config object doesn't has '{param}' attribute")

    def _set_config_index(self, index: int, config_: ext_config_mod.Configuration) -> None:
        """
        Set config by using index.
        This method is using for overriding default config.

        Parameters
        ----------
            index: int
                Parameter name.
            config_: Configuration
                Config object
        """
        if config_ is None:
            self._configs.pop(index)

        else:
            self._configs.insert(index, config_)

    def copy(self) -> "_RDPConfig":
        configs = [config.copy() for config in self._configs]
        return _RDPConfig(*configs)


def get(key: str, default: Any = None) -> Union[dict, Any]:
    """
    Gets the particular value from config by key name.

    Parameters
    ----------
    key : str
        Config parameter name.
    default
        Value to return if there is no particular parameter in config.
    Returns
    -------
    dict or Any
        Value retrieved from config by name or default value.

    """
    return get_config().get(key, default)


def get_bool(item: str) -> bool:
    return get_config().get_bool(item)


def get_str(item: str, fmt: str = "{}") -> str:
    """
    Converts the particular value from config as a string.

    Parameters
    ----------
    item
        Config parameter value to convert to string.
    fmt
        Placeholder for Python str.format() method to convert config value to string.

    Returns
    -------
    str
        Config parameter value converted to string.

    """
    return get_config().get_str(item, fmt)


def get_int(item: str) -> int:
    """
    Converts the particular value from config as an int.

    Parameters
    ----------
    item
        Config parameter value to convert to int.

    Returns
    -------
    int
        Config parameter value converted to int.

    """
    return get_config().get_int(item)


def get_list(item: str) -> List[Any]:
    return get_config().get_list(item)


def get_param(param: str) -> Any:
    """
    Gets config parameter or raise an exception if parameter does not exist.

    Parameters
    ----------
    param : str
        Config parameter.

    Returns
    -------
    Any
        Config parameter.

    Raises
    ------
    AttributeError
        If the parameter does not exist.

    """
    return get_config().get_param(param)


def set_param(param: str, value: Any, auto_create: bool = False) -> None:
    """
    Sets key in key-value pair inside the config instance.

    Parameters
    ----------
    param : str
        Parameter name.
    value : Any
        Parameter value.
    auto_create : bool, default=False
        Flag to create new key-value pair in config.

    Raises
    ------
    TypeError
        If the parameter name is not string.
    ValueError
        If config parameter does not exist and creation automatically is disabled.

    """
    get_config().set_param(param, value, auto_create)


class _defaults:  # noqa
    http_request_timeout: Optional[str] = None
    log_level: Optional[int] = None
    platform_server_mode: Optional[bool] = None


defaults: _defaults = _defaults()

_RD_LIB_CONFIG_PATH: str = "RD_LIB_CONFIG_PATH"
_RDPLIB_ENV_DIR: str = "RDPLIB_ENV_DIR"
_default_config_file_name: str = "refinitiv-data.config.json"

_config: Optional[_RDPConfig] = None
_config_files_paths: Optional[List[str]] = None
_project_config_dir: Optional[str] = None


def _create_rdpconfig(files_paths) -> _RDPConfig:
    if isinstance(files_paths, str):
        files_paths = [files_paths]
    configs = _create_configs(files_paths)
    return _RDPConfig(*configs)


def reload():
    global _config, _config_files_paths, _observer, defaults, _project_config_dir

    _custom_filepath: str = os.environ.get(_RD_LIB_CONFIG_PATH, "")

    if _custom_filepath:
        _custom_filepath = os.path.join(_custom_filepath, _default_config_file_name)

    _project_config_dir = os.environ.get(_RDPLIB_ENV_DIR) or os.getcwd()
    _config_files_paths = [
        c
        for c in [
            # CONFIG PROVIDED BY USER
            _custom_filepath,
            # PROJECT_CONFIG_FILE
            _get_filepath(rootdir=_project_config_dir, filename=_default_config_file_name),
            # USER_CONFIG_FILE
            _get_filepath(rootdir=os.path.expanduser("~"), filename=_default_config_file_name),
        ]
        if c
    ]
    _config = _create_rdpconfig(_config_files_paths)
    _config.load = _load_config_from_file

    _observer = None
    _watch_enabled = _config.get_bool(keys.watch_enabled)
    if _watch_enabled:
        _enable_watch()

    _default_config = _config.configs[len(_config.configs) - 1]

    defaults = _defaults()
    defaults.http_request_timeout = _default_config.get(keys.http_request_timeout)
    from ._log import convert_log_level, root_logger
    import refinitiv.data as rd

    defaults.log_level = convert_log_level(_default_config.get(keys.log_level))
    defaults.platform_server_mode = _default_config.get(keys.platform_session_default_server_mode)
    log_debug(root_logger(), rd.__version__, _config_files_paths)


def log_debug(logger, version: str, path_list: list):
    if logger.level > logging.DEBUG:
        return

    logger.debug(f"RD version is {version}; Python version is {sys.version}")

    try:
        import pkg_resources as _pkg_resources

        _installed_packages = _pkg_resources.working_set
        _installed_packages = sorted([f"{i.key}=={i.version}" for i in _installed_packages])
        logger.debug(f"Installed packages ({len(_installed_packages)}): {','.join(_installed_packages)}")
    except Exception as e:
        logger.debug(f"Cannot log installed packages, {e}")

    logger.debug(f'Read configs: {", ".join(path_list)}')


RDConfig = _RDPConfig


def get_config() -> RDConfig:
    """
    Returns
    -------
    config object
    """
    if _config is None:
        reload()
    return _config


def load_config(path: Optional[str]) -> RDConfig:
    """
    Load user's config file and set this file as default.

    Parameters
    ----------
        path: str
            Path to user's config file.

    Raises
    ----------
    Exception
        If can't find file by path that user provided

    Returns
    ----------
    config object
    """
    from ._log import root_logger, is_debug

    if not os.path.exists(path):
        raise FileNotFoundError(f"Can't find file: {path}. Current working folder {os.getcwd()}")

    logger = root_logger()
    is_debug(logger) and logger.debug(f"Load config from {path}")
    loaded_config = _read_config_file(path)
    user_config = ext_config_mod.config_from_dict(loaded_config)
    config = get_config()
    config._set_config_index(0, user_config)
    return config
