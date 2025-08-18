from .._content_type import ContentType
from ..content._universe_stream import _UniverseStream
from ..content._universe_streams import _UniverseStreams
from .._core.session.tools import get_user_id
from ..content.custom_instruments._custom_instruments_data_provider import symbol_with_user_id


class MixedStreams(_UniverseStreams):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, content_type=ContentType.NONE)
        self._uuid = None

    def _get_symbol(self, universe):
        if not symbol_with_user_id.match(universe):
            if not self._uuid:
                self._uuid = get_user_id(self._session)
            symbol = f"{universe}.{self._uuid}"
        else:
            symbol = universe
        return symbol

    def _get_pricing_stream(self, name) -> _UniverseStream:
        return _UniverseStream(
            content_type=ContentType.STREAMING_PRICING,
            name=name,
            session=self._session,
            owner=self,
            fields=self.fields,
            service=self._service,
            extended_params=self._extended_params,
        )

    def _get_custom_instruments_stream(self, name) -> _UniverseStream:
        return _UniverseStream(
            content_type=ContentType.STREAMING_CUSTOM_INSTRUMENTS,
            name=self._get_symbol(name),
            session=self._session,
            owner=self,
            fields=self.fields,
            service=self._service,
            extended_params=self._extended_params,
        )

    def create_stream_by_name(self, name) -> _UniverseStream:
        if name.startswith("S)"):
            stream = self._get_custom_instruments_stream(name)
        else:
            stream = self._get_pricing_stream(name)
        return stream

    def add_instruments(self, *instruments):
        super().add_instruments(*[self._get_symbol(name) if name.startswith("S)") else name for name in instruments])

    def remove_instruments(self, *instruments):
        super().remove_instruments(*[self._get_symbol(name) if name.startswith("S)") else name for name in instruments])
