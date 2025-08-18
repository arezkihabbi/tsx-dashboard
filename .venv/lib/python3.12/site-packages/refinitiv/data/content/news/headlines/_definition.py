from typing import Callable, Optional, TYPE_CHECKING, Union

from .._news_data_provider_layer import NewsDataProviderLayer
from ..headlines._sort_order import SortOrder
from ...._content_type import ContentType
from ...._tools import create_repr

if TYPE_CHECKING:
    from ...._core.session import Session
    from ...._types import ExtendedParams, OptDateTime


class Definition(NewsDataProviderLayer):
    """
    This class describes parameters to retrieve data for news headlines.

    Parameters
    ----------
    query: str
        The user search query.

    count: int, optional
        Count to limit number of headlines. Min value is 0. Default: 10

    date_from: str or timedelta, optional
        Beginning of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    date_to: str or timedelta, optional
        End of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.

    sort_order: str or SortOrder
        Sort order for the response. Default: SortOrder.new_to_old

    extended_params: dict, optional
        Additional parameters to provide to the API.

    Examples
    --------
    >>> from datetime import timedelta
    >>> from refinitiv.data.content import news
    >>> definition = news.headlines.Definition(
    ...     "Refinitiv",
    ...     date_from="20.03.2021",
    ...     date_to=timedelta(days=-4),
    ...     count=3
    ... )
    """

    def __init__(
        self,
        query: str,
        count: int = 10,
        date_from: "OptDateTime" = None,
        date_to: "OptDateTime" = None,
        sort_order: Union[str, SortOrder] = SortOrder.new_to_old,
        extended_params: "ExtendedParams" = None,
    ):
        super().__init__(
            data_type=ContentType.NEWS_HEADLINES,
            query=query,
            count=count,
            date_from=date_from,
            date_to=date_to,
            sort_order=sort_order,
            extended_params=extended_params,
        )
        self._query = query

    def get_data(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        on_page_response: Optional[Callable] = None,
    ):
        """
        Returns a response from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data
        on_page_response : Callable, optional
            Callable object to process retrieved data

        Returns
        -------
        NewsHeadlinesResponse

        Raises
        ------
        AttributeError
            If user didn't set default session.

        Examples
        --------
        >>> from datetime import timedelta
        >>> from refinitiv.data.content import news
        >>> definition = news.headlines.Definition(
        ...     query="Refinitiv",
        ...     date_from="20.03.2021",
        ...     date_to=timedelta(days=-4),
        ...     count=3
        ... )
        >>> response = definition.get_data()
        """
        self._kwargs["on_page_response"] = on_page_response
        return super().get_data(session, on_response)

    async def get_data_async(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        on_page_response: Optional[Callable] = None,
        closure: Optional[str] = None,
    ):
        """
        Returns a response asynchronously from the API to the library

        Parameters
        ----------
        session : Session, optional
            The Session defines the source where you want to retrieve your data
        on_response : Callable, optional
            Callable object to process retrieved data
        on_page_response : Callable, optional
            Callable object to process retrieved data
        closure : str, optional
            Specifies the parameter that will be merged with the request

        Returns
        -------
        NewsHeadlinesResponse

        Raises
        ------
        AttributeError
            If user didn't set default session.

        Examples
        --------
        >>> import asyncio
        >>> from datetime import timedelta
        >>> from refinitiv.data.content import news
        >>> definition = news.headlines.Definition(
        ...     query="Refinitiv",
        ...     date_from="20.03.2021",
        ...     date_to=timedelta(days=-4),
        ...     count=3
        ... )
        >>> response = asyncio.run(definition.get_data_async())
        """
        self._kwargs["on_page_response"] = on_page_response
        return await super().get_data_async(session, on_response, closure)

    def __repr__(self):
        return create_repr(
            self,
            content=f"{{query='{self._query}'}}",
        )
