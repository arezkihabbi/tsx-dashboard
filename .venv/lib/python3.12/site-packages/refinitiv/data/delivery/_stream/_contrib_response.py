import abc
from typing import Union


class ContribResponse(abc.ABC):
    def __init__(self, message: dict):
        self._message = message

    @property
    @abc.abstractmethod
    def is_success(self) -> bool:
        pass

    @property
    def type(self) -> str:
        return self._message.get("Type", "")

    @property
    def ack_id(self) -> Union[int, None]:
        return self._message.get("AckID")

    @property
    def nak_code(self) -> str:
        return self._message.get("NakCode", "")

    @property
    @abc.abstractmethod
    def nak_message(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def error(self) -> str:
        pass

    @property
    def debug(self) -> dict:
        return self._message.get("Debug", {})

    def __str__(self) -> str:
        return str(self._message)


class RejectedContribResponse(ContribResponse):
    @property
    def is_success(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return "Error"

    @property
    def error(self) -> str:
        return self._message.get("Text")

    @property
    def nak_message(self) -> str:
        return ""

    @property
    def debug(self) -> dict:
        return {}


class AckContribResponse(ContribResponse):
    def __repr__(self) -> str:
        d = {"Type": self.type, "AckId": self.ack_id}

        if self.nak_code:
            d["NakCode"] = self.nak_code
            d["Message"] = self.nak_message

        return str(d)

    @property
    def is_success(self) -> bool:
        return not self.nak_code

    @property
    def nak_message(self) -> str:
        return self._message.get("Text", "")

    @property
    def error(self) -> str:
        return ""


class ErrorContribResponse(ContribResponse):
    def __repr__(self) -> str:
        d = {
            "Type": self.type,
            "Text": self.nak_message,
            "Debug": self.debug,
        }
        return str(d)

    @property
    def is_success(self) -> bool:
        return False

    @property
    def nak_message(self) -> str:
        return ""

    @property
    def error(self) -> str:
        return self._message.get("Text", "")


class NullContribResponse(ContribResponse):
    def __init__(self):
        super().__init__(None)

    @property
    def is_success(self) -> bool:
        return False

    @property
    def type(self) -> str:
        return ""

    @property
    def ack_id(self) -> Union[int, None]:
        return None

    @property
    def nak_code(self) -> str:
        return ""

    @property
    def nak_message(self) -> str:
        return ""

    @property
    def error(self) -> str:
        return ""

    @property
    def debug(self) -> dict:
        return {}
