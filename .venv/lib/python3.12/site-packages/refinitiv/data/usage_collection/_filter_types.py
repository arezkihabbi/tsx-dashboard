from enum import Enum, auto


class NoValue(Enum):
    def __repr__(self):
        return "<%s.%s>" % (self.__class__.__name__, self.name)


class FilterType(NoValue):
    STREAM = auto()
    REST = auto()
    SYNC = auto()
    ASYNC = auto()
    LAYER_ACCESS = auto()
    LAYER_CONTENT = auto()
    LAYER_DELIVERY = auto()
    INIT = auto()
