import abc
import json
import time
from typing import Callable, TYPE_CHECKING, Union

import requests

from ._updater import Updater
from ..event import UpdateEvent
from ..tools import NullResponse, UNAUTHORIZED_CODES
from ...log_reporter import LogReporter
from ....delivery._data._endpoint_data import RequestMethod
from ....delivery._data._request import Request

if TYPE_CHECKING:
    from . import GrantType
    from ._ping_token_info import PingTokenInfo
    from ._sts_token_info import STSTokenInfo
    from .._platform_session import PlatformSession

codes = requests.codes


class RefreshTokenUpdater(Updater, LogReporter, abc.ABC):
    def __init__(
        self,
        session: "PlatformSession",
        token_info: Union["STSTokenInfo", "PingTokenInfo"],
        delay: float,
        callback: Callable[[str, str, dict], None],
    ) -> None:
        Updater.__init__(self, delay, "RefreshTokenUpdater")
        LogReporter.__init__(self, logger=session.logger())

        self._session = session
        self._token_info = token_info
        self._callback = callback
        self._grant: "GrantType" = self._session._grant
        self._app_key = self._session._app_key
        self._url = self._session.authentication_token_endpoint_url

    @Updater.delay.setter
    def delay(self, value: int):
        if value <= 0:
            raise ValueError("Delay must be greater than 0")
        Updater.delay.fset(self, value)

    def _do_update(self):
        cur_time = time.time()

        if self._token_info.expires_at <= cur_time:
            event = UpdateEvent.REFRESH_TOKEN_EXPIRED
            message = "Time expired for the refresh token update"
            self.is_debug() and self.debug(message)
            self._callback(event, message, {})
            return

        response = self._request_token()

        try:
            json_content = response.json()
        except json.decoder.JSONDecodeError:
            message = f"Malformed JSON received during token refresh: '{response.text}'"
            self.error(message)
            json_content = {}

        status_code = response.status_code

        if status_code == codes.ok:
            event = UpdateEvent.REFRESH_TOKEN_SUCCESS
            message = "All is well"
        else:
            if status_code in UNAUTHORIZED_CODES:
                event = UpdateEvent.REFRESH_TOKEN_BAD
                error_description = json_content.get("error_description", "empty error description")
            else:
                event = UpdateEvent.REFRESH_TOKEN_FAILED
                error_description = json_content.get(
                    "error_description",
                    getattr(response, "text", "empty error description"),
                )
            message = error_description
            self.error(f"[Error {status_code}] - {json_content}")

        self._callback(event, message, json_content)

    def _request_token(self):
        data = self._get_request_data()
        is_debug = self.is_debug()
        is_debug and self.debug(f"Request refresh token to {self._url}\n\twith post data = {str(data)}")
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._token_info.access_token}",
        }
        try:
            request = Request(
                url=self._url,
                method=RequestMethod.POST,
                headers=headers,
                data=data,
                auto_retry=True,
            )
            response = self._session.http_request(request)
            is_debug and self.debug(f"Refresh token response: {response.text}")
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
