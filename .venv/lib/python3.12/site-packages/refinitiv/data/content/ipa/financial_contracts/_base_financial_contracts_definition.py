from typing import Optional, TYPE_CHECKING

from ._stream_facade import Stream
from .._content_provider_layer import IPAContentProviderLayer
from ...._content_type import ContentType
from ...._tools import merge_dict_to_dict

if TYPE_CHECKING:
    from ...._core.session import Session


class BaseFinancialContractsDefinition(IPAContentProviderLayer):
    def __init__(self, **kwargs) -> None:
        super().__init__(ContentType.CONTRACTS, **kwargs)

    def get_stream(
        self,
        session: Optional["Session"] = None,
    ) -> Stream:
        """
        Returns a streaming quantitative analytic service subscription

        Parameters
        ----------
        session : Session, optional
            Means the default session will be used

        Returns
        -------
        Stream

        Raises
        ------
        AttributeError
            If user didn't set default session.
        """
        definition = self._kwargs.get("definition")
        instrument_type = definition.get_instrument_type()
        definition_dict = definition.get_dict()

        pricing_parameters = self._kwargs.get("pricing_parameters")

        definition = {
            "instrumentType": instrument_type,
            "instrumentDefinition": definition_dict,
        }

        if pricing_parameters:
            definition["pricingParameters"] = pricing_parameters.get_dict()

        extended_params = self._kwargs.get("extended_params")
        if extended_params:
            definition = merge_dict_to_dict(definition, extended_params)

        stream = Stream(
            session=session,
            fields=self._kwargs.get("fields"),
            universe=definition,
        )
        return stream

    def __eq__(self, other):
        return self._kwargs.get("definition") == other

    def __repr__(self):
        repr_str = super().__repr__()
        new_str = f" {{name='{self._kwargs.get('definition')}'}}>"
        repr_str = repr_str.replace(">", new_str)
        return repr_str
