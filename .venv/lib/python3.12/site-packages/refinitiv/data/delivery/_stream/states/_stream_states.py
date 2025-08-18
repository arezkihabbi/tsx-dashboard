from abc import ABC, abstractmethod

from ._basestream_states import (
    OpeningBaseStreamSt,
    CloseBaseStreamSt,
    UnopenedBaseStreamSt,
    OpenBaseStreamSt,
    BaseStreamStates,
)


class StreamStateMixin(ABC):
    @abstractmethod
    def send(self, message: dict) -> bool:
        pass


class UnopenedStreamSt(UnopenedBaseStreamSt, StreamStateMixin):
    def send(self, message: dict) -> bool:
        return False


class OpeningStreamSt(OpeningBaseStreamSt, StreamStateMixin):
    def send(self, message: dict) -> bool:
        return False


class OpenStreamSt(OpenBaseStreamSt, StreamStateMixin):
    def send(self, message: dict) -> bool:
        return self.stream.do_send(message)


class CloseStreamSt(CloseBaseStreamSt, StreamStateMixin):
    def send(self, message: dict) -> bool:
        return False


class StreamStates(BaseStreamStates):
    unopened_st_class = UnopenedStreamSt
    opening_st_class = OpeningStreamSt
    open_st_class = OpenStreamSt
    close_st_class = CloseStreamSt
