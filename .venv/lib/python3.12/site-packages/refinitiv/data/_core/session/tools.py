from typing import TYPE_CHECKING

import requests

from ._session_type import SessionType
from ..._open_state import OpenState
from ._default_session_manager import get_valid_session

if TYPE_CHECKING:
    from . import Session

codes = requests.codes

UNAUTHORIZED_CODES = {codes.bad, codes.unauthorized, codes.forbidden}


def is_desktop_session(session: "Session") -> bool:
    return session.type == SessionType.DESKTOP


def is_platform_session(session: "Session") -> bool:
    return session.type == SessionType.PLATFORM


def is_open(session: "Session") -> bool:
    return session.open_state is OpenState.Opened


def is_closed(session: "Session") -> bool:
    return session.open_state is OpenState.Closed


def raise_if_closed(session: "Session"):
    if is_closed(session):
        error_message = "Session is not opened. Can't send any request"
        session.error(error_message)
        raise ValueError(error_message)


class NullResponse:
    text = ""
    status_code = 0

    def json(self):
        return {}


class Sensitive(str):
    def __repr__(self):
        return "********"


def get_user_id(session=None) -> str:
    session = get_valid_session(session)
    return session._user_uuid
