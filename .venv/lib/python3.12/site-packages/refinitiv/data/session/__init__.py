"""Session layer.

Accessing the Refinitiv Data Platform to retrieve content requires your application to authenticate and manage
connection semantics to keep the user session live. Refinitiv Data Libraries provide this managed access through an
interface called a session. The session is the interface to the data platform and is responsible for defining
authentication details, managing connection resources, and implementing the necessary protocol to communicate with
the data platform. Depending on the access point your application uses to connect to the platform, it can choose from
one of the session implementations to initiate the connection. For the creation phase, all session implementations
expose the same API and behave in the same way.
"""

__all__ = (
    "Definition",
    "Session",
    "set_default",
    "get_default",
    "EventCode",
    "desktop",
    "platform",
)

from .._core.session._session_definition import Definition
from .._core.session._session import Session
from .._core.session.event_code import EventCode
from .._core.session._default_session_manager import set_default, get_default
from . import desktop, platform
