from typing import TYPE_CHECKING, Union

from .._content_data import Data
from ..._tools import create_repr
from ...delivery._data._data_provider import DataProviderLayer, Response
from ..._content_type import ContentType

if TYPE_CHECKING:
    from ._views import Views
    from ..._types import ExtendedParams


class Definition(DataProviderLayer[Response[Data]]):
    """
    This class describe parameters to retrieve data for search lookup.

    Parameters
    ----------

    view : str or Views
        picks a subset of the data universe to search against. see Views

    terms : str
        lists the symbols to be solved

    scope : str
        identifies the symbology which 'terms' belong to

    select : str
        specifies which properties to return for each result doc

    extended_params : dict, optional
        Other parameters can be provided if necessary

    Examples
    --------
    >>> from refinitiv.data.content import search
    >>> definition = search.lookup.Definition(
    >>>     view=search.Views.SEARCH_ALL,
    >>>     scope="RIC",
    >>>     terms="A,B,NOSUCHRIC,C,D",
    >>>     select="BusinessEntity,DocumentTitle"
    >>>)
    """

    def __init__(
        self,
        view: Union["Views", str],
        terms: str,
        scope: str,
        select: str,
        extended_params: "ExtendedParams" = None,
    ):
        self._view = view
        self._terms = terms
        self._scope = scope
        self._select = select
        self._extended_params = extended_params

        super().__init__(
            data_type=ContentType.DISCOVERY_LOOKUP,
            view=self._view,
            terms=self._terms,
            scope=self._scope,
            select=self._select,
            extended_params=self._extended_params,
        )

    def __repr__(self):
        return create_repr(
            self,
            middle_path="lookup",
            content=f"{{view='{self._view}', terms='{self._terms}', scope='{self._scope}', select='{self._select}'}}",
        )
