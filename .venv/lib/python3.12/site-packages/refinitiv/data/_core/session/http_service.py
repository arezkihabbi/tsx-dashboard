import os
import re
import threading
from typing import TYPE_CHECKING, Union

import httpx

from ._retry_transport import RequestRetryException, RetryAsyncTransport, RetryTransport
from .tools import is_desktop_session
from ..log_reporter import LogReporter
from ... import _configure as configure
from ..._tools import cached_property

if TYPE_CHECKING:
    from ...delivery._data._data_provider import Request
    from ._session import Session

APPLICATION_JSON = "application/json"
HTTPX_VERSION = "0.20.0"


def get_http_limits(config):
    max_connections = config.get(configure.keys.http_max_connections)
    max_keepalive_connections = config.get(configure.keys.http_max_keepalive_connections)
    limits = httpx.Limits(
        max_connections=max_connections,
        max_keepalive_connections=max_keepalive_connections,
    )
    return limits


def get_http_request_timeout_secs(session):
    """the default http request timeout in secs"""
    key = configure.keys.http_request_timeout
    value = session.config.get(key)

    is_list = isinstance(value, list)
    if is_list and len(value) == 1:
        value = value[0]
        try:
            value = int(value)
        except ValueError:
            pass

    number = isinstance(value, int) or isinstance(value, float)
    negative_number = number and value < 0

    if number and value == 0:
        value = None
    elif number and value == 1:
        value = 1

    is_none = value is None

    set_default = not is_none and (not number or negative_number)

    if set_default:
        value = configure.defaults.http_request_timeout
        session.warning(f"Invalid value of the {key}. Default value is used")

    return value


class BaseHTTPClient(LogReporter):
    _client: Union[httpx.Client, httpx.AsyncClient, None]
    _auto_retry_client: Union[httpx.Client, httpx.AsyncClient, None]

    _err_still_in_flight_pattern = re.compile(
        r"The connection pool was closed while [0-9]+ HTTP requests/responses were still in-flight."
    )

    def __init__(self, session: "Session") -> None:
        super().__init__(session.logger())
        self._session: "Session" = session

    def is_closed(self) -> bool:
        client = self._client
        return client is None or client.is_closed

    def build_request(self, client: Union[httpx.AsyncClient, httpx.Client], request: "Request") -> httpx.Request:
        headers = request.headers
        timeout = request.timeout or get_http_request_timeout_secs(self._session)

        access_token = self._session._access_token
        if access_token is not None:
            headers["Authorization"] = "Bearer {}".format(access_token)

        closure = request.closure
        if closure is not None:
            headers["Closure"] = closure

        cookies = None

        if is_desktop_session(self._session):
            proxy_app_version = os.getenv("DP_PROXY_APP_VERSION")
            user_uuid = os.getenv("REFINITIV_AAA_USER_ID")

            if proxy_app_version:
                headers.update({"app-version": proxy_app_version})

            if user_uuid:
                cookies = {"user-uuid": user_uuid}

        headers.setdefault("x-tr-applicationid", self._session.app_key)

        method = request.method

        self.is_debug() and self.debug(
            (f"HTTP Request id {request.id}\n")
            + (f"\turl = {request.url}\n" if request.url else "")
            + (f"\tmethod = {method}\n")
            + (f"\theaders = {headers}\n" if headers else "")
            + (f"\tparams = {request.params}\n" if request.params else "")
            + (f"\tcookies = {cookies}\n" if cookies else "")
            + (f"\tdata = {request.data}\n" if request.data else "")
            + (f"\tjson = {request.json}" if request.json else "")
        )

        if httpx.__version__ < HTTPX_VERSION:
            request = client.build_request(
                method=method,
                url=request.url,
                data=request.data,
                json=request.json,
                params=request.params,
                headers=headers,
                cookies=cookies,
            )
            request.timeout = timeout

        else:
            request = client.build_request(
                method=method,
                url=request.url,
                data=request.data,
                json=request.json,
                params=request.params,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
            )

        return request

    def assert_err_still_in_flight(self, exception):
        if not self._err_still_in_flight_pattern.match(str(exception)):
            raise exception


