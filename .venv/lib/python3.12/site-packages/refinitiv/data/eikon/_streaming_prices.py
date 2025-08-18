from typing import Union, Iterable, Callable

from ._tools import get_default_session
from .._core.session import Session
from .._content_type import ContentType
from ..content._universe_streams import _UniverseStreams
from ..content.pricing._stream_facade import PricingStream


class StreamingPrices(_UniverseStreams):
    def __init__(
        self,
        universe: Union[str, Iterable[str]],
        session: "Session" = None,
        fields: Union[str, list] = None,
        service: str = None,
        on_refresh: Callable = None,
        on_status: Callable = None,
        on_update: Callable = None,
        on_complete: Callable = None,
        extended_params: dict = None,
    ) -> None:
        if session is None:
            session = get_default_session()
        super().__init__(
            content_type=ContentType.STREAMING_PRICING,
            item_facade_class=PricingStream,
            universe=universe,
            session=session,
            fields=fields,
            service=service,
            extended_params=extended_params,
        )
        on_refresh and self.on_refresh(on_refresh)
        on_status and self.on_status(on_status)
        on_update and self.on_update(on_update)
        on_complete and self.on_complete(on_complete)
