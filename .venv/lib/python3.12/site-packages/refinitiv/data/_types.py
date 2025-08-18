from datetime import date, datetime, timedelta
from typing import Optional, Callable, List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd  # noqa
    from pandas._libs import NaTType  # noqa

OptStr = Optional[str]
Strings = List[str]
Dicts = List[dict]
OptStrings = Optional[Strings]
OptDicts = Optional[Dicts]

OptInt = Optional[int]
OptFloat = Optional[float]
OptList = Optional[list]
OptTuple = Optional[tuple]
OptDict = Optional[dict]
OptSet = Optional[set]
OptBool = Optional[bool]
OptCall = Optional[Callable]

ExtendedParams = OptDict
StrStrings = Union[str, Strings]
DictDicts = Union[dict, Dicts]
OptStrStrs = Optional[StrStrings]
DateTime = Union[str, date, datetime, timedelta]
OptDateTime = Optional[DateTime]

TimestampOrNaT = Union["pd.Timestamp", "NaTType"]
