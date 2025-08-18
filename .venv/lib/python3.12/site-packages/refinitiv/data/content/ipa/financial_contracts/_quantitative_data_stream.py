from typing import TYPE_CHECKING

from ._events import QuantitativeStreamEvts
from ._listeners import QuantitativeStreamListeners
from ...._content_type import ContentType
from ...._tools import cached_property
from ....delivery._stream import _RDPStream

if TYPE_CHECKING:
    from pandas import DataFrame
    from ...._types import ExtendedParams
    from ...._core.session import Session


class QuantitativeDataStream(_RDPStream):
    data = None
    headers = None

    def __init__(
        self,
        universe: list,
        session: "Session",
        fields: list = None,
        extended_params: "ExtendedParams" = None,
    ):
        _RDPStream.__init__(
            self,
            session=session,
            universe=universe,
            view=fields,
            extended_params=extended_params,
            content_type=ContentType.STREAMING_CONTRACTS,
        )

        if extended_params and "view" in extended_params:
            self.column_names = extended_params["view"]

        else:
            self.column_names = fields or None

    @cached_property
    def events(self) -> QuantitativeStreamEvts:
        return QuantitativeStreamEvts(self)

    @cached_property
    def cxn_listeners(self) -> QuantitativeStreamListeners:
        return QuantitativeStreamListeners(self)

    def get_snapshot(self) -> "DataFrame":
        import pandas as pd

        if self.data is None or self.column_names is None:
            return pd.DataFrame()

        return pd.DataFrame.from_records(self.data, columns=self.column_names)
