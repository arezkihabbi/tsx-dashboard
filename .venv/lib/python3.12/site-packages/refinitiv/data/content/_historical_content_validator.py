import re
from typing import TYPE_CHECKING, List, Callable

from .._tools import cached_property
from ..delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData

user_has_no_permissions_expr = re.compile(r"TS[A-Z]*\.((Interday)|(Intraday)|(QS))\.UserNotPermission\.[0-9]{5}")


class HistoricalContentValidator(ContentValidator):
    @classmethod
    def user_has_permissions(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        if isinstance(content_data, list) and len(content_data):
            status = content_data[0].get("status", {})
            code = status.get("code", "")

            if status and user_has_no_permissions_expr.match(code):
                data.status["error"] = status
                data.error_codes = code
                data.error_messages = status.get("message")
                return False

        return True

    @classmethod
    def content_data_status_is_not_error(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        if isinstance(content_data, list) and len(content_data):
            first_content_data = content_data[0]
            status = first_content_data.get("status", {})
            code = status.get("code", "")

            if "Error" in code:
                data.status["error"] = status
                data.error_codes = code
                data.error_messages = status.get("message")

                if not (first_content_data.keys() - {"universe", "status"}):
                    return False

                if "UserRequestError" in code:
                    return True

                return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [
            self.content_data_is_not_none,
            self.user_has_permissions,
            self.content_data_status_is_not_error,
        ]
