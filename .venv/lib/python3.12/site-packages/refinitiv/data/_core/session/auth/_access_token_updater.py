import abc
import time
from typing import TYPE_CHECKING, Callable

import requests
from json.decoder import JSONDecodeError

from ._updater import Updater
from ..event import UpdateEvent
from ..tools import NullResponse, UNAUTHORIZED_CODES
from ...log_reporter import LogReporter
from ....delivery._data._endpoint_data import RequestMethod
from ....delivery._data._request import Request

if TYPE_CHECKING:
    from . import GrantType
    from .._platform_session import PlatformSession

codes = requests.codes


class AccessTokenUpdater(Updater, LogReporter, abc.ABC):
    def __init__(self, session: "PlatformSession", delay: int, callback: Callable[[str, str, dict], None]):
        Updater.__init__(self, delay, "AccessTokenUpdater")
        LogReporter.__init__(self, logger=session.logger())

        self._session = session
        self._callback = callback

        self._grant: "GrantType" = self._session._grant
        self._app_key: str = self._session._app_key
        self._url: str = self._session.authentication_token_endpoint_url
        self._signon_control: bool = self._session.signon_control

        self.latency_secs: float = 0.0

    @Updater.delay.setter
    def delay(self, value: int):
        if value <= 0:
            raise ValueError("Delay must be greater than 0")
        Updater.delay.fset(self, value)

    def _do_update(self):
        response = self._request_token()
        status_code = response.status_code
        try:
            json_content = response.json()
        except JSONDecodeError:
            message = f"Malformed JSON received during token refresh: '{response.text}'"
            self.error(message)
            json_content = {}

        if status_code == codes.ok:
            event = UpdateEvent.ACCESS_TOKEN_SUCCESS
            message = "All is well"

        else:
            if status_code in UNAUTHORIZED_CODES:
                event = UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED
                error_description = json_content.get("error_description", "empty error description")
            else:
                event = UpdateEvent.ACCESS_TOKEN_FAILED
                error_description = json_content.get(
                    "error_description",
                    getattr(response, "text", "empty error description"),
                )
            message = error_description
            self.error(f"[Error {status_code}] - {json_content}")

        self._callback(event, message, json_content)

    def _request_token(self):
        try:
            start = time.time()
            request = Request(
                url=self._url,
                method=RequestMethod.POST,
                headers={"Accept": "application/json"},
                data=self._get_request_data(),
            )
            response = self._session.http_request(request)
            end = time.time()
            self.latency_secs = end - start
            self.is_debug() and self.debug(f"Latency: {self.latency_secs} sec.\nAccess token response: {response.text}")
        except Exception as e:
            response = NullResponse()
            response.text = str(e)

        return response

    @abc.abstractmethod
    def _get_request_data(self) -> dict:
        pass

    def _do_dispose(self):
        self._session = None
        self._callback = None
