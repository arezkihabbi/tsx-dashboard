import socket
from typing import Iterable, Optional, TYPE_CHECKING

import httpx
from appdirs import user_config_dir, user_data_dir

from .auth import create_auth_manager, AuthManager
from .event_code import EventCode
from ... import __version__
from ..._tools import cached_property, urljoin
from ...delivery._data._endpoint_data import RequestMethod
from ...delivery._data._request import Request
from ...errors import DesktopSessionError, PlatformSessionError

if TYPE_CHECKING:
    from ._desktop_session import DesktopSession
    from ._platform_session import PlatformSession


def update_port_in_url(url, port):
    try:
        protocol, path, default_port = url.split(":")
    except ValueError:
        protocol, path, *_ = url.split(":")

    if port is not None:
        retval = ":".join([protocol, path, str(port)])
    else:
        retval = url

    return retval


def read_firstline_in_file(filename, logger=None):
    try:
        f = open(filename)
        first_line = f.readline()
        f.close()
        return first_line
    except IOError as e:
        if logger:
            logger.error(f"I/O error({e.errno}): {e.strerror}")
        return ""


# --------------------------------------------------------------------------------------
#   Desktop
# --------------------------------------------------------------------------------------


class DesktopConnection:
    def __init__(self, session: "DesktopSession"):
        self._session = session
        self._base_url = self._session._base_url
        self._uuid = self._session._uuid
        self.app_key = self._session.app_key
        self._dp_proxy_base_url = self._session._dp_proxy_base_url

    def get_timeout(self):
        return self._session.get_timeout()

    def get_handshake_url(self):
        return self._session._get_handshake_url()

    def set_port_number(self, port_number):
        return self._session.set_port_number(port_number)

    def error(self, msg, *args, **kwargs):
        return self._session.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        return self._session.debug(msg, *args, **kwargs)

    def is_debug(self) -> bool:
        return self._session._is_debug()

    def open(self) -> bool:
        is_opened = True
        port_number = None
        try:
            if not self._dp_proxy_base_url:
                # Identify port number to update base url
                port_number = self.identify_scripting_proxy_port()
                self.set_port_number(port_number)

            handshake_url = self.get_handshake_url()

            self.handshake(handshake_url)

        except DesktopSessionError as e:
            self.error(e.message)
            is_opened = False

        if not self._dp_proxy_base_url and not port_number:
            is_opened = False
            self._session._call_on_event(EventCode.SessionAuthenticationFailed, "Eikon is not running")

        return is_opened

    def close(self):
        # nothing to close
        pass

    def identify_scripting_proxy_port(self):
        """
        Returns the port used by the Scripting Proxy stored in a configuration file.
        """
        import platform
        import os

        port = None
        path = []
        func = user_config_dir if platform.system() == "Linux" else user_data_dir
        app_names = ["Data API Proxy", "Eikon API proxy", "Eikon Scripting Proxy"]
        for app_author in ["Refinitiv", "Thomson Reuters"]:
            path = path + [
                func(app_name, app_author, roaming=True)
                for app_name in app_names
                if os.path.isdir(func(app_name, app_author, roaming=True))
            ]

        is_debug = self.is_debug()
        if len(path):
            port_in_use_file = os.path.join(path[0], ".portInUse")

            # Test if ".portInUse" file exists
            if os.path.exists(port_in_use_file):
                # First test to read .portInUse file
                first_line = read_firstline_in_file(port_in_use_file)
                if first_line != "":
                    saved_port = first_line.strip()
                    test_proxy_url = update_port_in_url(self._base_url, saved_port)
                    test_proxy_result = self.check_proxy(test_proxy_url)
                    if test_proxy_result:
                        port = saved_port
                        is_debug and self.debug(f"Port {port} was retrieved from .portInUse file")
                    else:
                        is_debug and self.debug(f"Retrieved port {saved_port} value from .portIntUse isn't valid.")

        if port is None:
            is_debug and self.debug("Warning: file .portInUse was not found. Try to fallback to default port number.")
            port = self.get_port_number_from_range(("9000", "9060"), self._base_url)

        if port is None:
            self.error("Error: no proxy address identified.\nCheck if Desktop is running.")
            return None

        return port

    def get_port_number_from_range(self, ports: Iterable[str], url: str) -> Optional[str]:
        is_debug = self.is_debug()
        for port_number in ports:
            is_debug and self.debug(f"Try defaulting to port {port_number}...")
            test_proxy_url = update_port_in_url(url, port_number)
            test_proxy_result = self.check_proxy(test_proxy_url)
            if test_proxy_result:
                is_debug and self.debug(f"Default proxy port {port_number} was successfully checked")
                return port_number
            is_debug and self.debug(f"Default proxy port #{port_number} failed")

        return None

    def check_proxy(self, url: str, timeout=None) -> bool:
        #   set default timeout
        timeout = timeout if timeout is not None else self.get_timeout()
        url = urljoin(url, "/api/status")

        is_debug = self.is_debug()
        try:
            request = Request(url=url, method=RequestMethod.GET, timeout=timeout)
            response = self._session.http_request(request)
            is_debug and self.debug(f"Checking proxy url {url} response : {response.status_code} - {response.text}")
            return True
        except (socket.timeout, httpx.ConnectTimeout):
            is_debug and self.debug(f"Timeout on checking proxy url {url}")
        except ConnectionError as e:
            is_debug and self.debug(f"Connexion Error on checking proxy {url} : {e!r}")
        except Exception as e:
            is_debug and self.debug(f"Error on checking proxy url {url} : {e!r}")
        return False

    def handshake(self, url, timeout=None):
        timeout = timeout if timeout is not None else self.get_timeout()

        is_debug = self.is_debug()
        is_debug and self.debug(f"Try to handshake on url {url}...")

        try:
            # DAPI for E4 - API Proxy - Handshake
            json = {
                "AppKey": self.app_key,
                "AppScope": "trapi",
                "ApiVersion": "1",
                "LibraryName": "RDP Python Library",
                "LibraryVersion": __version__,
            }

            if self._uuid:
                # add uuid for DP-PROXY multi user mode
                json.update({"Uuid": self._uuid})

            response = self._session.http_request(
                Request(
                    url=url,
                    method=RequestMethod.POST,
                    headers={"Content-Type": "application/json"},
                    json=json,
                    timeout=timeout,
                )
            )

            status_code = response.status_code

            if status_code == httpx.codes.OK:
                self._session._access_token = response.json().get("access_token", None)

            else:
                text = response.text

                if status_code == httpx.codes.BAD_REQUEST:
                    self.error(f"Status code {status_code}: Bad request on handshake url {url} : {text}")
                    message = f"Status code {status_code}: App key is incorrect"

                else:
                    message = f"Response {status_code} on handshake url {url} : {text}"
                    self.error(message)

                self._session._call_on_event(EventCode.SessionAuthenticationFailed, message)
                raise DesktopSessionError(1, message)

        except (socket.timeout, httpx.ConnectTimeout):
            raise DesktopSessionError(1, f"Timeout on handshake url {url}")

        except Exception as e:
            raise DesktopSessionError(1, f"Error on handshake url {url} : {e!r}")


