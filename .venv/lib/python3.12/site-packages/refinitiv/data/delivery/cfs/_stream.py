from .._data._data_provider_layer import DataProviderLayer
from .._data._data_type import DataType


class CFSStream(DataProviderLayer):
    def __init__(self, id):
        super().__init__(data_type=DataType.CFS_STREAM, id=id)
