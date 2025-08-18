import itertools
from dataclasses import dataclass, field
from typing import Optional

from ._endpoint_data import RequestMethod

_id_iterator = itertools.count()


@dataclass
class Request:
    """Request data class

    Attributes:
        url (str): URL used for request
        method (str): HTTP method
        headers (dict): HTTP headers
        data (dict): Optional request body parameters
        params (dict): Optional request query parameters
        json (dict): Optional json request body parameters
        closure (str): Optional closure that will be passed to the headers and returned
            in the response
        auto_retry (bool): Optional flag to enable auto retry for the request
        timeout (int): Optional timeout for the request, if not set, the default
            session timeout will be used
        id (int): Unique request id, incremented for each request
        path (str): Base path (e.g. /path/to/endpoint/{param}/) used for forming the
            request

    """

    url: str
    method: str = RequestMethod.GET
    headers: dict = field(default_factory=dict)
    data: Optional[dict] = None
    params: Optional[dict] = None
    json: Optional[dict] = None
    closure: Optional[str] = None
    auto_retry: bool = False
    timeout: Optional[int] = None
    id: int = field(init=False, default_factory=lambda: next(_id_iterator))
    path: Optional[str] = None
