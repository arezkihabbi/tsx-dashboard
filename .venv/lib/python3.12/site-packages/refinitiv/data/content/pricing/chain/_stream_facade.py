import copy
from typing import Any, Callable, List, TYPE_CHECKING

from ._stream import StreamingChain
from ...._core.session import get_valid_session
from ...._tools import cached_property, create_repr
from ....delivery._stream import StreamOpenWithUpdatesMixin

if TYPE_CHECKING:
    from ...._types import ExtendedParams, OptInt, OptStr
    from ...._core.session import Session


class Stream(StreamOpenWithUpdatesMixin):
    """
    Stream is designed to request streaming chains and decode it dynamically.
    This class also act like a cache for each part of the chain record.

    Parameters
    ----------
    name : str
        Single instrument name
    session : Session, optional
        The Session defines the source where you want to retrieve your data
    service : str, optional
        Name service
    skip_summary_links : bool, optional
        Store skip summary links
    skip_empty : bool, optional
        Store skip empty
    override_summary_links : int, optional
        Store the override number of summary links
    api: str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        If necessary other parameters

    Methods
    -------
    open(**kwargs)
        Open the Stream connection

    close()
        Closes the Stream connection, releases resources

    is_chain
        True - stream was decoded as a chain
        False - stream wasn't identified as a chain

    Attributes
    __________
    constituents: list
        A list of constituents in the chain record or empty list

    """

    def __init__(
        self,
        name: str,
        session: "Session" = None,
        service: "OptStr" = None,
        skip_summary_links: bool = True,
        skip_empty: bool = True,
        override_summary_links: "OptInt" = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        self._session = get_valid_session(session)
        self._always_use_default_session = session is None
        self._name = name
        self._service = service
        self._skip_summary_links = skip_summary_links
        self._skip_empty = skip_empty
        self._override_summary_links = override_summary_links
        self._api = api
        self._extended_params = extended_params

    @cached_property
    def _stream(self) -> StreamingChain:
        return StreamingChain(
            name=self._name,
            session=self._session,
            service=self._service,
            skip_summary_links=self._skip_summary_links,
            skip_empty=self._skip_empty,
            override_summary_links=self._override_summary_links,
            api=self._api,
            extended_params=self._extended_params,
            owner=self,
        )

    @property
    def name(self) -> str:
        return self._stream.name

    @property
    def is_chain(self) -> bool:
        return self._stream.is_chain

    @property
    def num_summary_links(self) -> int:
        return self._stream.num_summary_links

    @property
    def summary_links(self) -> List[str]:
        return self._stream.summary_links

    @property
    def display_name(self) -> str:
        return self._stream.display_name

    @property
    def constituents(self) -> List[str]:
        return copy.deepcopy(self._stream.get_constituents())

    def on_add(self, func: Callable[[int, str, "Stream"], Any]) -> "Stream":
        self._stream.on_add(func)
        return self

    def on_remove(self, func: Callable[[str, int, "Stream"], Any]) -> "Stream":
        self._stream.on_remove(func)
        return self

    def on_update(self, func: Callable[[str, str, int, "Stream"], Any]) -> "Stream":
        self._stream.on_update(func)
        return self

    def on_complete(self, func: Callable[[list, "Stream"], Any]) -> "Stream":
        self._stream.on_complete(func)
        return self

    def on_error(self, func: Callable[[tuple, str, "Stream"], Any]) -> "Stream":
        self._stream.on_error(func)
        return self

    def __repr__(self):
        return create_repr(self, content=f"{{name='{self._name}'}}", class_name=self.__class__.__name__)
