import traceback
import warnings
from typing import Generic, Optional, Callable, TYPE_CHECKING, Any

from ._response import Response, TypeData
from ..._configure import _RDPConfig
from ..._core.session._default_session_manager import get_valid_session
from ..._tools import DEBUG
from ...errors import RDError
from ...usage_collection._filter_types import FilterType
from ...usage_collection._logger import get_usage_logger
from ...usage_collection._utils import ModuleName

if TYPE_CHECKING:
    from ..._core.session import Session


def _check_response(response: Response, config: "_RDPConfig", response_class=Response) -> None:
    if isinstance(response, response_class):
        is_raise_exception = config.get_param("raise_exception_on_error")
        if not response.is_success and is_raise_exception:
            error_code = response.errors[0].code
            error_message = response.errors[0].message
            exception_class = getattr(response, "exception_class", None)

            if exception_class:
                error = exception_class(error_code, error_message)

            else:
                error = RDError(error_code, error_message)

            error.response = response
            raise error


def get_data(data_type, provider, session, **kwargs):
    from ._data_provider_factory import get_url, get_api_config

    session = get_valid_session(session)
    config = session.config
    url = get_url(data_type, config)
    api_config = get_api_config(data_type, config)
    auto_retry = api_config.get("auto-retry", False)
    # Library usage logging
    get_usage_logger().log_func(
        name=f"{ModuleName.DELIVERY}.{DataProviderLayer._USAGE_CLS_NAME}.get_data",
        func_path=f"{DataProviderLayer.__module__}.{DataProviderLayer.__qualname__}.get_data",
        kwargs={"url": url, "auto_retry": auto_retry, **kwargs},
        desc={FilterType.SYNC, FilterType.LAYER_DELIVERY},
    )
    response = provider.get_data(session, url, auto_retry=auto_retry, **kwargs)
    return response


async def get_data_async(data_type, provider, session, **kwargs):
    from ._data_provider_factory import get_url, get_api_config

    session = get_valid_session(session)
    config = session.config
    url = get_url(data_type, config)
    api_config = get_api_config(data_type, config)
    auto_retry = api_config.get("auto-retry", False)
    # Library usage logging
    get_usage_logger().log_func(
        name=f"{ModuleName.DELIVERY}.{DataProviderLayer._USAGE_CLS_NAME}.get_data_async",
        func_path=f"{DataProviderLayer.__module__}.{DataProviderLayer.__qualname__}.get_data_async",
        kwargs={"url": url, "auto_retry": auto_retry, **kwargs},
        desc={FilterType.ASYNC, FilterType.LAYER_DELIVERY},
    )
    response = await provider.get_data_async(session, url, auto_retry=auto_retry, **kwargs)
    return response


def get_data_by_data_type(data_type, session, **kwargs):
    from refinitiv.data.delivery._data._data_provider_factory import make_provider

    provider = make_provider(data_type)
    return get_data(data_type, provider, session, **kwargs)


def emit_event(handler, *args, **kwargs):
    session = args[2]
    try:
        handler(*args, **kwargs)
    except Exception as e:
        session.error(f"{handler} callback raised exception: {e!r}")
        session._is_debug() and session.debug(traceback.format_exc())

        if DEBUG:
            raise e


class DataProviderLayer(Generic[TypeData]):
    # Should not change even if class name is changed
    _USAGE_CLS_NAME = "DataProviderLayer"

    def __init__(self, data_type, **kwargs):
        self._initialize(data_type, **kwargs)
        self._log__init__usage(
            data_type=data_type,
            **kwargs,
        )

    @staticmethod
    def _log__init__usage(*args, **kwargs):
        get_usage_logger().log_func(
            name=f"{ModuleName.DELIVERY}.{DataProviderLayer._USAGE_CLS_NAME}.__init__",
            func_path=f"{DataProviderLayer.__module__}.{DataProviderLayer.__qualname__}.__init__",
            args=args,
            kwargs=kwargs,
            desc={FilterType.INIT, FilterType.LAYER_DELIVERY},
        )

    def _initialize(self, data_type, **kwargs):
        from ._data_provider_factory import make_provider

        self._kwargs = kwargs
        self._kwargs["__data_type__"] = data_type
        self._kwargs["__content_type__"] = data_type

        self._data_type = data_type
        self._content_type = data_type
        self._provider = make_provider(data_type)

    def _check_response(self, response: Response, config):
        _check_response(response, config)

    def get_data(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
    ) -> TypeData:
        """
        Sends a request to the client file store to retrieve the previously defined data.

        Parameters
        ----------
        session : Session
            Session object. If it's not passed the default session will be used.
        on_response : Callable
            User-defined callback function to process the retrieved data.

        Returns
        -------
        TypeData instance.

        """
        session = get_valid_session(session)
        response = get_data(self._data_type, self._provider, session, **self._kwargs)
        if on_response is not None:
            warnings.warn(
                "Avoid using on_response for get_data method, it will be removed in future library version v2.0.",
                category=FutureWarning,
            )
        on_response and emit_event(on_response, response, self, session)
        self._check_response(response, session.config)
        return response

    async def get_data_async(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        closure: Optional[Any] = None,
    ) -> TypeData:
        """
        Sends an asynchronous request to the Refinitiv Data Platform to retrieve the previously defined data.

        Parameters
        ----------
        session : Session
            Session object. If it's not passed the default session will be used.
        on_response : Callable
            User-defined callback function to process the retrieved data.
        closure : Any
            Closure parameters that will be returned with the response

        Returns
        -------
        TypeData instance

        """
        if not self._kwargs.get("closure") and closure:
            self._kwargs["closure"] = closure
        session = get_valid_session(session)
        response = await get_data_async(self._data_type, self._provider, session, **self._kwargs)
        on_response and emit_event(on_response, response, self, session)
        return response

    def __repr__(self):
        s = super().__repr__()
        s = s.replace(">", f" {{name='{self._kwargs.get('universe')}'}}>")
        return s
