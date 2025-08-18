from typing import TYPE_CHECKING, Optional

from .omm_stream import OMMStream
from ..._tools import create_repr, fields_arg_parser, try_copy_to_list

if TYPE_CHECKING:
    from ..._types import ExtendedParams, OptStrStrs
    from ..._core.session import Session


class Definition:
    """
    This class to subscribe to streaming items of any Domain Model
    (e.g. MarkePrice, MarketByPrice, ...)
    exposed by the underlying of the Refinitiv Data

    Parameters
    ----------
    name : str, optional
        Streaming instrument name.
    api: str, optional
        Streaming data source.
    service : str, optional
        Third-party service URL to manage the streaming data.
    fields : str or list, optional
        Single field or list of fields to return.
    domain : str, optional
        Specific streaming data domain.
    extended_params : dict, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.delivery import omm_stream
    >>> definition = omm_stream.Definition("EUR")
    """

    def __init__(
        self,
        name: str,
        api: Optional[str] = None,
        service: Optional[str] = None,
        fields: "OptStrStrs" = None,
        domain: str = "MarketPrice",
        extended_params: "ExtendedParams" = None,
    ) -> None:
        self._name = name
        self._api = api
        self._domain = domain
        self._service = service
        fields = try_copy_to_list(fields)
        self._fields = fields and fields_arg_parser.get_list(fields)
        self._extended_params = extended_params

    def __repr__(self):
        content = f"{{name='{self._name}'}}"
        return create_repr(self, middle_path="omm_stream", content=content)

    def get_stream(self, session: "Session" = None) -> OMMStream:
        """
        Returns the previously defined data stream from the Refinitiv Data Platform.

        Parameters
        ----------
        session: Session, optional
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        OMMStream instance

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        """
        stream = OMMStream(
            session=session,
            name=self._name,
            api=self._api,
            service=self._service,
            fields=self._fields,
            domain=self._domain,
            extended_params=self._extended_params,
        )
        return stream
