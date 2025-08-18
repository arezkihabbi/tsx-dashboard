from typing import Optional, TYPE_CHECKING

from ._repo_underlying_pricing_parameters import UnderlyingPricingParameters
from ..._param_item import serializable_param_item, param_item, definition_param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from .._base_financial_contracts_definition import BaseFinancialContractsDefinition


class UnderlyingContract(Serializable):
    """
    API endpoint for Financial Contract analytics,
    that returns calculations relevant to each contract type.

    Parameters
    ----------
    instrument_type : str, optional
        The type of instrument being defined.
    instrument_definition : object, optional
        Definition of the input contract
    pricing_parameters : UnderlyingPricingParameters, optional
        The pricing parameters to apply to this instrument. If pricing parameters are
        not provided at this level parameters defined globally at the request level are
        used. If no pricing parameters are provided globally default values apply.

    Examples
    --------
     >>> import refinitiv.data.content.ipa.financial_contracts as rdf
     >>> rdf.repo.UnderlyingContract(
     ...    instrument_type="Bond",
     ...    instrument_definition=rdf.bond.Definition(instrument_code="US191450264="),
     ...)
    """

    def __init__(
        self,
        instrument_type: Optional[str] = None,
        instrument_definition: Optional["BaseFinancialContractsDefinition"] = None,
        pricing_parameters: Optional[UnderlyingPricingParameters] = None,
    ) -> None:
        super().__init__()
        self.instrument_type = instrument_type
        self.instrument_definition = instrument_definition
        self.pricing_parameters = pricing_parameters

    def _get_items(self):
        return [
            definition_param_item.to_kv("instrumentDefinition", self.instrument_definition),
            serializable_param_item.to_kv("pricingParameters", self.pricing_parameters),
            param_item.to_kv("instrumentType", self.instrument_type),
        ]