def get_httpx_client(proxies, **kwargs):
    if httpx.__version__ >= "0.26.0":
        client = httpx.Client(proxy=proxies, **kwargs)
    else:
        client = httpx.Client(proxies=proxies, **kwargs)
    return client


def get_httpx_client_async(proxies, **kwargs):
    if httpx.__version__ >= "0.26.0":
        client = httpx.AsyncClient(proxy=proxies, **kwargs)
    else:
        client = httpx.AsyncClient(proxies=proxies, **kwargs)
    return client


class HTTPClient(BaseHTTPClient):
    def __init__(self, session: "Session") -> None:
        super().__init__(session)
        self._client: Union[httpx.Client, httpx.AsyncClient, None] = None
        self._auto_retry_client: Union[httpx.Client, httpx.AsyncClient, None] = None

    def open(self):
        config = self._session.config
        limits = get_http_limits(config)
        proxies = self._session._proxies.get_proxy_for_httpx()

        # httpx has its default Accept header and
        # server wants application/json or nothing
        self._client = get_httpx_client(
            headers={"Accept": APPLICATION_JSON},
            limits=limits,
            proxies=proxies,
        )

        key = configure.keys.http_auto_retry_config
        auto_retry_config = config.get(key, None)

        if auto_retry_config:
            number_of_retries = auto_retry_config.get("number-of-retries", 3)
            retry_on_errors = auto_retry_config.get("on-errors", [])
            retry_backoff_factor = auto_retry_config.get("backoff-factor", 1)
            retry_on_methods = auto_retry_config.get("on-methods", ["GET", "POST"])

            retry_transport = RetryTransport(
                total_attempts=number_of_retries,
                on_statuses=retry_on_errors,
                on_methods=retry_on_methods,
                backoff_factor=retry_backoff_factor,
            )
            self._auto_retry_client = get_httpx_client(transport=retry_transport, proxies=proxies)

    def close(self):
        if self._client:
            try:
                self._client.close()
                self._client = None
            except RuntimeError as e:
                self.assert_err_still_in_flight(e)

        if self._auto_retry_client:
            try:
                self._auto_retry_client.close()
                self._auto_retry_client = None
            except RuntimeError as e:
                self.assert_err_still_in_flight(e)

    def send(self, request: "Request") -> httpx.Response:
        client = self._auto_retry_client if request.auto_retry else self._client
        request = self.build_request(client, request)

        if httpx.__version__ < HTTPX_VERSION:
            response = client.send(request, timeout=request.timeout, follow_redirects=True)

        else:
            response = client.send(request, follow_redirects=True)

        return response


