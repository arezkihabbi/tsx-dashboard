from typing import List, Optional, TYPE_CHECKING, Union, Set

from ._data_provider import DataProviderLayer, Response
from ._data_type import DataType
from ..._core.session import get_valid_session
from ..._tools import validate_endpoint_request_url_parameters
from ...usage_collection._filter_types import FilterType
from ...usage_collection._logger import get_usage_logger
from ...usage_collection._utils import ModuleName

if TYPE_CHECKING:
    from ..._core.session._session import Session
    from ._endpoint_data import RequestMethod
    from ._data_provider import Response


class Definition(DataProviderLayer):
    """
    Defines the wrapper around the data delivery mechanism of the Refinitiv Data Platform.

    Parameters
    ----------
    url : str
        API endpoint URL.
    method : RequestMethod, optional
        HTTP request method.
    path_parameters : dict, optional
        Parameters that can be added to the endpoint URL.
    query_parameters : dict, optional
        HTTP request query parameters.
    header_parameters : dict, optional
        HTTP request header parameters.
    body_parameters : dict, optional
        HTTP request body parameters.


    Examples
    --------
    >>> from refinitiv.data.delivery import endpoint_request
    >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
    """

    # Should not change even if class name is changed
    _USAGE_CLS_NAME = "EndpointDefinition"

    def __init__(
        self,
        url: str,
        method: Union["RequestMethod", str, None] = None,
        path_parameters: Optional[dict] = None,
        query_parameters: Optional[dict] = None,
        header_parameters: Optional[dict] = None,
        body_parameters: Union[dict, List[dict], None] = None,
    ):
        self.url = url
        self.method = method
        self.path_parameters = path_parameters
        self.query_parameters = query_parameters
        self.body_parameters = body_parameters
        self.header_parameters = header_parameters
        super().__init__(
            data_type=DataType.ENDPOINT,
            url=self.url,
            method=self.method,
            path_parameters=self.path_parameters,
            query_parameters=self.query_parameters,
            body_parameters=self.body_parameters,
            header_parameters=self.header_parameters,
        )

    def get_data(self, session: Optional["Session"] = None) -> "Response":
        """
        Send a request to the Refinitiv Data Platform API directly.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        Response

        Examples
        --------
        >>> from refinitiv.data.delivery import endpoint_request
        >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
        >>> definition_endpoint.get_data()
        """
        validate_endpoint_request_url_parameters(self.url, self.path_parameters)

        session = get_valid_session(session)
        self._log_usage(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}.get_data",
            {FilterType.SYNC, FilterType.LAYER_DELIVERY, FilterType.REST},
        )
        response = self._provider.get_data(
            session,
            self.url,
            method=self.method,
            path_parameters=self.path_parameters,
            query_parameters=self.query_parameters,
            header_parameters=self.header_parameters,
            body_parameters=self.body_parameters,
        )
        return response

    async def get_data_async(self, session: Optional["Session"] = None) -> "Response":
        """
        Sends an asynchronous request directly to the Refinitiv Data Platform API.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        Response

        Examples
        --------
        >>> import asyncio
        >>> from refinitiv.data.delivery import endpoint_request
        >>> definition_endpoint = endpoint_request.Definition("/data/news/v1/analyze")
        >>> asyncio.run(definition_endpoint.get_data_async())
        """
        validate_endpoint_request_url_parameters(self.url, self.path_parameters)

        session = get_valid_session(session)
        self._log_usage(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}.get_data_async",
            {FilterType.ASYNC, FilterType.LAYER_DELIVERY, FilterType.REST},
        )
        response = await self._provider.get_data_async(
            session,
            self.url,
            method=self.method,
            path_parameters=self.path_parameters,
            query_parameters=self.query_parameters,
            header_parameters=self.header_parameters,
            body_parameters=self.body_parameters,
        )
        return response

    def _log_usage(self, name: str, filter_type: Set[FilterType]):
        get_usage_logger().log_func(
            name=f"{ModuleName.DELIVERY}.{self._USAGE_CLS_NAME}.{name}",
            func_path=f"{self.__class__.__module__}.{self.__class__.__qualname__}.{name}",
            kwargs=dict(
                url=self.url,
                method=self.method,
                path_parameters=self.path_parameters,
                query_parameters=self.query_parameters,
                header_parameters=self.header_parameters,
                body_parameters=self.body_parameters,
            ),
            desc=filter_type,
        )
