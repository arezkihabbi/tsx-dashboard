from typing import Callable, Optional, TYPE_CHECKING

from .._content_provider_layer import ContentUsageLoggerMixin
from ..._core.session import get_valid_session
from ...delivery._data._data_provider import DataProviderLayer

if TYPE_CHECKING:
    from ..._core.session import Session


class NewsDataProviderLayer(ContentUsageLoggerMixin, DataProviderLayer):
    _USAGE_CLS_NAME = "NewsDataProviderLayer"

    def get_data(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
    ):
        session = get_valid_session(session)
        response = super().get_data(session, on_response)
        return response

    async def get_data_async(
        self,
        session: Optional["Session"] = None,
        on_response: Optional[Callable] = None,
        closure: Optional[str] = None,
    ):
        session = get_valid_session(session)
        response = await super().get_data_async(session, on_response, closure)
        return response