class AsyncHTTPClient(BaseHTTPClient):
    @property
    def _client(self) -> httpx.AsyncClient:
        return getattr(threading.current_thread(), "async_httpclient", None)

    @_client.setter
    def _client(self, value):
        setattr(threading.current_thread(), "async_httpclient", value)

    @property
    def _auto_retry_client(self) -> httpx.AsyncClient:
        return getattr(threading.current_thread(), "async_retry_httpclient", None)

    @_auto_retry_client.setter
    def _auto_retry_client(self, value):
        setattr(threading.current_thread(), "async_retry_httpclient", value)

    async def open_async(self):
        client = self._client
        retry_client = self._auto_retry_client
        proxies = self._session._proxies.get_proxy_for_httpx()

        config = self._session.config

        if client is None or client.is_closed:
            # httpx has its default Accept header and
            # server wants application/json or nothing
            self._client = get_httpx_client_async(
                headers={"Accept": APPLICATION_JSON}, limits=get_http_limits(config), proxies=proxies
            )

        retry_config = config.get(configure.keys.http_auto_retry_config, None)

        if retry_config and (retry_client is None or retry_client.is_closed):
            retry_transport = RetryAsyncTransport(
                total_attempts=retry_config.get("number-of-retries", 3),
                on_statuses=retry_config.get("on-errors", []),
                on_methods=retry_config.get("on-methods", ["GET", "POST"]),
                backoff_factor=retry_config.get("backoff-factor", 1),
            )
            self._auto_retry_client = get_httpx_client_async(transport=retry_transport, proxies=proxies)

    async def close_async(self):
        client = self._client
        retry_client = self._auto_retry_client

        if client:
            try:
                await client.aclose()
                self._client = None
            except RuntimeError as e:
                self.assert_err_still_in_flight(e)

        if retry_client:
            try:
                await retry_client.aclose()
                self._auto_retry_client = None
            except RuntimeError as e:
                self.assert_err_still_in_flight(e)

    async def send(self, request: "Request") -> httpx.Response:
        client = self._auto_retry_client if request.auto_retry else self._client

        if client is None or client.is_closed:
            await self.open_async()
            client = self._auto_retry_client if request.auto_retry else self._client

        request = self.build_request(client, request)

        if httpx.__version__ < HTTPX_VERSION:
            response = await client.send(request, timeout=request.timeout, follow_redirects=True)

        else:
            response = await client.send(request, follow_redirects=True)

        return response


class HTTPService(LogReporter):
    def __init__(self, session: "Session") -> None:
        super().__init__(session.logger())
        self._session: "Session" = session

    @cached_property
    def _client(self) -> HTTPClient:
        return HTTPClient(self._session)

    @cached_property
    def _client_async(self) -> AsyncHTTPClient:
        return AsyncHTTPClient(self._session)

    @property
    def request_timeout_secs(self):
        return get_http_request_timeout_secs(self._session)

    def open(self):
        self._client.open()

    def close(self):
        self._client.close()

    def request(self, request: "Request") -> httpx.Response:
        if self._client.is_closed():
            self._client.open()

        try:
            response = self._client.send(request)
        except RequestRetryException as error:
            self.error(error)
            raise error
        except (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.HTTPStatusError,
            httpx.InvalidURL,
            httpx.LocalProtocolError,
            httpx.NetworkError,
            httpx.ProtocolError,
            httpx.ProxyError,
            httpx.ReadError,
            httpx.RequestError,
            httpx.ReadTimeout,
            httpx.RemoteProtocolError,
            httpx.TooManyRedirects,
            httpx.TransportError,
            httpx.TimeoutException,
        ) as error:
            self.error(f"An error occurred while requesting {error.request.url!r}.\n\t{error!r}")
            raise error

        self.is_debug() and self.debug(
            f"HTTP Response id {request.id}\n\tstatus_code = {response.status_code}\n\ttext = {response.text}"
        )
        return response

    async def open_async(self):
        await self._client_async.open_async()

    async def close_async(self):
        await self._client_async.close_async()

    async def request_async(self, request: "Request") -> httpx.Response:
        if self._client_async.is_closed():
            await self._client_async.open_async()

        try:
            response = await self._client_async.send(request)
        except RequestRetryException as error:
            self.error(error)
            raise error
        except (
            httpx.ConnectError,
            httpx.ConnectTimeout,
            httpx.HTTPStatusError,
            httpx.InvalidURL,
            httpx.LocalProtocolError,
            httpx.NetworkError,
            httpx.ProtocolError,
            httpx.ProxyError,
            httpx.ReadError,
            httpx.RequestError,
            httpx.ReadTimeout,
            httpx.RemoteProtocolError,
            httpx.TooManyRedirects,
            httpx.TransportError,
            httpx.TimeoutException,
        ) as error:
            self.error(f"An error occurred while requesting {error.request.url!r}.\n\t{error!r}")
            raise error

        self.is_debug() and self.debug(
            f"HTTP Response id {request.id}\n\tstatus_code = {response.status_code}\n\ttext = {response.text}"
        )
        return response


def get_service(session: "Session") -> HTTPService:
    return HTTPService(session)
