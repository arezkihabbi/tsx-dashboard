import os
import urllib.parse

from ..._tools import parse_url, urljoin, cfs_datetime_adapter


def _convert_name(name: str) -> str:
    """
    Convert names from snake_case to camel case
    with first letter in lower case

    Parameters
    ----------
    name : str

    Examples
    --------
    >>> _convert_name("fileset_id")
    ... 'filesetId'
    """
    if "_" not in name:
        return name

    return "".join(word if i == 0 else word.title() for i, word in enumerate(name.split("_")))


def _get_query_params(**kwargs):
    _query_parameters = []
    for key, value in kwargs.items():
        if value is not None and not key.startswith("_"):
            _query_parameters.append((_convert_name(key), value))
    return _query_parameters


def _get_url(config, endpoint):
    base_url = config.get_str("url")
    endpoint_url = config.get_str(f"endpoints.{endpoint}")
    _url = urljoin(base_url, endpoint_url)
    return _url


def _get_query_parameter(param, url):
    # url -> "site.com/package?par1=val1&par2=val2
    query = parse_url(url).query
    # query -> "par1=val1&par2=val2
    query_params = dict(urllib.parse.parse_qsl(query))
    # query_params -> {"par1": "val1", "par2": "val2"}
    return query_params.get(param)


def _convert_date_time(value):
    if value is None:
        return None
    return cfs_datetime_adapter.get_str(value)


def path_join(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)


def create_dirs_if_no_exists(folder):
    if not folder:
        return

    if not os.path.exists(folder):
        os.makedirs(folder)


def remove_one_ext(filename_ext_ext):
    filename_ext, *_ = filename_ext_ext.rsplit(".", 1)
    return filename_ext


def remove_ext(filename_ext):
    return remove_one_ext(filename_ext)
