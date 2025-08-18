from typing import TYPE_CHECKING, Union

from .. import content
from .._types import OptStr
from ..content.search import Views

if TYPE_CHECKING:
    import pandas as pd


def search(
    query: OptStr = None,
    view: Union[Views, str] = Views.SEARCH_ALL,
    filter: OptStr = None,
    order_by: OptStr = None,
    boost: OptStr = None,
    select: OptStr = None,
    top: int = 10,
    skip: int = 0,
    group_by: OptStr = None,
    group_count: int = 3,
    features: OptStr = None,
    scope: OptStr = None,
    terms: OptStr = None,
) -> "pd.DataFrame":
    """
    This class describe parameters to retrieve data for search.

    Parameters
    ----------
    query: str, optional
        Keyword argument for view

    view: Views or str, optional
        The view for searching see at Views enum.
        Default: Views.SEARCH_ALL

    filter: str, optional
        Where query is for unstructured end-user-oriented restriction, filter is for
        structured programmatic restriction.

    order_by: str, optional
        Defines the order in which matching documents should be returned.

    boost: str, optional
        This argument supports exactly the same predicate expression syntax as filter,
        but where filter restricts which documents are matched at all,
        boost just applies a large scoring boost to documents it matches,
        which will almost always guarantee that they appear at the top of the results.

    select: str, optional
        A comma-separated list of the properties of a document to be returned in the response.

    top: int, optional
        the maximum number of documents to retrieve. Must be non-negative.
        default: 10

    skip: int, optional
        The number of documents to skip in the sorted result set before returning the
        next top.

    group_by: str, optional
        If specified, this must name a single Groupable property.
        returned documents are grouped into buckets based on their value for this
        property.

    group_count: str, optional
        When supplied in combination with group_by, sets the maximum number of documents
        to be returned per bucket.
        default: 3

    Examples
    --------
    >>> from refinitiv.data as rd
    >>> df = rd.discovery.search(query="cfo", view=rd.discovery.Views.PEOPLE)
    """
    return (
        content.search.Definition(
            query=query,
            view=view,
            filter=filter,
            order_by=order_by,
            boost=boost,
            select=select,
            top=top,
            skip=skip,
            group_by=group_by,
            group_count=group_count,
            features=features,
            scope=scope,
            terms=terms,
        )
        .get_data()
        .data.df
    )
