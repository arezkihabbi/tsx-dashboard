import urllib.parse
from typing import Any, TYPE_CHECKING

from ._endpoint_data import RequestMethod
from ._request import Request
from ..._tools import parse_url, urljoin, bool_or_none_to_str, get_params

if TYPE_CHECKING:
    from ..._core.session import Session


class RequestFactory:
    def get_url(self, session: "Session", url: str, *args, **kwargs) -> str:
        return url

    def create(self, session, url, *args, **kwargs) -> Request:
        method = self.get_request_method(**kwargs)
        path = self.get_url(session, url, *args, **kwargs)
        session.verify_scope(path, method)
        url_root = session._get_rdp_url_root()

        header_parameters = self.get_header_parameters(session, **kwargs)
        path_parameters = self.get_path_parameters(session, **kwargs)
        query_parameters = self.get_query_parameters(*args, **kwargs)
        query_parameters = self.extend_query_parameters(query_parameters, extended_params=kwargs.get("extended_params"))
        closure = kwargs.get("closure")

        url = self.update_url(url_root, path, path_parameters, query_parameters)

        body_parameters = None
        headers = header_parameters
        if method != RequestMethod.GET:
            headers["Content-Type"] = "application/json"
        if method in (RequestMethod.POST, RequestMethod.PUT):
            body_parameters = self.get_body_parameters(session, *args, **kwargs)
            body_parameters = self.extend_body_parameters(body_parameters, **kwargs)

        request = Request(
            url=url,
            method=method,
            headers=headers,
            json=body_parameters,
            path=path,
        )

        if closure is not None:
            request.closure = closure

        return request

    def update_url(self, url_root, url, path_parameters, query_parameters):
        try:
            result = parse_url(url)

            if not all([result.scheme, result.netloc, result.path]):
                if result.query and result.path:
                    url = urljoin(url_root, result.path)
                else:
                    url = urljoin(url_root, url)
            else:
                url = "".join([url_root, result.path])

            if result.query and isinstance(query_parameters, list):
                query_parameters.extend(urllib.parse.parse_qsl(result.query))

        except Exception:
            url = "/".join([url_root + "/" + url])

        if path_parameters:
            for key, value in path_parameters.items():
                value = bool_or_none_to_str(value)
                value = urllib.parse.quote(str(value))
                url = url.replace("{" + key + "}", value)

        if self.is_multiple_query_parameters(query_parameters):
            url = self.add_multiple_query_parameters(url, query_parameters)
        elif query_parameters:
            url = self.add_query_parameters(url, query_parameters)

        return url

    def is_multiple_query_parameters(self, query_parameters: Any) -> bool:
        """Check multiple query parameters.

        Args:
            query_parameters (Any): Query parameters.

        Uses to check query parameters
        if they passes like {"universe": ["IBM.N", "ORCL.N"]}
        in case
        when query string must be constructed like '?universe=BNPP.PA,ORCL.N'
        """
        if isinstance(query_parameters, dict):
            return all(
                [
                    len(query_parameters) == 1,
                    isinstance(next(iter(query_parameters.values())), list),
                ]
            )

        return False

    def get_request_method(self, *, method=None, **kwargs) -> RequestMethod:
        return method or RequestMethod.GET

    @property
    def body_params_config(self):
        return []

    def get_body_parameters(self, *args, body_params_config=None, **kwargs) -> dict:
        body_params_config = body_params_config or self.body_params_config
        return dict(get_params(body_params_config, *args, **kwargs))

    @property
    def query_params_config(self):
        return []

    def get_query_parameters(self, *args, **kwargs) -> list:
        return get_params(self.query_params_config, *args, **kwargs)

    def get_path_parameters(self, session=None, *, path_parameters=None, **kwargs) -> dict:
        return path_parameters or {}

    def add_multiple_query_parameters(self, url: str, query_parameters: dict) -> str:
        """Add multiple query parameters to query string.

        Args:
            url (str): url to construct query string.
            query_parameters (dict): query parameters to construct query string.

        Uses to construct percent-encoded query string
        if query parameters passed like {"universe": ["IBM.N", "ORCL.N"]}
        and
        must be transformed to query string like '?universe=BNPP.PA,ORCL.N',
        not like '?universe=BNPP.PA&universe=ORCL.N'

        Estimates API accepts only '?universe=BNPP.PA,ORCL.N' format to get estimates
        actual KPI measures for multiple universe.
        """
        key, value = query_parameters.popitem()
        return f"{url}?{urllib.parse.urlencode({key: ', '.join(value)})}"

    def add_query_parameters(self, url: str, query_parameters: dict) -> str:
        return f"{url}?{urllib.parse.urlencode(query_parameters)}"

    def extend_query_parameters(self, query_parameters, extended_params=None):
        return query_parameters

    def extend_body_parameters(self, body_parameters, extended_params=None, **kwargs):
        if extended_params:
            body_parameters.update(extended_params)
        return body_parameters

    def get_header_parameters(self, session=None, header_parameters=None, **kwargs):
        headers = header_parameters or {}

        if session and session._app_name:
            headers["x-tr-applicationid"] = session._app_name

        return headers