# --------------------------------------------------------------------------------------
#   RefinitivData
# --------------------------------------------------------------------------------------


class RefinitivDataConnection:
    def __init__(self, session: "PlatformSession"):
        self._session = session

    @cached_property
    def auth_manager(self) -> AuthManager:
        return create_auth_manager(
            self._session,
            self._session.server_mode,
        )

    async def http_request_async(self, request: "Request") -> httpx.Response:
        return await self._session._http_service.request_async(request)

    def http_request(self, request: "Request") -> httpx.Response:
        return self._session._http_service.request(request)

    def open(self) -> bool:
        is_opened = self.auth_manager.authorize()
        return is_opened

    def close(self):
        self.auth_manager.close()


class RefinitivDataAndDeployedConnection(RefinitivDataConnection):
    def __init__(self, session):
        RefinitivDataConnection.__init__(self, session)


class DeployedConnection(RefinitivDataAndDeployedConnection):
    def __init__(self, session):
        RefinitivDataAndDeployedConnection.__init__(self, session)

    async def http_request_async(self, *args, **kwargs):
        raise PlatformSessionError(
            -1,
            "Error!!! Platform session cannot connect to refinitiv dataplatform. "
            "Please check or provide the access right.",
        )

    def http_request(self, *args, **kwargs):
        raise PlatformSessionError(
            -1,
            "Error!!! Platform session cannot connect to refinitiv dataplatform. "
            "Please check or provide the access right.",
        )

    def open(self) -> bool:
        return True

    def close(self):
        # nothing to close
        pass
