from typing import Optional, TYPE_CHECKING

from ._base_financial_contracts_definition import BaseFinancialContractsDefinition

if TYPE_CHECKING:
    from ._stream_facade import Stream
    from ...._core.session import Session


class BaseOptionDefinition(BaseFinancialContractsDefinition):
    def get_stream(self, session: Optional["Session"] = None) -> "Stream":
        fields = self._kwargs.get("fields")
        if fields is None:
            response = self.get_data(session=session)
            if isinstance(response.data.raw, dict) and "headers" in response.data.raw:
                fields = [item.get("name", "") for item in response.data.raw["headers"]]
                self._kwargs["fields"] = fields

        return super().get_stream(session=session)
