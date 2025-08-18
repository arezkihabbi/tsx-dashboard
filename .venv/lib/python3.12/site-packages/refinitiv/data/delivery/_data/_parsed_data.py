from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    import httpx


class ParsedData:
    def __init__(
        self,
        status: dict,
        raw_response: "httpx.Response",
        content_data: Union[dict, list, str] = None,
        error_codes: Union[str, int, List[int]] = None,
        error_messages: Union[str, List[str]] = None,
    ) -> None:
        self.status = status
        self.raw_response = raw_response
        self.content_data = content_data
        if isinstance(error_codes, (int, str)):
            error_codes = [error_codes]
        self._error_codes = error_codes or []
        if isinstance(error_messages, str):
            error_messages = [error_messages]
        self._error_messages = error_messages or []

    @property
    def error_codes(self) -> List[int]:
        return self._error_codes

    @error_codes.setter
    def error_codes(self, value: int):
        if not isinstance(value, list):
            value = [value]
        self._error_codes = value

    @property
    def first_error_code(self) -> int:
        if len(self._error_codes) > 0:
            return self._error_codes[0]
        return 0

    @property
    def error_messages(self) -> List[str]:
        return self._error_messages

    @error_messages.setter
    def error_messages(self, value: str):
        if not isinstance(value, list):
            value = [value]
        self._error_messages = value

    @property
    def first_error_message(self) -> str:
        if len(self._error_messages) > 0:
            return self._error_messages[0]
        return ""

    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "raw_response": self.raw_response,
            "content_data": self.content_data,
            "error_codes": self.error_codes,
            "error_messages": self.error_messages,
        }

    def __eq__(self, o: object) -> bool:
        if isinstance(o, dict):
            return self.as_dict() == o
        return super().__eq__(o)

    def __repr__(self) -> str:
        return str(self.as_dict())
