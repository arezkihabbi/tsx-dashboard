import abc
import asyncio
import itertools
import logging
import warnings
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from threading import Lock
from typing import Callable, TYPE_CHECKING, Union

from . import http_service
from ._dacs_params import DacsParams
from ._listeners import CxnListeners
from ._session_cxn_type import SessionCxnType
from ._user_uuid import get_user_uuid
from .event_code import EventCode
from .proxy_info import ProxiesInfo
from .tools import is_closed
from ... import _configure as configure, _log as log
from ..._open_state import OpenState
from ..._tools import DEBUG, cached_property, create_repr

if TYPE_CHECKING:
    import httpx
    from ._session_cxn_factory import SessionConnection
    from .http_service import HTTPService
    from ..._configure import _RDPConfig
    from ...delivery._data._data_provider import Request
    from ...delivery._stream.metadata import Dictionary

SESSION_IS_CLOSED = "Session is closed"
DEFAULT_APP_NAME = "RD-PYTHON-LIB"


class Session(AbstractContextManager, AbstractAsyncContextManager):
    _id_iterator = itertools.count()
    # Logger for messages outside of particular session instances

    __acquire_session_id_lock = Lock()
    __acquire_stream_id_lock = Lock()
    __acquire_metadata_load_lock = Lock()

    @property
    @abc.abstractmethod
    def type(self):
        pass

    @staticmethod
    def class_logger():
        return log.create_logger("session")

    @property
    def name(self):
        return self._name

    def __init__(
        self,
        app_key,
        on_state: Callable[[OpenState, str, "Session"], None] = None,
        on_event: Callable[[EventCode, Union[dict, str], "Session"], None] = None,
        token=None,
        deployed_platform_username=None,
        dacs_position=None,
        dacs_application_id=None,
        name="default",
        proxies: Union[str, dict] = None,
        app_name: str = None,
    ):
        with self.__acquire_session_id_lock:
            self._session_id = next(self._id_iterator)

        session_type = self.type.name.lower()
        logger_name = f"sessions.{session_type}.{name}.{self.session_id}"

        logger = self.class_logger()
        log.is_debug(logger) and logger.debug(
            f'Creating session "{logger_name}" based on session.{session_type}.Definition("{session_type}.{name}")'
        )

        if app_key is None:
            raise ValueError("app_key value can't be None")

        self._state = OpenState.Closed

        self._app_key = app_key
        self._on_state: Callable[[OpenState, str, Session], None] = on_state
        self._on_event: Callable[[EventCode, Union[dict, str], Session], None] = on_event
        self._access_token = token
        self._dacs_params = DacsParams()
        self._app_name = f"{app_name}_{DEFAULT_APP_NAME}" if app_name else DEFAULT_APP_NAME

        if deployed_platform_username:
            self._dacs_params.deployed_platform_username = deployed_platform_username
        if dacs_position:
            self._dacs_params.dacs_position = dacs_position
        if dacs_application_id:
            self._dacs_params.dacs_application_id = dacs_application_id

        self._logger = log.create_logger(logger_name)
        # redirect log method of this object to the log in logger object
        self.log = self._logger.log
        self.warning = self._logger.warning
        self.error = self._logger.error
        self.debug = self._logger.debug
        self.info = self._logger.info

        self._name = name
        self._config: "_RDPConfig" = configure.get_config().copy()

        # override session api config with session's specific api parameters
        specific_api_path = f"sessions.{session_type}.{name}.apis"
        specific_api = self._config.get(specific_api_path)
        if specific_api:
            self._config.set_param("apis", specific_api)

        self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
        # rssl/rwf stream ids always starts with 5
        self._omm_stream_counter = itertools.count(5)
        self._rdp_stream_counter = itertools.count(5)  # can not be 0

        self._is_metadata_loaded = False
        self._proxies = ProxiesInfo(proxies)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    async def __aenter__(self):
        await self.open_async()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.close_async()

    def _get_omm_stream_id(self) -> int:
        with self.__acquire_stream_id_lock:
            return next(self._omm_stream_counter)

    def _get_rdp_stream_id(self) -> int:
        with self.__acquire_stream_id_lock:
            return next(self._rdp_stream_counter)

    @cached_property
    def _http_service(self) -> "HTTPService":
        return http_service.get_service(self)

    @cached_property
    def _connection(self) -> "SessionConnection":
        from ._session_cxn_factory import get_session_cxn

        cxn_type = self._get_session_cxn_type()
        cxn = get_session_cxn(cxn_type, self)
        self._is_debug() and self.debug(f"Created session connection {cxn_type}")
        return cxn

    @cached_property
    def _listeners(self) -> CxnListeners:
        return CxnListeners(self)

    @abc.abstractmethod
    def _get_session_cxn_type(self) -> SessionCxnType:
        pass

    def on_state(self, callback: Callable[[OpenState, str, "Session"], None]) -> None:
        """
        Registers a defined callback function.
        Called by the library whenever the state of the session is updated.

        Parameters
        ----------
        callback: Callable[[OpenState, str, Session], None]
            Callback function or method to be notified of any state change.

        Raises
        ----------
        TypeError
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_state = callback

    def _call_on_state(self, message: str):
        if not self._on_state:
            return
        self._is_debug() and self.debug(f"Session calls on_state({self}, {self._state}, {message})")
        try:
            self._on_state(self._state, message, self)
        except Exception as e:
            self.error(f"on_state user function on session {self.session_id} raised error {e}")

    def on_event(self, callback: Callable[[EventCode, Union[dict, str], "Session"], None]) -> None:
        """
        Registers a defined callback function.
        Called by the library whenever the event of the session is updated.

        Parameters
        ----------
        callback: Callable[[EventCode, Union[dict, str], "Session"], None]
            Callback function or method to be notified of any event change.

        Raises
        ----------
        TypeError
            If user provided invalid object type
        """
        if not callable(callback):
            raise TypeError("Please provide callable object")

        self._on_event = callback

    def _call_on_event(self, event: EventCode, message: Union[dict, str]):
        if not self._on_event:
            return
        self._is_debug() and self.debug(f"Session calls on_event({self}, {event}, {message})")
        try:
            self._on_event(event, message, self)
        except Exception as e:
            self.error(f"on_event user function on session {self.session_id} raised error {e}")

    def __repr__(self):
        return create_repr(
            self,
            middle_path="session",
            content=f"{{name='{self.name}'}}",
        )

    def _on_config_updated(self):
        log_level = log.read_log_level_config()
        if log_level != self.get_log_level():
            self.set_log_level(log_level)

    @property
    def config(self) -> "_RDPConfig":
        return self._config

    @property
    def open_state(self):
        """
        Returns the session state.
        """
        return self._state

    @property
    def app_key(self):
        """
        Returns the application id.
        """
        return self._app_key

    @app_key.setter
    def app_key(self, app_key):
        """
        Set the application key.
        """
        if app_key is None:
            return
        if not isinstance(app_key, str):
            raise AttributeError("application key must be a string")

        self._app_key = app_key

    def update_access_token(self, access_token):
        self._is_debug() and self.debug(f"Session.update_access_token(access_token='{access_token}'")
        self._access_token = access_token

        from ...delivery._stream import stream_cxn_cache

        if stream_cxn_cache.has_cxns(self):
            cxns_by_session = stream_cxn_cache.get_cxns(self)
            for cxn in cxns_by_session:
                cxn.send_login_message()

    @property
    def session_id(self):
        return self._session_id

    def logger(self) -> logging.Logger:
        return self._logger

    def _get_rdp_url_root(self) -> str:
        return ""

    @cached_property
    def _user_uuid(self):
        return get_user_uuid(self)

    @cached_property
    def http_request_timeout_secs(self):
        return self._http_service.request_timeout_secs

    ############################################################
    #   shared metadata

    @cached_property
    def _metadata(self) -> "Dictionary":
        from ...delivery._dictionary import Dictionary

        return Dictionary(self)

    def _load_metadata(self, api: str) -> None:
        with self.__acquire_metadata_load_lock:
            if not self._is_metadata_loaded:
                self._metadata.load(api=api)
                self._is_metadata_loaded = True

    def _validate_metadata(self, fields: dict) -> dict:
        if not self._is_metadata_loaded:
            raise ValueError("Metadata is not loaded")

        return self._metadata.validate(fields)

    ############################################################
    #   reconnection configuration

    @property
    def stream_auto_reconnection(self):
        return True

    @property
    def server_mode(self):
        return False

    @abc.abstractmethod
    def get_omm_login_message(self):
        """return the login message for OMM 'key' section"""
        pass

    @abc.abstractmethod
    def get_rdp_login_message(self, stream_id):
        """return the login message for RDP protocol"""
        pass

    ######################################
    # methods to manage log              #
    ######################################
    def set_log_level(self, log_level: [int, str]) -> None:
        """
        Sets the level of log messages.
        By default, logs are disabled.

        Parameters
        ----------
        log_level : int | str
            Log level value. Possible values are :
            [CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET]
        """
        log_level = log.convert_log_level(log_level)
        self._logger.setLevel(log_level)

        if DEBUG:
            # Enable debugging

            # Report all mistakes managing asynchronous resources.
            warnings.simplefilter("always", ResourceWarning)

    def get_log_level(self):
        """
        Gets the current log level.

        Returns
        -------
        level
        """
        return self._logger.level

    def trace(self, message):
        self._logger.log(log.TRACE, message)

    def _is_debug(self):
        return self._logger.level == logging.DEBUG

    ######################################
    # methods to open and close session  #
    ######################################
    def open(self) -> OpenState:
        """
        Opens the session.

        Returns
        -------
        OpenState
        """
        if is_closed(self):
            is_debug = self._is_debug()
            is_debug and self.debug("Open session")

            self._state = OpenState.Pending
            self._call_on_state("Session opening in progress")
            self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
            self._http_service.open()
            is_opened = self._connection.open()

            if is_opened:
                self._state = OpenState.Opened
                self._call_on_state("Session is opened")
                is_debug and self.debug("Opened session")
            else:
                self.close()
                self._state = OpenState.Closed
                self._call_on_state(SESSION_IS_CLOSED)

        return self._state

    async def open_async(self) -> OpenState:
        """
        Opens the session asynchronously.

        Returns
        -------
        OpenState
        """
        if is_closed(self):
            is_debug = self._is_debug()
            is_debug and self.debug("Open async session")

            self._state = OpenState.Pending
            self._call_on_state("Session opening in progress")
            self._config.on(configure.ConfigEvent.UPDATE, self._on_config_updated)
            await self._http_service.open_async()
            is_opened = self._connection.open()

            if is_opened:
                self._state = OpenState.Opened
                self._call_on_state("Session is opened")
            else:
                await self.close_async()
                self._state = OpenState.Closed
                self._call_on_state(SESSION_IS_CLOSED)

            is_debug and self.debug("Opened async session")

        return self._state

    def close(self) -> OpenState:
        """
        Closes the session.

        Returns
        -------
        OpenState
        """
        if not is_closed(self):
            is_debug = self._is_debug()
            is_debug and self.debug(f"Closing session '{self.name}'")

            self._state = OpenState.Closed

            from ...delivery._stream import stream_cxn_cache

            stream_cxn_cache.close_cxns(self)
            self._http_service.close()
            self._connection.close()

            if DEBUG:
                import time
                from ...delivery._stream import stream_cxn_cache
                import threading

                time.sleep(5)
                s = "\n\t".join([str(t) for t in threading.enumerate()])
                is_debug and self.debug(f"Threads:\n\t{s}")

                if stream_cxn_cache.has_cxns(self):
                    raise AssertionError(
                        f"Not all cxns are closed (session={self},\ncxns={stream_cxn_cache.get_cxns(self)})"
                    )

            self._config.remove_listener(configure.ConfigEvent.UPDATE, self._on_config_updated)
            self._call_on_state(SESSION_IS_CLOSED)
            is_debug and self.debug(f"Closed session '{self.name}'")

        return self._state

    async def close_async(self) -> OpenState:
        """
        Closes the session asynchronously.

        Returns
        -------
        OpenState
        """
        if not is_closed(self):
            is_debug = self._is_debug()
            is_debug and self.debug("Close async session")

            self._state = OpenState.Closed

            from ...delivery._stream import stream_cxn_cache

            stream_cxn_cache.close_cxns(self)
            await self._http_service.close_async()
            self._connection.close()

            if DEBUG:
                from ...delivery._stream import stream_cxn_cache
                import threading

                await asyncio.sleep(5)
                s = "\n\t".join([str(t) for t in threading.enumerate()])
                is_debug and self.debug(f"Threads:\n\t{s}")

                if stream_cxn_cache.has_cxns(self):
                    raise AssertionError(
                        f"Not all cxns are closed (session={self},\ncxns={stream_cxn_cache.get_cxns(self)})"
                    )

            self._config.remove_listener(configure.ConfigEvent.UPDATE, self._on_config_updated)
            self._call_on_state(SESSION_IS_CLOSED)
            is_debug and self.debug("Closed async session")

        return self._state

    async def http_request_async(self, request: "Request") -> "httpx.Response":
        return await self._http_service.request_async(request)

    def http_request(self, request: "Request") -> "httpx.Response":
        return self._http_service.request(request)

    def verify_scope(self, key: str, method: str):
        # for override
        pass

    def _handle_insufficient_scope(self, path: str, method: str, message: str) -> None:
        # for override
        pass

    @abc.abstractmethod
    def __eq__(self, other):
        pass

    def __hash__(self):
        return super().__hash__()
