import abc
import json
import pathlib
import threading
import warnings
from typing import List, Optional, TYPE_CHECKING, Union, Dict, Type
from urllib.parse import urlsplit

import httpx

from ._stream_cxn_config_data import StreamServiceInfo, DesktopStreamCxnConfig, PlatformStreamCxnConfig, StreamCxnConfig
from .._data import Request, RequestMethod
from ..._configure import keys
from ..._core.session import SessionCxnType
from ..._errors import ScopeError, RDError
from ..._tools import parse_url, urljoin, get_delays

if TYPE_CHECKING:
    from ..._core.session import Session, PlatformSession
    from ..._configure import _RDPConfig


def get_discovery_url(root_url: str, base_config_name: str, full_config_name: str, config: "_RDPConfig") -> str:
    base_path = config.get_str(f"{base_config_name}.url")

    try:
        endpoint_path = config.get_str(f"{full_config_name}.path")
    except KeyError:
        raise KeyError(f"Cannot find discovery endpoint '{full_config_name}' into config.")

    if base_path.startswith("http"):
        url = base_path
    else:
        url = urljoin(root_url, base_path)

    return urljoin(url, endpoint_path)


def _filter_by_location(locations: List[str], infos: List[StreamServiceInfo]) -> list:
    if not locations:
        return infos

    filtered = []
    for location in locations:
        for info in infos:
            has_location = any(loc.strip().startswith(location) for loc in info.location)
            if has_location and info not in filtered:
                filtered.append(info)

    return filtered


def create_infos(data, transport, port_by_prefix, tier):
    infos = []
    for service in data.get("services", []):
        if service.get("transport") != transport:
            continue

        if tier is not None and "tier" in service:
            tier_range: List[int] = service["tier"]
            if tier < tier_range[0] or tier > tier_range[1]:
                continue

        endpoint_path = pathlib.Path(service.get("endpoint"))
        host = str(endpoint_path.parts[0])
        path = "/".join(endpoint_path.parts[1:])

        scheme = ""
        port = service.get("port")
        if transport == "websocket":
            scheme = port_by_prefix.get(port, "ws")

        infos.append(
            StreamServiceInfo(
                scheme=scheme,
                host=host,
                port=port,
                path=path,
                data_formats=service.get("dataFormat", ["unknown"]),
                location=service.get("location"),
                transport=transport,
            )
        )
    return infos


def get_base_cfg_name(cfg_key: str) -> str:
    return cfg_key.split(".endpoints.")[0]


class CxnConfigProvider(abc.ABC):
    config_class = None
    _port_by_prefix = {
        80: "ws",
        443: "wss",
    }

    def __init__(self) -> None:
        self._start_connecting = threading.Event()
        self._start_connecting.set()
        self._timer = threading.Event()
        self._delays = get_delays()

    def wait_start_connecting(self):
        self._start_connecting.clear()

    def start_connecting(self):
        self._start_connecting.set()

    def get_cfg(self, session: "Session", api_cfg_key: str) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        """
        Parameters
        ----------
        session: Session
        api_cfg_key: str
            Example - "apis.streaming.pricing.endpoints.main"

        Returns
        -------
        PlatformStreamCxnConfig or DesktopStreamCxnConfig

        """
        base_config_name = get_base_cfg_name(api_cfg_key)
        cfg: "_RDPConfig" = session.config

        if cfg.get(f"{base_config_name}.use_rwf", False):
            transport = "tcp"
        else:
            transport = "websocket"

        urls: Union[str, List[str], None] = None

        if transport in {"tcp", "websocket"}:
            urls = cfg.get(f"{api_cfg_key}.direct-url")

        session_cxn_type = session._get_session_cxn_type()
        if urls is not None and session_cxn_type == SessionCxnType.DESKTOP:
            warnings.warn(
                "direct-url config parameter cannot be used with desktop session, "
                f"the '{api_cfg_key}.direct-url' parameter will be discarded."
            )
            urls = None

        if urls is not None:
            if not isinstance(urls, list):
                urls = [urls]

            infos = [self.info_from_url(transport, url) for url in urls]

        else:
            infos = self._request_infos(
                discovery_url=get_discovery_url(session._get_rdp_url_root(), base_config_name, api_cfg_key, cfg),
                api_cfg_key=api_cfg_key,
                config=cfg,
                session=session,
                transport=transport,
            )

        protocols = cfg.get_list(f"{api_cfg_key}.protocols")
        return self._create_cfg(session, infos, protocols, transport, api_cfg_key)

    @staticmethod
    def info_from_url(transport: str, url: str, data_formats=None) -> StreamServiceInfo:
        if data_formats is None:
            data_formats = ["unknown"]

        # If there is no scheme or netloc add netloc marker to make it valid URL
        if not ("://" in url or url.startswith("//")) and not url.startswith("/"):
            url = "//" + url
        url = url.strip()

        result = parse_url(url)
        scheme = result.scheme
        host = result.hostname
        port = result.port
        path = result.path

        # If url parsing did not get valid hostname, raise exception
        if not host:
            raise ValueError(f"Invalid URL: {url}")

        if not scheme and transport == "websocket":
            scheme = "wss" if port == 443 else "ws"

        return StreamServiceInfo(
            scheme=scheme or "",
            host=host,
            port=port or 80,
            path=path or "",
            data_formats=data_formats,
            location="",
            transport=transport,
        )

    def _request_infos(
        self,
        discovery_url: str,
        api_cfg_key: str,
        config: "_RDPConfig",
        session: "Session",
        transport: str = "websocket",
    ) -> List[StreamServiceInfo]:
        method = RequestMethod.GET
        path = urlsplit(discovery_url).path
        try:
            session.verify_scope(path, method)
        except ScopeError as e:
            session.error(
                f"Insufficient Scope. Cannot load the list of associated URLs "
                f"from {discovery_url} for {api_cfg_key} endpoint."
            )
            raise e
        tier: Optional[int] = config.get(f"{get_base_cfg_name(api_cfg_key)}.tier")

        server_mode = session.server_mode
        request = Request(
            url=discovery_url,
            method=method,
            # server won't accept tier: false
            params={"tier": True} if tier else {},
            auto_retry=True,
            path=path,
        )
        response = None
        while True:
            self._start_connecting.wait()
            try:
                response = session.http_request(request)
            except httpx.HTTPError:
                if server_mode is True:
                    delay = self._delays.next()
                    session._is_debug() and session.debug(
                        f"CxnConfigProvider waiting {delay} secs until the next attempt."
                    )
                    self._timer.wait(delay)
                    continue
            break

        try:
            data = response.json()
        except (AttributeError, json.decoder.JSONDecodeError):
            message = f"Cannot load the list of associated URLs from {discovery_url} for {api_cfg_key} endpoint."
            session.error(message)
            raise ConnectionError(message) from None

        err = data.get("error")
        if err:
            if response.status_code == 403:
                session._handle_insufficient_scope(request.path, request.method, err.get("message"))
            raise RDError(response.status_code, err.get("message"))

        infos = create_infos(data, transport, self._port_by_prefix, tier)
        return self._filter_infos(infos, api_cfg_key, config)

    def _filter_infos(
        self,
        infos: List[StreamServiceInfo],
        api_cfg_key: str,
        cfg: "_RDPConfig",
    ) -> List[StreamServiceInfo]:
        return infos

    def _create_cfg(
        self,
        session: "Session",
        infos: List[StreamServiceInfo],
        protocols: List[str],
        transport: str = "websocket",
        api_cfg_key: str = "",
    ) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        return self.config_class(infos, protocols, transport, api_cfg_key)


