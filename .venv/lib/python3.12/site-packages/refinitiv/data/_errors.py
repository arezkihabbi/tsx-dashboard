from typing import TYPE_CHECKING, List, Set

if TYPE_CHECKING:
    from .delivery._data._data_provider import Response


class RDError(Exception):
    """Base class for exceptions in this refinitiv-data module.

    Parameters
    ----------
    code: int
        error code for this exception
    message: str
        error description for this exception
    """

    response: "Response"

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __str__(self) -> str:
        return f"Error code {self.code} | {self.message}"


class SessionError(RDError):
    pass


class StreamingError(RDError):
    pass


class StreamConnectionError(RDError):
    pass


class PlatformSessionError(SessionError):
    pass


class DesktopSessionError(SessionError):
    pass


class ESGError(RDError):
    pass


class NewsHeadlinesError(RDError):
    pass


class EndpointError(RDError):
    pass


class StreamError(RDError):
    pass


class StreamingPricesError(RDError):
    pass


class ItemWasNotRequested(RDError):
    def __init__(self, item_type, not_requested, requested):
        item_type = f"{item_type}{'s' if len(not_requested) > 1 else ''}"
        super().__init__(-1, f"{item_type} {not_requested} was not requested : {requested}")


class EnvError(RDError):
    pass


class BondPricingError(RDError):
    pass


class FinancialContractsError(RDError):
    pass


class RequiredError(RDError):
    pass


class ConfigurationError(RDError):
    pass


class ScopeError(RDError):
    def __init__(
        self,
        required_scope: List[Set[str]],
        available_scope: Set[str],
        key: str,
        method: str,
    ):
        missing_scopes = [scope - available_scope for scope in required_scope]
        self.required_scope = required_scope
        self.available_scope = available_scope
        self.key = key
        self.method = method
        self.missing_scopes = missing_scopes
        super().__init__(
            -1,
            message=f"Insufficient scope for key={key}, method={method}.\n"
            f"Required scopes: {' OR '.join(map(str, required_scope))}\n"
            f"Available scopes: {available_scope or '{}'}\n"
            f"Missing scopes: {' OR '.join(map(str, missing_scopes))}",
        )
