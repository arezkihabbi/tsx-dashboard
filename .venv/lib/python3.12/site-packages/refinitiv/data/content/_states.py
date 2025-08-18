from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from ..delivery._stream.states import (
    UnopenedBaseStreamSt,
    OpeningBaseStreamSt,
    OpenBaseStreamSt,
    CloseBaseStreamSt,
    BaseStreamStates,
    BaseStreamState,
)

if TYPE_CHECKING:
    from ._universe_streams import _UniverseStreams  # noqa: F401
    from .._types import OptDict
    from ..delivery._stream import OptContribT
    from ..delivery.omm_stream import ContribResponse


class UniverseStreamsStMixin(BaseStreamState, ABC):
    @abstractmethod
    def contribute(
        self, name: str, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        pass

    @abstractmethod
    def add_fields(self, fields) -> None:
        pass

    @abstractmethod
    def remove_fields(self, fields) -> None:
        pass

    @abstractmethod
    def add_instruments(self, instruments) -> None:
        pass

    @abstractmethod
    def remove_instruments(self, instruments) -> None:
        pass


class UnopenedUniverseStreamsSt(UnopenedBaseStreamSt["_UniverseStreams"], UniverseStreamsStMixin):
    def contribute(
        self, name: str, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to an unopened stream")

    def add_fields(self, fields) -> None:
        self.stream.do_add_fields(fields)

    def remove_fields(self, fields) -> None:
        self.stream.do_remove_fields(fields)

    def add_instruments(self, instruments) -> None:
        self.stream.do_add_instruments(instruments)

    def remove_instruments(self, instruments) -> None:
        self.stream.do_remove_instruments(instruments)


class OpeningUniverseStreamsSt(OpeningBaseStreamSt, UniverseStreamsStMixin):
    def contribute(
        self, name: str, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to an opening stream")

    def add_fields(self, fields) -> None:
        return

    def remove_fields(self, fields) -> None:
        return

    def add_instruments(self, instruments) -> None:
        return

    def remove_instruments(self, instruments) -> None:
        return


class OpenUniverseStreamsSt(OpenBaseStreamSt, UniverseStreamsStMixin):
    def contribute(
        self, name: str, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        return self.stream.do_contribute(name, fields, contrib_type, post_user_info)

    def add_fields(self, fields) -> None:
        self.stream.do_add_fields(fields)

    def remove_fields(self, fields) -> None:
        self.stream.do_remove_fields(fields)

    def add_instruments(self, instruments) -> None:
        self.stream.do_add_instruments(instruments)

    def remove_instruments(self, instruments) -> None:
        self.stream.do_remove_instruments(instruments)


class CloseUniverseStreamsSt(CloseBaseStreamSt, UniverseStreamsStMixin):
    def contribute(
        self, name: str, fields: dict, contrib_type: "OptContribT" = None, post_user_info: "OptDict" = None
    ) -> "ContribResponse":
        raise ValueError("Cannot contribute to closed stream")

    def add_fields(self, fields) -> None:
        self.stream.do_add_fields(fields)

    def remove_fields(self, fields) -> None:
        self.stream.do_remove_fields(fields)

    def add_instruments(self, instruments) -> None:
        self.stream.do_add_instruments(instruments)

    def remove_instruments(self, instruments) -> None:
        self.stream.do_remove_instruments(instruments)


class UniverseStreamsStates(BaseStreamStates):
    unopened_st_class = UnopenedUniverseStreamsSt
    opening_st_class = OpeningUniverseStreamsSt
    open_st_class = OpenUniverseStreamsSt
    close_st_class = CloseUniverseStreamsSt
