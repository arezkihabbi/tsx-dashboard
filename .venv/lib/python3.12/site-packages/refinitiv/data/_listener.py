from typing import TypeVar, Generic, Callable

ContextType = TypeVar("ContextType")
OriginatorType = TypeVar("OriginatorType")


class EventListener(Generic[ContextType]):
    """
    Base class for event listener.
    """

    def __init__(self, context: ContextType, callback: Callable = None) -> None:
        super().__init__()
        self.context = context
        self._callback = callback
        self.classname = self.__class__.__name__

    def callback(self, *args, **kwargs):
        if self._callback is not None:
            self._callback(self.context, *args, **kwargs)
        else:
            raise NotImplementedError("callback method must be implemented.")
