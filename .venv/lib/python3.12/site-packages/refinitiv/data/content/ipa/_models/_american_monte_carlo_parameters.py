from .._enums import AmericanMonteCarloMethod

from .._param_item import enum_param_item, param_item
from .._serializable import Serializable


class AmericanMonteCarloParameters(Serializable):
    def __init__(
        self,
        american_monte_carlo_method: AmericanMonteCarloMethod = None,
        additional_points=None,
        all_the_time_points_per_year=None,
        iteration_number=None,
    ):
        super().__init__()
        self.american_monte_carlo_method = american_monte_carlo_method
        self.additional_points = additional_points
        self.all_the_time_points_per_year = all_the_time_points_per_year
        self.iteration_number = iteration_number

    def _get_items(self):
        return [
            enum_param_item.to_kv("americanMonteCarloMethod", self.american_monte_carlo_method),
            param_item.to_kv("additionalPoints", self.additional_points),
            param_item.to_kv("allTheTimePointsPerYear", self.all_the_time_points_per_year),
            param_item.to_kv("iterationNumber", self.iteration_number),
        ]
