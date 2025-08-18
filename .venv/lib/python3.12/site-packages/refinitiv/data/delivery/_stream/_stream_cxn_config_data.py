import abc
import os
from dataclasses import dataclass
from itertools import compress
from typing import List, TYPE_CHECKING, Union

from ..._core.session.tools import is_desktop_session

if TYPE_CHECKING:
    from ..._core.session import Session


@dataclass
class StreamServiceInfo:
    scheme: str
    host: str
    port: int
    path: str
    data_formats: List[str]
    location: str
    transport: str


class StreamCxnConfig(abc.ABC):
    def __init__(
        self,
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
        transport: str = "websocket",
        api_cfg_key: str = "",
    ):
        if isinstance(infos, list) and len(infos) == 0:
            raise ValueError("infos are empty")

        if not isinstance(infos, list):
            infos = [infos]

        if not isinstance(protocols, list):
            protocols = [protocols]

        self._num_infos = len(infos)
        self._infos = infos
        self._protocols = protocols
        self._transport = transport
        self._available = [True] * len(infos)
        self._index = 0
        self._api_cfg_key = api_cfg_key

    @property
    def transport(self):
        return self._transport

    @property
    def info(self):
        return self._infos[self._index]

    @property
    def num_infos(self) -> int:
        return self._num_infos

    def info_not_available(self) -> None:
        self._available[self._index] = False

    def has_available_info(self) -> bool:
        return any(self._available)

    def next_available_info(self) -> int:
        if not self.has_available_info():
            raise ValueError("No available infos")
        infos = compress(
            self._infos[self._index + 1 :] + self._infos[: self._index],
            self._available[self._index + 1 :] + self._available[: self._index],
        )
        info = next(infos)
        self._index = self._infos.index(info)
        if self._index == 0:
            raise StopIteration()
        return self._index

    @property
    def url(self):
        if not hasattr(self.info, "url"):
            self.info.url = self._get_url(self.info)
        return self.info.url

    @property
    def url_scheme(self):
        return self.info.scheme

    @property
    def urls(self):
        if not hasattr(self, "_urls"):
            self._urls = [self._get_url(info) for info in self._infos]
        return self._urls

    @property
    def headers(self):
        return []

    @property
    def data_formats(self):
        return self.info.data_formats

    @property
    def supported_protocols(self):
        return self._protocols

    def reset_reconnection_config(self):
        self._index = 0

    @property
    def data_fmt(self):
        if not self.data_formats:
            return ""
        return self.data_formats[0]

    @abc.abstractmethod
    def _do_get_url(self, info: "StreamServiceInfo") -> str:
        pass

    def _get_url(self, info: "StreamServiceInfo") -> str:
        url = self._do_get_url(info)
        return url

    def __str__(self) -> str:
        urls = "\n\t\t\t   ".join(self.urls)
        s = (
            f"{self.__class__.__name__}\n"
            f"\t\theaders={self.headers},"
            f"data_formats={self.data_formats},"
            f"supported_protocols={self.supported_protocols},"
            f"data_fmt={self.data_fmt}\n"
            f"\t\turls : {urls}"
        )
        return s

    @property
    def api_cfg_key(self):
        return self._api_cfg_key


class DesktopStreamCxnConfig(StreamCxnConfig):
    def __init__(
        self,
        session: "Session",
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"],
        protocols: Union[List[str], str],
        api_cfg_key: str = "",
    ):
        super().__init__(infos, protocols, api_cfg_key=api_cfg_key)
        self._session = session

    @property
    def headers(self):
        app_version = os.getenv("DP_PROXY_APP_VERSION")
        headers = [f"x-tr-applicationid: {self._session.app_key}"]

        if self._session._access_token:
            headers.append(f"Authorization: Bearer {self._session._access_token}")

        if app_version and is_desktop_session(self._session):
            headers.append(f"app-version: {app_version}")

        return headers

    def _do_get_url(self, info: "StreamServiceInfo") -> str:
        return f"{info.scheme.strip()}://{info.host.strip()}:{info.port}/{info.path.strip()}"


class PlatformStreamCxnConfig(StreamCxnConfig):
    def _do_get_url(self, info: "StreamServiceInfo") -> str:
        if self.transport == "tcp":
            return f"{info.host}:{info.port}"
        else:
            path = info.path or "WebSocket"
            return f"{info.scheme.strip()}://{info.host.strip()}:{info.port}/{path.strip()}"


class NullStreamCxnConfig(StreamCxnConfig):
    def __init__(self):
        StreamCxnConfig.__init__(self, [StreamServiceInfo("", "", 0, "", [""], "", "")], [])

    def _do_get_url(self, info) -> str:
        return ""
