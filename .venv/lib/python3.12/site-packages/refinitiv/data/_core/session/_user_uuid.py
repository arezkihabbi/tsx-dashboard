import re

from ..._content_type import ContentType

_dots_are_not_allowed_pattern = (
    "Validation Error: Dots are not allowed in the symbol field except for the final .UUID suffix."
)
_wrong_uuid_regexp = re.compile(r"(Validation Error: .UUID suffix ).*( not matched with userID)")
_wrong_symbol = "S)Instrument.UUID-0000"


def _has_all_error_user_id(response):
    return all(
        error.message.startswith(_dots_are_not_allowed_pattern) or _wrong_uuid_regexp.match(error.message)
        for error in response.errors
    )


def _check_response(response, config):
    from ...delivery._data._data_provider_layer import _check_response as default_check_response

    return None if _has_all_error_user_id(response) else default_check_response(response, config)


def get_user_uuid(session) -> str:
    from ...delivery._data._data_provider_layer import get_data_by_data_type

    response = get_data_by_data_type(ContentType.CUSTOM_INSTRUMENTS_INSTRUMENTS, session, universe=_wrong_symbol)
    _check_response(response, session.config)
    errors = response.errors
    messages = [error.message for error in errors]
    user_id = ""
    for message in messages:
        if message.startswith(_dots_are_not_allowed_pattern):
            _, user_id = message.split(" - ")[0].split(" ID ")
            break
        if _wrong_uuid_regexp.match(message):
            _, user_id = message.rsplit(" ", 1)
            break
    return user_id