class DesktopCxnConfigProvider(CxnConfigProvider):
    config_class = DesktopStreamCxnConfig

    def _create_cfg(
        self,
        session: "Session",
        infos: List[StreamServiceInfo],
        protocols: List[str],
        transport: str = "websocket",
        api_cfg_key: str = "",
    ) -> Union[PlatformStreamCxnConfig, DesktopStreamCxnConfig]:
        return self.config_class(session, infos, protocols, api_cfg_key)


class PlatformCxnConfigProvider(CxnConfigProvider):
    config_class = PlatformStreamCxnConfig

    def _filter_infos(
        self,
        infos: List[StreamServiceInfo],
        api_cfg_key: str,
        cfg: "_RDPConfig",
    ) -> List[StreamServiceInfo]:
        locations = cfg.get_list(f"{api_cfg_key}.locations")
        return _filter_by_location(locations, infos)


class DeployedCxnConfigProvider(CxnConfigProvider):
    def get_cfg(self, session: "PlatformSession", api_cfg_key: str) -> PlatformStreamCxnConfig:
        url: str = session._deployed_platform_host
        cfg: "_RDPConfig" = session.config

        if url is None:
            session_name: str = session.name
            key = keys.platform_realtime_distribution_system(session_name)
            url_key = f"{key}.url"
            url = cfg.get_str(url_key)

        if cfg.get(f"{get_base_cfg_name(api_cfg_key)}.use_rwf", False):
            transport = "tcp"
            data_formats = None
        else:
            transport = "websocket"
            data_formats = ["tr_json2"]

        info = self.info_from_url(transport, url, data_formats=data_formats)

        return PlatformStreamCxnConfig(info, "OMM", transport=transport)


class PlatformAndDeployedCxnConfigProvider(DeployedCxnConfigProvider, PlatformCxnConfigProvider):
    def get_cfg(self, session: "PlatformSession", api_cfg_key: str) -> StreamCxnConfig:
        if api_cfg_key.startswith("apis.streaming.pricing.endpoints.main"):
            cxn_config = DeployedCxnConfigProvider.get_cfg(self, session, api_cfg_key)

        else:
            cxn_config = PlatformCxnConfigProvider.get_cfg(self, session, api_cfg_key)

        return cxn_config


provider_class_by_session_cxn_type: Dict[SessionCxnType, Type[CxnConfigProvider]] = {
    SessionCxnType.DEPLOYED: DeployedCxnConfigProvider,
    SessionCxnType.REFINITIV_DATA: PlatformCxnConfigProvider,
    SessionCxnType.REFINITIV_DATA_AND_DEPLOYED: PlatformAndDeployedCxnConfigProvider,
    SessionCxnType.DESKTOP: DesktopCxnConfigProvider,
}

cache_provider_by_session = {}


def get_cxn_config(api_config_key: str, session: "Session") -> StreamCxnConfig:
    return get_cxn_cfg_provider(session).get_cfg(session, api_config_key)


def get_cxn_cfg_provider(session: "Session") -> CxnConfigProvider:
    session_cxn_type = session._get_session_cxn_type()
    provider_class = provider_class_by_session_cxn_type.get(session_cxn_type)

    if not provider_class:
        raise ValueError(f"Can't find provider_class by session_cxn_type={session_cxn_type}")

    return cache_provider_by_session.setdefault(session, provider_class())


def release_cxn_cfg_provider(session: "Session") -> None:
    cache_provider_by_session.pop(session, None)
