import typing as t

from httpx import Response, Request, HTTPTransport, AsyncHTTPTransport
from httpx import __version__ as _HTTPX_VERSION
from refinitiv.data._log import get_logger, is_debug
from tenacity import (
    wait_exponential,
    Retrying,
    AsyncRetrying,
    stop_after_attempt,
    stop_after_delay,
)

from ...errors import RDError


class RequestRetryException(RDError):
    pass


class RequestTimeout(RequestRetryException):
    def __init__(
        self,
        timeout: float,
        total_time: float,
        attempts_count: int,
        attempts_max: int,
        url: str,
        method: str,
    ):
        self.timeout = timeout
        self.total_time = total_time
        self.attempts_count = attempts_count
        self.attempts_max = attempts_max
        self.url = url
        self.method = method
        super().__init__(
            -1,
            f"{method} request to {url} failed : "
            f"Timeout of {timeout} exceeded for retrying. "
            f"Total attempts: {attempts_count}",
        )


class RequestAttemptsExhausted(RequestRetryException):
    def __init__(
        self,
        timeout: float,
        total_time: float,
        attempts_count: int,
        attempts_max: int,
        url: str,
        method: str,
    ):
        self.timeout = timeout
        self.total_time = total_time
        self.attempts_count = attempts_count
        self.attempts_max = attempts_max
        self.url = url
        self.method = method
        super().__init__(
            -1,
            f"{method} request to {url} failed : "
            f"Max attempts count ({attempts_max}) exceeded for retrying. "
            f"Retry time: {total_time}",
        )


class _RetryTransportBase:
    def __init__(
        self,
        retrying_cls: t.Union[t.Type[Retrying], t.Type[AsyncRetrying]],
        total_timeout: float = 0,
        total_attempts: int = 10,
        on_statuses: t.Optional[t.Iterable[int]] = None,
        on_methods: t.Optional[t.Iterable[str]] = None,
        backoff_factor: float = 0,
    ):
        self._total_timeout = total_timeout
        self._total_attempts = total_attempts
        self._on_statuses: set = set(on_statuses or [])
        self._on_methods: set = set(map(str.upper, on_methods or []))
        self._backoff_factor = backoff_factor
        stop_condition = stop_after_attempt(total_attempts)
        self._logger = get_logger("RetryTransportBase")

        if self._total_timeout > 0:
            stop_condition |= stop_after_delay(self._total_timeout)
        self._retrying = retrying_cls(
            wait=wait_exponential(multiplier=backoff_factor),
            stop=stop_condition,
            reraise=True,
        )

    if "0.18" <= _HTTPX_VERSION < "0.20":

        def _handle_retry_exception(self, url, method, exc: RequestRetryException):
            stats = self._retrying.statistics
            if self._total_timeout and 0 < self._total_timeout <= stats["delay_since_first_attempt"]:
                raise RequestTimeout(
                    self._total_timeout,
                    stats["delay_since_first_attempt"],
                    stats["attempt_number"],
                    self._total_attempts,
                    url,
                    method,
                ) from exc
            elif stats["attempt_number"] >= self._total_attempts:
                raise RequestAttemptsExhausted(
                    self._total_timeout,
                    stats["delay_since_first_attempt"],
                    stats["attempt_number"],
                    self._total_attempts,
                    url,
                    method,
                ) from exc
            else:
                raise exc

        def _check_response(self, method: bytes, response: tuple):
            status_code, *_ = response
            if method.decode() in self._on_methods and status_code in self._on_statuses:
                raise RequestRetryException(
                    -1,
                    f"Request failed and will be retried: status code - {status_code}",
                )
            return response

    else:

        def _handle_retry_exception(self, request: Request, exc: RequestRetryException):
            stats = self._retrying.statistics
            if self._total_timeout and 0 < self._total_timeout <= stats["delay_since_first_attempt"]:
                raise RequestTimeout(
                    self._total_timeout,
                    stats["delay_since_first_attempt"],
                    stats["attempt_number"],
                    self._total_attempts,
                    request.url,
                    request.method,
                ) from exc
            elif stats["attempt_number"] >= self._total_attempts:
                raise RequestAttemptsExhausted(
                    self._total_timeout,
                    stats["delay_since_first_attempt"],
                    stats["attempt_number"],
                    self._total_attempts,
                    request.url,
                    request.method,
                ) from exc
            else:
                raise exc

        def _check_response(self, request: Request, response: Response):
            if request.method in self._on_methods and response.status_code in self._on_statuses:
                raise RequestRetryException(
                    -1,
                    f"Request failed and will be retried: status code - {response.status_code}",
                )
            return response


