import asyncio
import threading
import time
from typing import TYPE_CHECKING, Optional, Callable

from .._content_provider_layer import ContentProviderLayer
from ..._core.session import get_valid_session
from ..._tools import urljoin
from ...delivery._data._data_provider import emit_event
from ...delivery._data._endpoint_data import RequestMethod, Error

if TYPE_CHECKING:
    from ...delivery._data._data_provider import Response
    from ..._configure import _RDPConfig
    from ..._core.session import Session

DELAY_BEFORE_FIRST_GET_ASYNC_OPERATION = 0.3
DELAY_BETWEEN_TWO_GET_ASYNC_OPERATION = 5


class IPAContentProviderLayer(ContentProviderLayer):
    def __init__(self, content_type, **kwargs):
        super().__init__(content_type, **kwargs)
        self._lock: Optional[threading.Lock] = None
        self._lock_async: Optional[asyncio.Lock] = None
        self._async_url: Optional[str] = None
        self._operation_url: Optional[str] = None
        self._resource_url: Optional[str] = None
        self._delay_before_first_get_operation: Optional[int] = None
        self._delay_between_two_get_operation: Optional[int] = None
        self._config: Optional["_RDPConfig"] = None
        self._session: Optional["Session"] = None

    def _read_config(self):
        from ...delivery._data._data_provider_factory import get_base_url, get_api_config

        base_url = get_base_url(self._content_type, self._config)
        api_config = get_api_config(self._content_type, self._config)
        self._operation_url = urljoin(base_url, api_config.get("endpoints.async-operation"))
        self._resource_url = urljoin(base_url, api_config.get("endpoints.async-resource"))
        self._delay_before_first_get_operation = api_config.get(
            "delay-before-first-get-async-operation",
            DELAY_BEFORE_FIRST_GET_ASYNC_OPERATION,
        )
        self._delay_between_two_get_operation = api_config.get(
            "delay-between-two-get-async-operation",
            DELAY_BETWEEN_TWO_GET_ASYNC_OPERATION,
        )

    def _check_initial_response(self, initial_response: "Response") -> bool:
        check_failed = False

        # At this step, normal response should have 202 status code,
        # "Accepted" error message and location header
        status_code = initial_response.raw.status_code
        if status_code != 202:
            check_failed = True
            first_error = initial_response.errors[0]
            err_msg = first_error.message
            err_msg = f"Async IPA response status code {status_code}|{err_msg} != 202|Accepted"
            self._session.error(err_msg)
            self._write_error(initial_response, first_error.code, err_msg)

        location = initial_response.raw.headers.get("location")
        if not location:
            check_failed = True
            err_msg = "IPA Asynchronous request operation failed, response doesn't contain location."
            self._session.error(err_msg)
            self._write_error(initial_response, 0, err_msg)

        return check_failed

    def _check_operation_response(self, operation_response: "Response") -> bool:
        check_failed = False
        resource_location = operation_response.data.raw.get("resourceLocation")
        if not resource_location:
            check_failed = True
            err_msg = "IPA Asynchronous request resource failed, operation response doesn't contain resource location."
            self._session.error(err_msg)
            self._write_error(operation_response, 0, err_msg)

        return check_failed

    def _write_error(self, response: "Response", err_code: int, err_msg: str):
        error = Error(err_code, err_msg)
        response.errors.append(error)
        response.is_success = False

    def _raise_error_no_async_url(self):
        raise AttributeError(f"Asynchronous endpoint is not available for this content provider")

    def get_data(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        async_mode: Optional[bool] = None,
    ):
        from ...delivery._data._data_provider_factory import get_url

        self._session = get_valid_session(session)
        self._config: "_RDPConfig" = self._session.config
        self._async_url = get_url(self._content_type, self._config, request_mode="async")
        response = None

        if async_mode and self._async_url:
            self._lock = threading.Lock()
            self._read_config()
            response = self._get_data_with_async_mode()
            on_response and emit_event(on_response, response, self, session)
            self._check_response(response, self._config)

        elif async_mode and not self._async_url:
            self._raise_error_no_async_url()

        else:
            response = super().get_data(session, on_response)

        return response

    def _get_data_with_async_mode(self) -> "Response":
        initial_response = self._provider.get_data(self._session, self._async_url, **self._kwargs)

        check_failed = self._check_initial_response(initial_response)
        if check_failed:
            return initial_response

        operation_response = None
        location = initial_response.raw.headers.get("location")
        operation_id = location.rsplit("/", 1)[-1]
        url = urljoin(self._operation_url, operation_id)
        loop_retrieving = True
        is_debug = self._session._is_debug()
        while loop_retrieving:
            # wait before requesting operation status
            time.sleep(self._delay_before_first_get_operation)
            # while request operation not succeeded or not failed, request operation

            with self._lock:
                is_debug and self._session.debug(f"Request operation :\n {url}")
                operation_response = self._provider.get_data(
                    self._session, url, method=RequestMethod.GET, **self._kwargs
                )

            status_code = operation_response.raw.status_code
            if status_code != 200:
                # operation status should be 200, otherwise,
                # it failed, then return response as an error
                return operation_response

            status_text = operation_response.data.raw.get("status")
            if status_text in {"failed", "succeeded"}:
                # request succeeded or failed, in both cases,
                # stop to wait and retrieve result
                loop_retrieving = False
            else:
                # wait for 5 sec before next request
                time.sleep(self._delay_between_two_get_operation)

        check_failed = self._check_operation_response(operation_response)
        if check_failed:
            return operation_response

        with self._lock:
            resource_location = operation_response.data.raw.get("resourceLocation")
            resource_id = resource_location.rsplit("/", 1)[-1]
            url = urljoin(self._resource_url, resource_id)
            is_debug and self._session.debug(f"Request resource :\n {url}")
            resource_response = self._provider.get_data(self._session, url, method=RequestMethod.GET, **self._kwargs)

        return resource_response

    async def get_data_async(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        async_mode: Optional[bool] = None,
        closure: Optional[str] = None,
    ):
        from ...delivery._data._data_provider_factory import get_url

        self._session = get_valid_session(session)
        self._config: "_RDPConfig" = self._session.config
        self._async_url = get_url(self._content_type, self._config, request_mode="async")
        response = None

        if async_mode and self._async_url:
            self._lock_async = asyncio.Lock()
            self._read_config()
            response = await self._get_data_with_async_mode_async()
            on_response and emit_event(on_response, response, self, session)
            self._check_response(response, self._config)

        elif async_mode and not self._async_url:
            self._raise_error_no_async_url()

        else:
            response = await super().get_data_async(session, on_response, closure)

        return response

    async def _get_data_with_async_mode_async(self):
        initial_response = await self._provider.get_data_async(self._session, self._async_url, **self._kwargs)

        check_failed = self._check_initial_response(initial_response)
        if check_failed:
            return initial_response

        operation_response = None
        location = initial_response.raw.headers.get("location")
        operation_id = location.rsplit("/", 1)[-1]
        url = urljoin(self._operation_url, operation_id)
        loop_retrieving = True
        is_debug = self._session._is_debug()
        while loop_retrieving:
            # wait before requesting operation status
            await asyncio.sleep(self._delay_before_first_get_operation)
            # while request operation not succeeded or not failed, request operation

            async with self._lock_async:
                is_debug and self._session.debug(f"Request operation :\n {url}")
                operation_response = await self._provider.get_data_async(
                    self._session, url, method=RequestMethod.GET, **self._kwargs
                )

            status_code = operation_response.raw.status_code
            if status_code != 200:
                # operation status should be 200, otherwise,
                # it failed, then return response as an error
                return operation_response

            status_text = operation_response.data.raw.get("status")
            if status_text in {"failed", "succeeded"}:
                # request succeeded or failed, in both cases,
                # stop to wait and retrieve result
                loop_retrieving = False
            else:
                # wait for 5 sec before next request
                await asyncio.sleep(self._delay_between_two_get_operation)

        check_failed = self._check_operation_response(operation_response)
        if check_failed:
            return operation_response

        async with self._lock_async:
            resource_location = operation_response.data.raw.get("resourceLocation")
            resource_id = resource_location.rsplit("/", 1)[-1]
            url = urljoin(self._resource_url, resource_id)
            is_debug and self._session.debug(f"Request resource :\n {url}")
            resource_response = await self._provider.get_data_async(
                self._session, url, method=RequestMethod.GET, **self._kwargs
            )

        return resource_response
