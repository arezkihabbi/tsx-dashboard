from abc import ABC, abstractmethod
from typing import List

from refinitiv.data.usage_collection._utils import LogRecord


class AbstractUsageLogger(ABC):
    """
    Abstract class for usage loggers.
    Should be implemented by the user.
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def log(self, batch: List[LogRecord]) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
