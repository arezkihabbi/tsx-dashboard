from typing import TYPE_CHECKING, Iterable, Callable, List

from ..._tools import cached_property
from ...delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData

NO_ROW_HEADERS_COUNT_MESSAGE = "Unable to resolve all request identifiers."


class DataGridContentValidator(ContentValidator):
    @classmethod
    def status_is_not_error(cls, data: "ParsedData") -> bool:
        status_content = data.status.get("content", "")
        if status_content.startswith("Failed"):
            data.error_codes = -1
            data.error_messages = status_content
            return False

        return True


class DataGridRDPContentValidator(DataGridContentValidator):
    @classmethod
    def content_data_has_no_error(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        error = content_data.get("error")
        if error and not content_data.get("data"):
            data.error_codes = error.get("code", -1)
            data.error_messages = error.get("description")

            if not data.error_messages:
                error_message = error.get("message")
                errors = error.get("errors")

                if isinstance(errors, list):
                    error_message += ":\n"
                    error_message += "\n".join(map(str, errors))

                data.error_messages = error_message

            return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [
            self.status_is_not_error,
            self.content_data_is_not_none,
            self.content_data_has_no_error,
        ]


class DataGridUDFContentValidator(DataGridContentValidator):
    @classmethod
    def get_raw(cls, parsed_data: "ParsedData"):
        return parsed_data.content_data.get("responses", [{}])[0]

    @classmethod
    def content_data_is_valid_type(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        if isinstance(content_data, str):
            data.error_codes = -1
            data.error_messages = content_data
            return False

        return True

    @classmethod
    def content_data_has_valid_response(cls, data: "ParsedData") -> bool:
        responses = data.content_data.get("responses", [])
        first_response = responses[0] if responses else {}
        error = first_response.get("error")
        if error and not first_response.get("data"):
            if isinstance(error, dict):
                data.error_codes = error.get("code", -1)
                data.error_messages = error.get("message", error)

            else:
                data.error_codes = -1
                data.error_messages = error

            return False

        return True

    @classmethod
    def content_data_response_has_valid_data(cls, data: "ParsedData") -> bool:
        response = cls.get_raw(data)

        if response.get("ticket"):
            return True

        row_headers_count = response.get("rowHeadersCount")
        if not row_headers_count:
            data.error_codes = -1
            data.error_messages = NO_ROW_HEADERS_COUNT_MESSAGE
            return False

        error = response.get("error")
        if error and not any(
            any(items[row_headers_count:]) if isinstance(items, Iterable) else False for items in response.get("data")
        ):
            first_error = error[0]
            data.error_codes = first_error.get("code", -1)
            data.error_messages = first_error.get("message", first_error)
            return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [
            self.status_is_not_error,
            self.content_data_is_not_none,
            self.content_data_is_valid_type,
            self.content_data_has_no_error,
            self.content_data_has_valid_response,
            self.content_data_response_has_valid_data,
        ]
