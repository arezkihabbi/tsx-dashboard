from contextlib import AbstractContextManager
from typing import Callable, Iterable, List, Optional, TYPE_CHECKING, Union

import pandas as pd

from ._mixed_streams import MixedStreams
from ._pricing_recorder import PricingRecorder
from .._core.session import get_default, raise_if_closed
from .._listener import EventListener
from .._tools import cached_property, iterator_str_arg_parser
from ..content.pricing import _stream_facade as pricing_stream_facade

if TYPE_CHECKING:
    from .. import OpenState


class MixedStreamsListener(EventListener["PricingStream"]):
    def callback(self, message: dict, name: str, originator: "MixedStreams", *args, **kwargs):
        try:
            df = pd.DataFrame(message, index=[name])
            self._callback(df, name, self.context)
        except Exception as error:
            originator.session.logger().error(error)


def open_pricing_stream(
    universe: Union[str, Iterable[str]],
    fields: Union[str, List[str]] = None,
    service: Optional[str] = None,
    on_data: Optional[Callable] = None,
) -> "PricingStream":
    """
    Creates and opens a pricing stream.

    Parameters
    ----------
    universe : str | List[str]
        Instruments to request.
    fields : str | list, optional
        Fields to request.
    service : str, optional
        Name of the streaming service publishing the instruments.
    on_data : function, optional
        Callback function.

    Returns
    ----------
    PricingStream

    Examples
    -------
    >>> import refinitiv.data as rd
    >>> def callback(updated_data, ric, stream):
    ...    print(updated_data)
    >>> pricing_stream = rd.open_pricing_stream(universe=['EUR='], fields=['BID', 'ASK', 'OPEN_PRC'], on_data=callback)  # noqa
    """
    session = get_default()
    raise_if_closed(session)

    universe = iterator_str_arg_parser.get_list(universe)

    mixed_streams = MixedStreams(
        item_facade_class=pricing_stream_facade.PricingStream,
        session=session,
        universe=universe,
        fields=fields,
        service=service,
    )
    stream = PricingStream(mixed_streams)

    if on_data:
        listener = MixedStreamsListener(stream, on_data)
        mixed_streams.on_update(listener)
        mixed_streams.on_refresh(listener)

    stream.open()
    return stream


class PricingStream(AbstractContextManager):
    def __init__(self, stream: "MixedStreams"):
        self._stream = stream

    @cached_property
    def recorder(self) -> PricingRecorder:
        return PricingRecorder(self._stream)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    def open(self, with_updates: bool = True) -> "OpenState":
        return self._stream.open(with_updates=with_updates)

    def close(self) -> "OpenState":
        return self._stream.close()

    def get_snapshot(
        self, universe: Union[str, List[str], None] = None, fields: Optional[List[str]] = None, convert: bool = True
    ) -> "pd.DataFrame":
        return self._stream.get_snapshot(universe=universe, fields=fields, convert=convert)

    def _get_fields(self, universe: str, fields: Optional[list] = None) -> dict:
        return self._stream._get_fields(universe=universe, fields=fields)

    def add_instruments(self, *args) -> None:
        self._stream.add_instruments(*args)

    def remove_instruments(self, *args) -> None:
        self._stream.remove_instruments(*args)

    def __getitem__(self, item) -> "PricingStream":
        return self._stream.__getitem__(item)

    def __iter__(self):
        return self._stream.__iter__()
