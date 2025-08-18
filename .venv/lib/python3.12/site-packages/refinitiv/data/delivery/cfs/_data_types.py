from dataclasses import dataclass

from pandas import DataFrame

from ._tools import _get_query_parameter
from .._data._endpoint_data import EndpointData


@dataclass
class BaseData(EndpointData):
    _iter_object: "IterObj" = None
    _dataframe: "DataFrame" = None

    def __post_init__(self):
        self.raw["skip_token"] = _get_query_parameter("skipToken", self.raw.get("@nextLink", None))

    @property
    def df(self):
        if self._dataframe is None:
            value = self.raw.get("value") or [self.raw]
            columns = set()
            for i in value:
                columns = columns | i.keys()
            columns = tuple(columns)
            data = [[value[key] if key in value else None for key in columns] for value in value]
            self._dataframe = DataFrame(data, columns=columns)

        return self._dataframe


@dataclass
class BucketData(BaseData):
    @property
    def buckets(self):
        return self._iter_object


@dataclass
class FileSetData(BaseData):
    @property
    def file_sets(self):
        return self._iter_object


class PackageData(BaseData):
    @property
    def packages(self):
        return self._iter_object

    @property
    def df(self):
        if not self.raw.get("value"):
            return DataFrame()
        return super().df


class FileData(BaseData):
    @property
    def files(self):
        return self._iter_object
