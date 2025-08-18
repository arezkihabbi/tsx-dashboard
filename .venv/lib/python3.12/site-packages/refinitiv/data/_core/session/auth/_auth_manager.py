import abc
import threading
from typing import TYPE_CHECKING, Callable, Set, List

from ._access_token_updater import AccessTokenUpdater
from ._refresh_token_updater import RefreshTokenUpdater
from ._token_info import TokenInfo
from ..event import UpdateEvent
from ...log_reporter import LogReporter
from ...._errors import ScopeError, RDError
from ...._tools import get_delays, CallbackHandler, cached_property

if TYPE_CHECKING:
    from .._platform_session import PlatformSession

delays = get_delays()


class AuthManager(LogReporter, abc.ABC):
    """
    Methods
    -------
    is_closed()
        The method returns True if closed, otherwise False
    is_authorized()
        The method returns True if authorized, otherwise False.
        If instance destroyed or closed always returns False
    authorize()
        The method starts process authorization
    close()
        The method stops refresh token updater and access token updater
    dispose()
        The method destroy an instance
    """

    token_info_class = TokenInfo
    access_token_updater_class = AccessTokenUpdater
    refresh_token_updater_class = RefreshTokenUpdater

    def __init__(self, session: "PlatformSession", auto_reconnect: bool) -> None:
        LogReporter.__init__(self, logger=session.logger())

        self._session = session
        self._auto_reconnect = auto_reconnect

        self._ee = CallbackHandler()
        self._token_info = self.token_info_class()

        self._closed: bool = False
        self._authorized: bool = False
        self._disposed: bool = False

        self._scope_map = {}

        self._result_evt: threading.Event = threading.Event()
        self._start_evt: threading.Event = threading.Event()
        self._thread: threading.Thread = threading.Thread(
            target=self._do_authorize,
            name="AuthManager-Thread",
            daemon=True,
        )

    @cached_property
    def _access_token_updater(self) -> AccessTokenUpdater:
        return self.access_token_updater_class(
            self._session,
            0.00001,
            self._access_token_update_handler,
        )

    @cached_property
    def _refresh_token_updater(self) -> RefreshTokenUpdater:
        return self.refresh_token_updater_class(
            self._session,
            self._token_info,
            0.00001,
            self._refresh_token_update_handler,
        )

    def on(self, event: str, listener: Callable):
        self._ee.on(event, listener)

    def is_closed(self) -> bool:
        """
        Returns
        -------
        bool
            True if closed, otherwise False
        """
        return self._closed is True

    def is_authorized(self) -> bool:
        """
        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self.is_closed():
            return False

        return self._authorized is True

    def authorize(self) -> bool:
        """
        The method starts process authorization

        Returns
        -------
        bool
            True if authorized, otherwise False
        """
        if self._disposed:
            raise RuntimeError("AuthManager disposed")

        if self.is_authorized():
            return True

        is_debug = self.is_debug()
        is_debug and self.debug("AuthManager: start authorize")

        self._closed = False
        self._authorized = False

        self._result_evt.clear()
        self._start_evt.set()

        if not self._thread.ident:
            self._thread.start()

        if not self.is_closed() and not self._disposed:
            self._result_evt.wait()

        is_authorized = self.is_authorized()
        is_debug and self.debug(f"AuthManager: end authorize, result {is_authorized}")
        return is_authorized

    def _do_authorize(self):
        while not self._disposed and not self.is_closed():
            self._start_evt.wait()

            if self._disposed:
                break

            is_debug = self.is_debug()
            is_debug and self.debug(
                f"AuthManager: Access token will be requested in {self._access_token_updater.delay} seconds"
            )
            try:
                self._access_token_updater.start()
            except RDError as e:
                self.close()
                raise e

            if self.is_authorized():
                latency_secs = self._access_token_updater.latency_secs
                delay = self._token_info.calc_token_update_time(latency_secs)
                self._refresh_token_updater.delay = delay
                is_debug and self.debug(
                    f"AuthManager: Refresh token will be requested in {self._refresh_token_updater.delay} seconds"
                )
                self._refresh_token_updater.start()

    def close(self):
        """
        The method stops refresh token updater and access token updater
        """
        if self._disposed:
            raise RuntimeError("AuthManager disposed")

        if self.is_closed():
            return

        self.is_debug() and self.debug("AuthManager: close")
        self._result_evt.set()
        self._start_evt.clear()
        self._access_token_updater.stop()
        self._refresh_token_updater.stop()
        self._closed = True
        self._authorized = False
        self._ee.emit(UpdateEvent.CLOSE_AUTH_MANAGER, self)

    def _access_token_update_handler(self, event: str, message: str, json_content: dict) -> None:
        is_debug = self.is_debug()
        is_debug and self.debug(f"AuthManager: Access token handler, event: {event}, message: {message}")

        if event is UpdateEvent.ACCESS_TOKEN_SUCCESS:
            self._authorized = True
            delays.reset()
            new_token_info = self._token_info.from_dict(json_content)
            self._token_info.update(new_token_info)
            access_token = self._token_info.access_token
            is_debug and self.debug(f"Access token {access_token}. Expire in {self._token_info.expires_in} seconds")
            self._ee.emit(UpdateEvent.UPDATE_ACCESS_TOKEN, access_token)
            self._access_token_updater.stop()
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_SUCCESS, message)
            self._result_evt.set()

        elif event is UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED:
            self._authorized = False
            self._access_token_updater.stop()
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self.close()
            self._result_evt.set()

        elif event is UpdateEvent.ACCESS_TOKEN_FAILED:
            if not self._auto_reconnect:
                self._authorized = False
                self._access_token_updater.stop()
                self._result_evt.set()

            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)

            if self._auto_reconnect:
                delay = delays.next()
                is_debug and self.debug(f"AuthManager: reconnecting in {delay} secs")
                self._access_token_updater.delay = delay
                self._ee.emit(UpdateEvent.RECONNECTING, message)

            else:
                self.close()

    def _refresh_token_update_handler(self, event: str, message: str, json_content: dict) -> None:
        is_debug = self.is_debug()
        is_debug and self.debug(f"AuthManager: Refresh token handler, event: {event}, message: {message}")

        if event is UpdateEvent.REFRESH_TOKEN_SUCCESS:
            new_token_info = self._token_info.from_dict(json_content)
            self._token_info.update(new_token_info)
            access_token = new_token_info.access_token
            is_debug and self.debug(
                f"Received access token {access_token}. Expire in {new_token_info.expires_in} seconds"
            )
            self._ee.emit(UpdateEvent.UPDATE_ACCESS_TOKEN, access_token)
            latency_secs = self._access_token_updater.latency_secs
            delay = new_token_info.calc_token_update_time(latency_secs)
            self._refresh_token_updater.delay = delay
            is_debug and self.debug(f"Set refresh token delay to {delay} seconds")
            self._ee.emit(event, message)

        elif event is UpdateEvent.REFRESH_TOKEN_BAD:
            self._authorized = False
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self.close()

        elif event is UpdateEvent.REFRESH_TOKEN_FAILED:
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)

            if self._auto_reconnect:
                delay = delays.next()
                is_debug and self.debug(f"AuthManager: Trying to get Refresh token again in {delay} secs")
                self._refresh_token_updater.delay = delay
                self._ee.emit(UpdateEvent.RECONNECTING, message)

            else:
                self._authorized = False
                self.close()

        elif event is UpdateEvent.REFRESH_TOKEN_EXPIRED:
            self._ee.emit(event, message)
            self._ee.emit(UpdateEvent.AUTHENTICATION_FAILED, message)
            self._authorized = False

            if self._auto_reconnect:
                is_debug and self.debug("AuthManager: reconnecting")
                self._ee.emit(UpdateEvent.RECONNECTING, message)
                self._refresh_token_updater.stop()

            else:
                self.close()

    def dispose(self):
        """
        The method destroy an instance

        Returns
        -------
        None
        """
        if self._disposed:
            return

        if not self.is_closed():
            self.close()

        self._disposed = True
        self._access_token_updater.dispose()
        self._refresh_token_updater.dispose()
        self._start_evt.set()
        self._ee.remove_all_callbacks()
        self._ee = None
        self._token_info = None
        self._start_evt = None
        self._thread = None
        self._session = None

    def set_scope(self, key: str, method: str, required_scopes: List[Set[str]]):
        self._scope_map[key.rstrip("/"), method.lower()] = required_scopes

    def verify_scope(self, key: str, method: str):
        required_scope_sets = self._scope_map.get((key.rstrip("/"), method.lower()))

        if required_scope_sets is None:
            self.is_debug() and self.debug(f"Scope for key={key}, method={method} not found.")

        if required_scope_sets and all(
            not required_scope.issubset(self._token_info.scope) for required_scope in required_scope_sets
        ):
            self.warning(f"No user scope for key={key}, method={method}.")
            raise ScopeError(required_scope_sets, self._token_info.scope, key, method)
