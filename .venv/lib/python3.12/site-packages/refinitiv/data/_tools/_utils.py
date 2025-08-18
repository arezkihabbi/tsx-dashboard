import inspect
import re
from typing import Tuple, Set, List, Union, Iterable
from urllib.parse import ParseResult, urlparse, ParseResultBytes

pattern_1 = re.compile("(.)([A-Z][a-z]+)")
pattern_2 = re.compile("([a-z0-9])([A-Z])")


def camel_to_snake(s):
    if not s:
        return s

    if "_" in s:
        words = [camel_to_snake(w) for w in s.split("_")]
        s = "_".join(words)

    else:
        s = pattern_1.sub(r"\1_\2", s)
        s = pattern_2.sub(r"\1_\2", s)

    return s.lower()


def parse_url(url: str) -> ParseResult:
    import sys

    py_ver = sys.version_info
    if py_ver.major == 3 and (py_ver.minor <= 11 or (py_ver.minor == 11 and py_ver.micro < 1)):
        result_urlparse = urlparse(url)

        if isinstance(result_urlparse, ParseResultBytes):
            return result_urlparse

        scheme = result_urlparse.scheme
        netloc = result_urlparse.netloc
        path = result_urlparse.path
        query = result_urlparse.query
        fragment = result_urlparse.fragment

        i = path.find(":")
        if not scheme and path and i > 0:
            scheme, path = path[:i].lower(), path[i + 1 :]

        if scheme and (not scheme[0].isascii() or not scheme[0].isalpha()):
            path = f"{scheme}:{path}" if path else scheme
            scheme = ""

        result = ParseResult(
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=result_urlparse.params,
            query=query,
            fragment=fragment,
        )
    else:
        result = urlparse(url)

    return result


def validate_endpoint_request_url_parameters(url, path_parameters):
    if url == "":
        raise ValueError("Requested URL is missing, please provide valid URL")

    if url.endswith("{universe}") and not path_parameters:
        raise ValueError("Path parameter 'universe' is missing, please provide path parameter")


def inspect_parameters_without_self(class_: object):
    cls_init_attributes = dict(inspect.signature(class_.__init__).parameters)
    cls_init_attributes.pop("self", None)
    return cls_init_attributes.keys()


def version_to_tuple(version: str) -> Tuple[int, ...]:
    return tuple(map(int, version.split(".")))


def has_any_substrings(s: str, substrings: Union[List[str], Set[str]]) -> bool:
    return any(substr for substr in substrings if substr in s)


def fill(*, delim=" ", **kwargs) -> str:
    return delim.join(f"{k}={v}" for k, v in kwargs.items() if isinstance(v, int) or v)


def quotes(o: Union[str, Iterable]) -> str:
    return f"'{o}'" if isinstance(o, str) else f"{o}"
