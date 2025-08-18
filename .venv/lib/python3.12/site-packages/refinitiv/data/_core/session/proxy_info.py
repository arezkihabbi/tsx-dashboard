from dataclasses import dataclass
from functools import lru_cache
from typing import Union, Tuple, Dict, List
from urllib.request import getproxies

from httpx._utils import get_environment_proxies

from ..._tools import parse_url


@dataclass
class ProxyInfo:
    type: str
    host: str
    port: Union[str, int, None]
    user: Union[str, None]
    password: Union[str, None]

    @property
    def auth(self) -> Union[Tuple[Union[str, None], Union[str, None]], None]:
        if self.user and self.password:
            return self.user, self.password


@dataclass
class StreamProxyInfo(ProxyInfo):
    no_proxy: List[str] = None


@dataclass
class NullStreamProxyInfo(StreamProxyInfo):
    type: None = None
    host: None = None
    port: None = None
    user: None = None
    password: None = None
    no_proxy: None = None


class ProxiesInfo:
    def __init__(self, proxies: Union[str, dict]) -> None:
        self._raw = proxies

    @lru_cache()
    def get_proxy_for_stream(self, url_scheme: str) -> StreamProxyInfo:
        return get_proxy_for_stream(self._raw, url_scheme)

    @lru_cache()
    def get_proxy_for_httpx(self) -> dict:
        return get_proxy_for_httpx(self._raw)


def get_proxy_for_stream(proxies: Union[str, Dict[str, str]], url_scheme: str) -> StreamProxyInfo:
    proxies = proxies or {}

    if proxies and isinstance(proxies, str):
        proxy = _get_proxy_info_from_url(proxies)
        proxies = {proxy.type: proxies}

    env_proxies = _get_proxies_data_from_env()

    url = proxies.get("http", env_proxies.get("http"))
    if url_scheme == "wss":
        url = proxies.get("https", env_proxies.get("https", url))

    retval = _get_stream_proxy_info_from_url(url)

    no_proxy = env_proxies.get("no")
    no_proxy = proxies.get("no", no_proxy)
    if no_proxy:
        no_proxy = no_proxy.split(",")
        retval.no_proxy = no_proxy

    return retval


def get_proxy_for_httpx(proxies: Union[str, Dict[str, str]]) -> Dict[str, str]:
    proxies = proxies or {}
    if proxies and isinstance(proxies, str):
        proxy = _get_proxy_info_from_url(proxies)
        proxies = {proxy.type: proxies}

    proxies = {_sanitize_scheme(scheme): url for scheme, url in proxies.items()}

    env_proxies = get_environment_proxies()

    env_no_proxies = {
        scheme: env_proxies.pop(scheme) for scheme in list(env_proxies.keys()) if env_proxies[scheme] is None
    }
    for scheme, url in env_proxies.items():
        if scheme not in proxies:
            proxies[scheme] = url

    no_proxy = proxies.pop("no", None)
    if no_proxy:
        no_proxy = {url: None for url in no_proxy.split(",")}
    else:
        no_proxy = env_no_proxies
    proxies.update(no_proxy)

    return proxies


def _get_proxies_data_from_env() -> Dict[str, str]:
    proxies = getproxies()
    return {scheme: url for scheme, url in proxies.items()}


def _get_proxy_info_from_url(url: str) -> ProxyInfo:
    return ProxyInfo(**_get_proxy_data_from_url(url))


def _get_stream_proxy_info_from_url(url: str) -> StreamProxyInfo:
    return StreamProxyInfo(**_get_proxy_data_from_url(url)) if url else NullStreamProxyInfo()


def _sanitize_scheme(scheme: str) -> str:
    if scheme in ("http", "all", "https"):
        return f"{scheme}://"
    return scheme


def _get_proxy_data_from_url(url: str) -> dict:
    """Construct a ProxyInfo from a URL (such as http_proxy env var value)"""
    url = parse_url(url)

    username = None
    password = None
    if "@" in url.netloc:
        ident, host_port = url.netloc.rsplit("@", 1)
        if ":" in ident:
            username, password = ident.split(":", 1)

        else:
            password = ident

    else:
        host_port = url.netloc

    port = None
    if ":" in host_port:
        host, port = host_port.split(":", 1)

    else:
        host = host_port

    scheme = url.scheme
    if port:
        port = int(port)

    else:
        try:
            port = dict(https=443, http=80)[scheme]
        except KeyError:
            pass

    return dict(type=scheme, host=host, port=port, user=username, password=password)
