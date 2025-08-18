from .._enums import Method
from .._models import AmericanMonteCarloParameters, PdeParameters

from .._param_item import enum_param_item, serializable_param_item
from .._serializable import Serializable


class NumericalMethod(Serializable):
    def __init__(
        self,
        american_monte_carlo_parameters: AmericanMonteCarloParameters = None,
        method: Method = None,
        pde_parameters: PdeParameters = None,
    ):
        super().__init__()
        self.american_monte_carlo_parameters = american_monte_carlo_parameters
        self.method = method
        self.pde_parameters = pde_parameters

    def _get_items(self):
        return [
            serializable_param_item.to_kv("americanMonteCarloParameters", self.american_monte_carlo_parameters),
            enum_param_item.to_kv("method", self.method),
            serializable_param_item.to_kv("pdeParameters", self.pde_parameters),
        ]
