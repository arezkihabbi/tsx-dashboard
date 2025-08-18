from typing import TYPE_CHECKING

from ._pricing_content_provider import PricingData
from ._stream_facade import Stream
from .._content_provider_layer import ContentUsageLoggerMixin
from ..._content_type import ContentType
from ..._core.session import Session
from ..._tools import create_repr, try_copy_to_list, universe_arg_parser, fields_arg_parser
from ...delivery._data._data_provider import DataProviderLayer, Response

if TYPE_CHECKING:
    from ..._types import OptStr, ExtendedParams, StrStrings, OptStrStrs


class Definition(
    ContentUsageLoggerMixin[Response[PricingData]],
    DataProviderLayer[Response[PricingData]],
):
    """
    Creates a definition of information about the specific Pricing data.

    Parameters
    ----------
    universe : str or list of str
        Single instrument or list of instruments.
    fields : str or list of str, optional
        Single field or list of fields to return.
    service : str, optional
        Name of the streaming service publishing the instruments.
    api: str, optional
        Specifies the data source for the further retrieval of data.
    extended_params : dict, optional
        Specifies the parameters that will be merged with the request.

    Examples
    --------
    >>> from refinitiv.data.content import pricing
    >>> definition = pricing.Definition("EUR=")
    >>> response = definition.get_data()

    """

    _USAGE_CLS_NAME = "Pricing.PricingDefinition"

    def __init__(
        self,
        universe: "StrStrings",
        fields: "OptStrStrs" = None,
        service: "OptStr" = None,
        api: "OptStr" = None,
        extended_params: "ExtendedParams" = None,
    ) -> None:
        extended_params = extended_params or {}
        universe = extended_params.pop("universe", universe)
        universe = try_copy_to_list(universe)
        universe = universe_arg_parser.get_list(universe)
        fields = extended_params.pop("fields", fields)
        fields = try_copy_to_list(fields)
        fields = fields_arg_parser.get_unique(fields or [])
        super().__init__(
            data_type=ContentType.PRICING,
            universe=universe,
            fields=fields,
            extended_params=extended_params,
        )
        self._universe = universe
        self._fields = fields
        self._service = service
        self._api = api
        self._extended_params = extended_params

    def __repr__(self) -> str:
        return create_repr(
            self,
            content=f"{{name={self._universe}}}",
        )

    def get_stream(self, session: Session = None) -> Stream:
        """
        Creates and returns the pricing stream that allows you to get streaming data for previously defined instruments.

        Parameters
        ----------
        session : Session, optional
            Session object. If it's not passed the default session will be used.

        Returns
        -------
        pricing.Stream

        Examples
        --------
        >>> from refinitiv.data.content import pricing
        >>> definition = pricing.Definition("IBM")
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        return Stream(
            universe=self._universe,
            session=session,
            fields=self._fields,
            service=self._service,
            api=self._api,
            extended_params=self._extended_params,
        )
