from typing import TYPE_CHECKING

from ._contrib_response import ContribResponse, NullContribResponse
from ._contrib_type import OptContribT
from ._stream_factory import create_offstream_contrib
from ..._core.session import get_valid_session

if TYPE_CHECKING:
    from ..._core.session import Session
    from ..._types import OptStr, OptCall


def contribute(
    name: str,
    fields: dict,
    *,
    service: "OptStr" = None,
    contrib_type: OptContribT = None,
    session: "Session" = None,
    api: "OptStr" = None,
    on_ack: "OptCall" = None,
    on_error: "OptCall" = None,
) -> "ContribResponse":
    """
    Function to send OffStream contribution request.

    Parameters
    ----------
    name: string
        RIC to retrieve instrument stream.

    fields: dict{field:value}
        Specify fields and values to contribute.

    service: string, optional
        Specify the service to contribute on.
        Default: None

    contrib_type: Union[str, ContribType], optional
        Define the contribution type : ["Refresh", "Update"]
        Default: "Update"

    session: Session, optional
        Specify the session used to contribute

    api: string, optional
        specific name of contrib streaming defined in config file.
        i.e. 'streaming.pricing.endpoints.my_server'
        Default: 'streaming.pricing.endpoints.main'

    on_ack : function, optional
        Callback function for on_ack event to check contribution result

    on_error : function, optional
        Callback function for on_error event

    Returns
    ----------
    ContribResponse

    Examples
    --------
    Prerequisite: The contrib_session must be opened

    >>> import refinitiv.data as rd
    >>> def on_ack_callback(ack_msg, stream):
    ...     print("Receive Ack response:", ack_msg)
    >>> def on_error_callback(error_msg, stream):
    ...     print("Receive Error:", error_msg)
    >>> update = {
    ...     "ASK": 1.23,
    ...     "BID": 1.24
    ... }
    >>> response = rd.delivery.omm_stream.contribute(
    ...     name="EUR=",
    ...     fields=update,
    ...     service="SVC_CONTRIB",
    ...     on_ack=on_ack_callback,
    ...     on_error=on_error_callback
    ... )
    """
    session = get_valid_session(session)
    offstream = create_offstream_contrib(
        session=session,
        name=name,
        api=api,
        domain="MarketPrice",
        service=service,
    )
    on_ack and offstream.on_ack(on_ack)
    on_error and offstream.on_error(on_error)
    try:
        offstream.open()
    except ConnectionError:
        response = NullContribResponse()
        on_error and on_error(offstream.get_contrib_error_message(), offstream)
    else:
        response = offstream.contribute(fields, contrib_type)
        offstream.close()
    return response


async def contribute_async(
    name: str,
    fields: dict,
    *,
    service: "OptStr" = None,
    contrib_type: OptContribT = None,
    session: "Session" = None,
    api: "OptStr" = None,
    on_ack: "OptCall" = None,
    on_error: "OptCall" = None,
) -> "ContribResponse":
    """
    Function to send asynchrnous OffStream contribution request.

    Parameters
    ----------
    name: string
        RIC to retrieve instrument stream.

    fields: dict{field:value}
        Specify fields and values to contribute.

    service: string, optional
        Specify the service to contribute on.
        Default: None

    contrib_type: Union[str, ContribType], optional
        Define the contribution type
        Default: "Update"

    session: Session, optional
        Specify the session used to contribute

    api: string, optional
        specific name of contrib streaming defined in config file.
        i.e. 'streaming.pricing.endpoints.my_server'
        Default: 'streaming.pricing.endpoints.main'

    on_ack : function, optional
        Callback function for on_ack event to check contribution result

    on_error : function, optional
        Callback function for on_error event

    Returns
    ----------
    ContribResponse

    Examples
    --------
    Prerequisite: The contrib_session must be opened.

    >>> import asyncio
    >>> import refinitiv.data as rd
    >>> def on_ack_callback(ack_msg, stream):
    ...     print("Receive Ack response:", ack_msg)
    >>> def on_error_callback(error_msg, stream):
    ...     print("Receive Error:", error_msg)
    >>> update = {
    ...     "ASK": 1.23,
    ...     "BID": 1.24
    ... }
    >>> response = asyncio.run(rd.delivery.omm_stream.contribute_async(
    ...     "EUR=",
    ...     fields=update,
    ...     service="SVC_CONTRIB",
    ...     on_ack=on_ack_callback,
    ...     on_error=on_error_callback
    ... ))
    """
    session = get_valid_session(session)
    offstream = create_offstream_contrib(
        session=session,
        name=name,
        api=api,
        domain="MarketPrice",
        service=service,
    )
    on_ack and offstream.on_ack(on_ack)
    on_error and offstream.on_error(on_error)
    try:
        await offstream.open_async()
    except ConnectionError:
        response = NullContribResponse()
        on_error and on_error(offstream.get_contrib_error_message(), offstream)
    else:
        response = await offstream.contribute_async(fields, contrib_type)
        offstream.close()
    return response
