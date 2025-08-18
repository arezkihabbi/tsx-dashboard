from dataclasses import dataclass
from typing import Any, Callable, Dict, TYPE_CHECKING

from ..delivery._data._endpoint_data import EndpointData

if TYPE_CHECKING:
    import pandas as pd


@dataclass
class Data(EndpointData):
    _dataframe: "pd.DataFrame" = None
    _dfbuilder: Callable[[Any, Dict[str, Any]], "pd.DataFrame"] = None

    @property
    def df(self):
        if self._dataframe is None:
            self._dataframe = self._dfbuilder(self.raw, **self._kwargs)

        return self._dataframe
