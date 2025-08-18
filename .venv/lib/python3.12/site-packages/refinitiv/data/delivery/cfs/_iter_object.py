from ._data_types import BucketData, FileData, FileSetData, PackageData
from .._data._data_provider_layer import get_data_by_data_type
from .._data._data_type import DataType
from ..._tools import camel_to_snake


class BaseCFSObject:
    def __init__(self, data, provider, session=None):
        self._session = session
        self._data = {camel_to_snake(key): value for key, value in data.items()}
        self._child_objects = None
        self._provider = provider
        for name, value in self._data.items():
            setattr(self, name, value)

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        if self._child_type is None:
            raise TypeError(f"object {self._provider.name, type(self)} is not iterable")

        args = self._params
        kwargs = {args[0]: self._data[args[1]]}
        self._child_objects = get_data_by_data_type(data_type=self._child_type, session=self._session, **kwargs)
        self._n = 0
        return self

    def __next__(self):
        _iter_obj = self._child_objects.data._iter_object
        if not _iter_obj:
            raise StopIteration
        if self._n < len(_iter_obj):
            result = self._child_objects.data._iter_object[self._n]
            self._n += 1
            return result
        raise StopIteration

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

    @property
    def _params(self):
        raise NotImplementedError

    @property
    def _child_type(self):
        raise NotImplementedError


class CFSFile(BaseCFSObject):
    _child_type = None
    _params = None


class CFSBucket(BaseCFSObject):
    _child_type = DataType.CFS_FILE_SETS
    _params = ("bucket", "name")


class CFSFileSet(BaseCFSObject):
    _child_type = DataType.CFS_FILES
    _params = ("fileset_id", "id")


class CFSPackage(BaseCFSObject):
    _child_type = DataType.CFS_FILE_SETS
    _params = ("package_id", "package_id")

    def __init__(self, data, provider, session=None):
        super().__init__(data, provider, session=session)
        self._bucket_names = self._data.get("bucket_names", [])

    def __iter__(self):
        args = self._params
        kwargs = {args[0]: self._data[args[1]]}
        bucket_name = self._bucket_names[0] if self._bucket_names else []
        self._child_objects = get_data_by_data_type(
            data_type=self._child_type,
            session=self._session,
            bucket=bucket_name,
            **kwargs,
        )
        self._n = 0
        return self

    def __next__(self):
        _iter_obj = self._child_objects.data._iter_object
        if not _iter_obj:
            raise StopIteration
        if self._n < len(_iter_obj):
            result = self._child_objects.data._iter_object[self._n]
            self._n += 1
            return result
        while self._bucket_names:
            bucket = self._bucket_names.pop(0)
            args = self._params
            kwargs = {args[0]: self._data[args[1]], "bucket": bucket}
            self._child_objects = get_data_by_data_type(self._child_type, self._session, **kwargs)
            if not self._child_objects.errors and self._child_objects.data.raw["value"]:
                self._n = 0
                result = self._child_objects.data._iter_object[self._n]
                self._n += 1
                return result
        raise StopIteration


class_by_type = {
    BucketData: CFSBucket,
    PackageData: CFSPackage,
    FileSetData: CFSFileSet,
    FileData: CFSFile,
}


class IterObj:
    def __init__(self, value, session=None, provider=None):
        _class = class_by_type.get(provider)
        self._values = [_class(i, provider=provider, session=session) for i in value]

    def __getitem__(self, item):
        return self._values[item]

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self._values):
            result = self._values[self._n]
            self._n += 1
            return result
        raise StopIteration

    def __repr__(self):
        return "\n".join([repr(i) for i in self._values])

    def __len__(self):
        return len(self._values)
