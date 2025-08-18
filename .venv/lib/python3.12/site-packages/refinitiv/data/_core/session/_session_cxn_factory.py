from typing import Union

from ._session import Session
from ._session_cxn_type import SessionCxnType
from .connection import (
    RefinitivDataConnection,
    RefinitivDataAndDeployedConnection,
    DesktopConnection,
    DeployedConnection,
)

cxn_class_by_type = {
    SessionCxnType.DEPLOYED: DeployedConnection,
    SessionCxnType.REFINITIV_DATA: RefinitivDataConnection,
    SessionCxnType.REFINITIV_DATA_AND_DEPLOYED: RefinitivDataAndDeployedConnection,
    SessionCxnType.DESKTOP: DesktopConnection,
}

SessionConnection = Union[
    RefinitivDataConnection,
    RefinitivDataAndDeployedConnection,
    DesktopConnection,
    DeployedConnection,
]

PlatformConnection = Union[RefinitivDataConnection, RefinitivDataAndDeployedConnection, DeployedConnection]


def get_session_cxn(session_cxn_type: SessionCxnType, session: "Session") -> SessionConnection:
    cxn_class = cxn_class_by_type.get(session_cxn_type)

    if not cxn_class:
        raise ValueError(f"Can't find cxn_class by session_cxn_type: {session_cxn_type}")

    cxn = cxn_class(session)
    return cxn
