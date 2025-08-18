from typing import TYPE_CHECKING

from ....delivery._data import Request, RequestMethod

if TYPE_CHECKING:
    from ._sts_token_info import STSTokenInfo
    from .._platform_session import PlatformSession


def revoke_token(token_info: "STSTokenInfo", session: "PlatformSession"):
    url = session._token_revoke_url
    headers = {
        "Authorization": f"{token_info.access_token}",
        "Content-type": "application/x-www-form-urlencoded",
    }
    access_token_request = Request(
        url=url,
        method=RequestMethod.POST,
        headers=headers,
        data={
            "token": token_info.access_token,
            "token_type_hint": "access_token",
            "client_id": session.app_key,
        },
    )
    refresh_token_request = Request(
        url=url,
        method=RequestMethod.POST,
        headers=headers,
        data={
            "token": token_info.refresh_token,
            "token_type_hint": "refresh_token",
            "client_id": session.app_key,
        },
    )

    session.http_request(access_token_request)
    is_debug = session._is_debug()
    is_debug and session.debug("Access token was revoked.")
    session.http_request(refresh_token_request)
    is_debug and session.debug("Refresh token was revoked.")
