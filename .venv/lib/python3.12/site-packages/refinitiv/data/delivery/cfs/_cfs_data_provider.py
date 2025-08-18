import urllib
from typing import TYPE_CHECKING

from refinitiv.data._tools import urljoin
from ._data_types import BucketData, FileData, FileSetData, PackageData
from ._iter_object import IterObj
from ._tools import _get_query_params
from .._data._data_provider import (
    DataProvider,
    RequestFactory,
)
from .._data._response_factory import ResponseFactory

if TYPE_CHECKING:
    from .._data._response import Response
    from ..._core.session import Session


# --------------------------------------------------------------------------------------
#   Request factory
# --------------------------------------------------------------------------------------


class CFSRequestFactory(RequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        return _get_query_params(**kwargs)

    def add_query_parameters(self, url, query_parameters) -> str:
        return "?".join([url, urllib.parse.urlencode(query_parameters, safe=";")])


class CFSPackageRequestFactory(CFSRequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        package_id = kwargs.get("_package_id")
        if package_id is not None:
            return []

        return super().get_query_parameters(**kwargs)

    def get_url(self, *args, **kwargs):
        url = super().get_url(*args, **kwargs)
        url_id = kwargs.get("_package_id")
        if url_id is not None:
            url = urljoin(url, url_id)
        return url


class CFSStreamRequestFactory(RequestFactory):
    def get_url(self, *args, **kwargs):
        return super().get_url(*args, **kwargs) + "/{id}/stream"

    def get_path_parameters(self, session=None, *, path_parameters=None, id=None, **kwargs) -> dict:
        path_parameters = path_parameters or {}
        if id:
            path_parameters["id"] = id
        return path_parameters

    def get_query_parameters(self, *_, **kwargs) -> list:
        query_parameters = kwargs.get("query_parameters") or []
        query_parameters.append(("doNotRedirect", "true"))
        return query_parameters


# --------------------------------------------------------------------------------------
#   Response factory
# --------------------------------------------------------------------------------------


class CFSResponseFactory(ResponseFactory):
    def create_data_success(self, raw: dict, owner_: "Response", session: "Session" = None, **kwargs):
        content_value = raw.get("value") or [raw]
        return self.data_class(
            raw=raw,
            _owner=owner_,
            _iter_object=IterObj(content_value, session, self.data_class),
        )


# --------------------------------------------------------------------------------------
#   Data provider
# --------------------------------------------------------------------------------------


cfs_request_factory = CFSRequestFactory()
cfs_buckets_data_provider = DataProvider(
    request=cfs_request_factory, response=CFSResponseFactory(data_class=BucketData)
)
cfs_file_sets_data_provider = DataProvider(
    request=cfs_request_factory, response=CFSResponseFactory(data_class=FileSetData)
)
cfs_files_data_provider = DataProvider(request=cfs_request_factory, response=CFSResponseFactory(data_class=FileData))
cfs_packages_data_provider = DataProvider(
    request=CFSPackageRequestFactory(),
    response=CFSResponseFactory(data_class=PackageData),
)
cfs_stream_data_provider = DataProvider(request=CFSStreamRequestFactory())

del cfs_request_factory