class RetryTransport(HTTPTransport, _RetryTransportBase):
    """
    Synchronous HTTP Transport with retry functionality

    Synchronous HTTP Transport with retry functionality that uses formula
     2^x * backoff_factor. Retry happens only if method is in the on_methods iterable
     and status code is in on_statuses iterable and/or if other network errors
     happen(connections issues, timeouts, etc).
     Otherwise the response is returned as is.

    Attributes
    ----------
    total_timeout : float
        Maximum time to keep retrying the request
    total_attempts: int
        Maximum count of attempts to try the request
    on_statuses: Iterable[int]
        Iterable of http status codes on which the retry should happen
    on_methods: Iterable[str]
        Iterable of http methods on which the retry should happen
    backoff_factor: float
        Multiplier to the exponential function
    **transport_kwargs: dict
        Keyword arguments to HTTPTransport
    Examples
    --------
        >>> from httpx import Client
        >>> transport = RetryTransport(total_timeout=10,
        >>>                            total_attempts=5,
        >>>                            on_statuses=[429, 501],
        >>>                            on_methods=['POST', 'GET'],
        >>>                            backoff_factor=2)
        >>> client = Client(transport=transport)

    """

    def __init__(
        self,
        total_timeout: float = 0,
        total_attempts: int = 10,
        on_statuses: t.Optional[t.Iterable[int]] = None,
        on_methods: t.Optional[t.Iterable[str]] = None,
        backoff_factor: float = 0,
        **transport_kwargs,
    ):
        HTTPTransport.__init__(self, **transport_kwargs)
        _RetryTransportBase.__init__(
            self,
            Retrying,
            total_timeout,
            total_attempts,
            on_statuses,
            on_methods,
            backoff_factor,
        )

    if "0.18" <= _HTTPX_VERSION < "0.20":

        def _handle_request(self, method: bytes, *args, **kwargs) -> tuple:
            return self._check_response(method, super().handle_request(method, *args, **kwargs))

        def handle_request(
            self,
            method: bytes,
            url: t.Tuple[bytes, bytes, t.Optional[int], bytes],
            *args,
            **kwargs,
        ) -> tuple:
            try:
                return self._retrying(self._handle_request, method, url, *args, **kwargs)
            except RequestRetryException as exc:
                self._handle_retry_exception(url, method, exc)

    else:  # For version 0.20+

        def _handle_request(self, request: Request) -> Response:
            is_debug(self._logger) and self._logger.debug(f"Sending request to {request.url}")
            return self._check_response(request, super().handle_request(request=request))

        def handle_request(self, request: Request) -> Response:
            try:
                return self._retrying(self._handle_request, request)
            except RequestRetryException as exc:
                self._handle_retry_exception(request, exc)


class RetryAsyncTransport(AsyncHTTPTransport, _RetryTransportBase):
    """
    Asynchronous HTTP Transport with retry functionality

    Asynchronous HTTP Transport with retry functionality that uses formula
     2^x * backoff_factor. Retry happens only if method is in the on_methods iterable
     and status code is in on_statuses iterable and/or if other network errors
     happen(connections issues, timeouts, etc).
     Otherwise the response is returned as is.

    Attributes
    ----------
    total_timeout : float
        Maximum time to keep retrying the request
    total_attempts: int
        Maximum count of attempts to try the request
    on_statuses: Iterable[int]
        Iterable of http status codes on which the retry should happen
    on_methods: Iterable[str]
        Iterable of http methods on which the retry should happen
    backoff_factor: float
        Multiplier to the exponential function
    **transport_kwargs: dict
        Keyword arguments to AsyncHTTPTransport
    Examples
    --------
        >>> from httpx import AsyncClient
        >>> transport = RetryAsyncTransport(total_timeout=10,
        >>>                                 total_attempts=5,
        >>>                                 on_statuses=[429, 501],
        >>>                                 on_methods=['POST', 'GET'],
        >>>                                 backoff_factor=2)
        >>> client = AsyncClient(transport=transport)

    """

    def __init__(
        self,
        total_timeout: float = 0,
        total_attempts: int = 10,
        on_statuses: t.Optional[t.Iterable[int]] = None,
        on_methods: t.Optional[t.Iterable[str]] = None,
        backoff_factor: float = 0,
        **transport_kwargs,
    ):
        AsyncHTTPTransport.__init__(self, **transport_kwargs)
        _RetryTransportBase.__init__(
            self,
            AsyncRetrying,
            total_timeout,
            total_attempts,
            on_statuses,
            on_methods,
            backoff_factor,
        )

    if "0.18" <= _HTTPX_VERSION < "0.20":

        async def _handle_async_request(self, method: bytes, *args, **kwargs) -> tuple:
            return self._check_response(method, await super().handle_async_request(method, *args, **kwargs))

        async def handle_async_request(
            self,
            method: bytes,
            url: t.Tuple[bytes, bytes, t.Optional[int], bytes],
            *args,
            **kwargs,
        ) -> tuple:
            try:
                return await self._retrying(self._handle_async_request, method, url, *args, **kwargs)
            except RequestRetryException as exc:
                self._handle_retry_exception(url, method, exc)

    else:

        async def _handle_async_request(self, request: Request) -> Response:
            return self._check_response(request, await super().handle_async_request(request=request))

        async def handle_async_request(self, request: Request) -> Response:
            try:
                return await self._retrying(self._handle_async_request, request)
            except RequestRetryException as exc:
                self._handle_retry_exception(request, exc)
