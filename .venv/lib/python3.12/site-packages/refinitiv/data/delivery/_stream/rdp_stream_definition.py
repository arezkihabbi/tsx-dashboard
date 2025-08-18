from typing import TYPE_CHECKING, Any

from .rdp_stream import RDPStream
from ..._tools import try_copy_to_list

if TYPE_CHECKING:
    from ..._types import ExtendedParams, StrStrings
    from ..._core.session import Session


class Definition:
    """
    Defines the data to retrieve using RDP the data stream from the Refinitiv Data Platform.

    Parameters
    ----------
    service: string, optional
        RDP service name.
    universe: list
        Single instrument or list of instruments.
    view: list
        Data fields that should be retrieved from the data stream.
    parameters: dict
        Extra parameters to retrieve from the item stream.
    api: string
        RDP streaming data source.
    extended_params: dict, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.delivery import rdp_stream
    >>> definition = rdp_stream.Definition(
    ...     service=None,
    ...     universe=[],
    ...     view=None,
    ...     parameters={"universeType": "RIC"},
    ...     api="streaming.trading-analytics.endpoints.redi",
    ...)
    """

    def __init__(
        self,
        service: str,
        universe: Any,
        view: "StrStrings",
        parameters: dict,
        api: str,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        self._service = service
        if not isinstance(universe, dict):
            universe = try_copy_to_list(universe)
        self._universe = universe
        self._view = try_copy_to_list(view)
        self._parameters = parameters
        self._api = api
        self._extended_params = extended_params

    def get_stream(self, session: "Session" = None) -> RDPStream:
        """
        Returns the previously defined RDP data stream from the Refinitiv Data Platform.

        Parameters
        ----------
        session : Session
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        RDPStream instance.

        """
        stream = RDPStream(
            session=session,
            service=self._service,
            universe=self._universe,
            view=self._view,
            parameters=self._parameters,
            api=self._api,
            extended_params=self._extended_params,
        )
        return stream
