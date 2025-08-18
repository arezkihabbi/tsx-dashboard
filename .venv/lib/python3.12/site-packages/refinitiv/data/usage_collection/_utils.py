from collections import namedtuple
from dataclasses import dataclass, field
from datetime import timezone, datetime as dt
from enum import Enum
from typing import Dict, Tuple, Set, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ._filter_types import FilterType
    from ._abstract_logger import AbstractUsageLogger


def _get_utc_time() -> float:
    return dt.now(timezone.utc).timestamp()


@dataclass(frozen=True)
class RecordData:
    """
    This class is used to store the data for a single log record.
    """

    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    result: object = field(default=None)


@dataclass(frozen=True)
class LoggerConfig:
    """
    This class is used to store the configuration for a single user logger.
    """

    logger_type: Type["AbstractUsageLogger"]
    args: Tuple = field(default_factory=tuple)
    kwargs: Dict = field(default_factory=dict)
    filters: Set["FilterType"] = field(default_factory=set)


@dataclass(frozen=True)
class LogRecord:
    """
    This class is used to store record, with filter used by logger and name of
    the record.
    """

    name: str
    func_path: str
    data: RecordData
    filter: Set["FilterType"] = field(default_factory=set)
    timestamp: float = field(default_factory=_get_utc_time)


class ModuleName(str, Enum):
    DELIVERY = "Delivery"
    CONTENT = "Content"
    ACCESS = "Access"

    def __str__(self):
        return self.value


StreamUsageKey = namedtuple("StreamUsageKey", ["stream_id", "service", "name"])
