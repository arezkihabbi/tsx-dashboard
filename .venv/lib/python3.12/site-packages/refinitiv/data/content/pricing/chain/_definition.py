from typing import Optional, TYPE_CHECKING

from ._stream_facade import Stream
from ...._tools import create_repr, validate_types

if TYPE_CHECKING:
    from ...._types import ExtendedParams, OptStr
    from ...._core.session import Session


class Definition(object):
    """
    Creates a definition of information about the specified chains to request and decode them dynamically.

    Parameters
    ----------
    name : str
        Single instrument chain name.
    service : str, optional
        Streaming service name.
    skip_summary_links : bool, optional
        If True - summary links will be skipped.
    skip_empty : bool, optional
        If True - empty data items will be skipped.
    override_summary_links : int, optional
        Number of summary links that can be overridden.
    api : str, optional
        Specifies the data source. It can be updated/added using config file
    extended_params : dict, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.content.pricing import chain
    >>> definition_chain = chain.Definition("0#.FTSE")
    """

    def __init__(
        self,
        name: str,
        service: Optional[str] = None,
        # option for chain constituents
        skip_summary_links: bool = True,
        skip_empty: bool = True,
        override_summary_links: Optional[int] = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ):
        validate_types(override_summary_links, [int, type(None)], "override_summary_links")

        self._name = name
        self._service = service
        self._skip_summary_links = skip_summary_links
        self._skip_empty = skip_empty
        self._override_summary_links = override_summary_links
        self._api = api
        self._extended_params = extended_params

    def __repr__(self):
        return create_repr(self, content=f"{{name='{self._name}'}}")

    def get_stream(self, session: "Session" = None) -> Stream:
        """
        Creates and returns the pricing chain object that allows you to get streaming data for previously defined
        chains.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        chain.Stream

        Examples
        -------
        Create a chain.Stream object

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("0#.FTSE")
        >>> chain_stream = definition_chain.get_stream()

        Open the Stream connection

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("0#.FTSE")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()

        Closes the Stream connection

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("0#.FTSE")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.close()

        Call constituents

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("0#.FTSE")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.constituents

        Call property is_chain

        >>> from refinitiv.data.content.pricing import chain
        >>> definition_chain = chain.Definition("0#.FTSE")
        >>> chain_stream = definition_chain.get_stream()
        >>> chain_stream.open()
        >>> chain_stream.is_chain
        """
        stream = Stream(
            name=self._name,
            session=session,
            service=self._service,
            skip_summary_links=self._skip_summary_links,
            skip_empty=self._skip_empty,
            override_summary_links=self._override_summary_links,
            api=self._api,
            extended_params=self._extended_params,
        )
        return stream
