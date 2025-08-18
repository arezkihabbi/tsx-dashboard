from enum import unique
from typing import Union

import pandas as pd

from ..._base_enum import StrEnum
from ..._types import OptDateTime
from ...content.news import headlines as _headlines
from ...content.news import story as _story
from ...content.news.headlines._sort_order import SortOrder


@unique
class Format(StrEnum):
    TEXT = "Text"
    HTML = "Html"


def get_story(
    story_id: str,
    format: Union[Format, str] = Format.HTML,
) -> str:
    """
    Retrieves the news story items.

    Parameters
    ----------
    story_id : str
        News Story ID.
    format : str, Format, optional
        Response format.

    Returns
    -------
    str
        Story html or text response

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> response = rd.news.get_story("urn:newsml:reuters.com:20220713:nL1N2YU10J", format=rd.news.Format.TEXT)
    """

    content = _story.Definition(story_id).get_data().data.story.content
    return content.html if format == Format.HTML else content.text


def get_headlines(
    query: str,
    count: int = 10,
    start: "OptDateTime" = None,
    end: "OptDateTime" = None,
    order_by: Union[str, SortOrder] = SortOrder.new_to_old,
) -> pd.DataFrame:
    """
    Retrieves news headlines.

    Parameters
    ----------
    query: str
        The user search query for news headlines.
    count: int, optional
        Count to limit number of headlines.
    start: str or timedelta, optional
        Beginning of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.
    end: str or timedelta, optional
        End of date range.
        String format is: '%Y-%m-%dT%H:%M:%S'. e.g. '2016-01-20T15:04:05'.
    order_by: str or SortOrder
        Sort order for headline items.

    Returns
    -------
    pd.DataFrame
        Headlines dataframe

    Examples
    --------
    >>> from datetime import timedelta
    >>> import refinitiv.data as rd
    >>> response = rd.news.get_headlines(
    ...     "Refinitiv",
    ...     start="20.03.2021",
    ...     end=timedelta(days=-4),
    ...     count=3
    ... )
    """

    definition = _headlines.Definition(query=query, count=count, date_from=start, date_to=end, sort_order=order_by)
    return definition.get_data().data.df
