import collections
from dataclasses import dataclass, field
from enum import Enum, unique
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ._response import Response

Error = collections.namedtuple("Error", ["code", "message"])


@unique
class RequestMethod(str, Enum):
    """
    Possible values for the request methods:
       GET : GET request method.
       POST : POST request method.
       DELETE : DELETE request method.
       PUT : PUT request method.
    """

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class EndpointData:
    raw: Any
    _owner: "Response" = None
    _kwargs: Dict = field(default_factory=dict)
