from enum import Enum, auto


class DataType(Enum):
    CFS_BUCKETS = auto()
    CFS_FILE_SETS = auto()
    CFS_FILES = auto()
    CFS_PACKAGES = auto()
    CFS_STREAM = auto()
    ENDPOINT = auto()
