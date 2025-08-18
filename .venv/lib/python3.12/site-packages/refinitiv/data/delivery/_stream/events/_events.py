from enum import Enum
from typing import Generic, TypeVar, Union, Optional, Dict, Callable

from ..event import StreamEvt, StreamStEvt
from ...._listener import OriginatorType, EventListener
from ...._tools import CallbackHandler

T = TypeVar("T")


class Events_CallbackHandler(Generic[T, OriginatorType]):
    """
    Base class for events. This class uses CallbackHandler to store event callbacks.
    """

    _callback_handler_: Optional[CallbackHandler] = None

    def __init__(self, originator: OriginatorType) -> None:
        self.originator: OriginatorType = originator

    @property
    def _callback_handler(self) -> CallbackHandler:
        if self._callback_handler_ is None:
            self._callback_handler_ = CallbackHandler()
        return self._callback_handler_

    def on(self, event: Union[float, str, Enum], callback: Union[EventListener, Callable]) -> T:
        """
        Add event listener.
        """
        if isinstance(callback, EventListener):
            callback = callback.callback
        self._callback_handler.on(event, callback)
        return self

    def off(self, event: Union[float, str, Enum], callback: Union[EventListener, Callable]) -> T:
        """
        Remove event listener.
        """
        if isinstance(callback, EventListener):
            callback = callback.callback
        self._callback_handler.remove_callback(event, callback)
        return self

    def dispatch(self, event: Union[float, str, Enum], *args, **kwargs):
        """
        Dispatch event.
        """
        self._callback_handler.emit(event, self.originator, *args, **kwargs)

    def is_on(self, event: Union[float, str, Enum]) -> bool:
        """
        Check if the event is registered.
        """
        return self._callback_handler.is_on(event)

    def has_callback(self, event: Union[float, str, Enum], callback: Union[EventListener, Callable]) -> bool:
        """
        Check if the event has the callback.
        """
        if isinstance(callback, EventListener):
            callback = callback.callback
        return self._callback_handler.has_callback(event, callback)

    def has_no_callback(self, event: Union[float, str, Enum], callback: Union[EventListener, Callable]) -> bool:
        """
        Check if the event does not have the callback.
        """
        return not self.has_callback(event, callback)


def validate_callback(callback: Callable):
    if not callable(callback):
        raise TypeError("Callback must be a callable object")


class Events_SimpleDict(Generic[OriginatorType]):
    """
    Base class for events. This class uses simple dictionary to store event callbacks.
    """

    _callback_by_evt_: Optional[Dict[Union[StreamEvt, StreamStEvt], Callable]] = None

    def __init__(self, originator: OriginatorType) -> None:
        self.originator: OriginatorType = originator

    @property
    def _callback_by_evt(self) -> Dict[Union[StreamEvt, StreamStEvt], Callable]:
        if self._callback_by_evt_ is None:
            self._callback_by_evt_ = {}
        return self._callback_by_evt_

    def on(self, event: Union[str, StreamEvt, StreamStEvt], callback: Union[Callable, EventListener]):
        """
        Add event callback.
        """
        if isinstance(callback, EventListener):
            callback = callback.callback
        validate_callback(callback)
        self._callback_by_evt[event] = callback
        return self

    def off(self, event: Union[str, StreamEvt, StreamStEvt]):
        """
        Remove event callback.
        """
        self._callback_by_evt.pop(event, None)
        return self

    def dispatch(self, event: Union[str, StreamEvt, StreamStEvt], *args, **kwargs) -> None:
        """
        Dispatch event.
        """
        callback = self._callback_by_evt.get(event)
        callback and callback(*args, **kwargs)

    def off_all_events(self):
        """
        Delete all events.
        """
        self._callback_by_evt.clear()
