from typing import Optional

from ._tools import _convert_date_time
from .._data._data_provider_layer import DataProviderLayer
from .._data._data_type import DataType
from ..._tools import validate_types


class Definition(DataProviderLayer):
    """
    Describes the indivisible set of files inside a particular bucket with all their attributes.

    Parameters
    __________
        bucket : str
            The name of the bucket to retrieve file sets.
        name : str, optional
            Name of the file set.
        attributes : dict, optional
            List of publisher-defined key-value attributes. Each key-pair value is split by a colon. (e.g.
            attributes=key1:val1,key2:val2).
        package_id : str, optional
            File set package ID.
        status : str, optional
             Filter file-set by status (Ready/Pending).
        available_from : str, optional
            File set availability start date.
        available_to : str, optional
            File set availability end date.
        content_from : str, optional
            Age of the content within the file, start date.
        content_to : str, optional
            Age of the content within the file, end date.
        created_since : str, optional
            File set creation date.
        modified_since : str, optional
            File set modification date.
        skip_token : str, optional
            Skip token is only used if a previous operation returned a partial result. If a previous response
            contains a nextLink element, the value of the nextLink element will include a skip token parameter that
            specifies a starting point to use for subsequent calls.
        page_size : int, optional
            Returned filesets number.

    Methods
    -------
    get_data(session=session)
        Returns a response to the data platform
    get_data_async(session=None)
        Returns a response asynchronously to the data platform

    Examples
    --------
    >>> from refinitiv.data.delivery import cfs
    >>> definition = cfs.file_sets.Definition()
    >>> file_sets = definition.get_data()

    Using get_data_async

    >>> import asyncio
    >>> task = definition.get_data_async()
    >>> response = asyncio.run(task)
    """

    def __init__(
        self,
        bucket: str,
        name: Optional[str] = None,
        attributes: Optional[dict] = None,
        package_id: Optional[str] = None,
        status: Optional[str] = None,
        available_from: Optional[str] = None,
        available_to: Optional[str] = None,
        content_from: Optional[str] = None,
        content_to: Optional[str] = None,
        created_since: Optional[str] = None,
        modified_since: Optional[str] = None,
        skip_token: Optional[str] = None,
        page_size: int = 25,
    ):
        validate_types(page_size, [int], "page_size")
        created_since = _convert_date_time(created_since)
        modified_since = _convert_date_time(modified_since)
        available_from = _convert_date_time(available_from)
        available_to = _convert_date_time(available_to)
        content_from = _convert_date_time(content_from)
        content_to = _convert_date_time(content_to)
        if attributes is not None:
            attributes = ",".join([f"{key}:{value}" for key, value in attributes.items()])
        super().__init__(
            data_type=DataType.CFS_FILE_SETS,
            bucket=bucket,
            name=name,
            attributes=attributes,
            package_id=package_id,
            status=status,
            available_from=available_from,
            available_to=available_to,
            content_from=content_from,
            content_to=content_to,
            created_since=created_since,
            modified_since=modified_since,
            skip_token=skip_token,
            page_size=page_size,
        )
