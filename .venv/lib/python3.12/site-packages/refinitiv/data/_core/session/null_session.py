from typing import TYPE_CHECKING

from ._session_type import SessionType
from ._session import Session
from ._session_cxn_type import SessionCxnType

if TYPE_CHECKING:
    from ... import OpenState


class NullSession(Session):
    type = SessionType.NONE

    def __init__(self):
        Session.__init__(self, app_key="")

    def __eq__(self, other):
        return False

    def _get_session_cxn_type(self) -> SessionCxnType:
        return SessionCxnType.NONE

    def get_omm_login_message(self):
        return {}

    def get_rdp_login_message(self, stream_id):
        return {}

    async def open_async(self) -> "OpenState":
        # do nothing
        pass
