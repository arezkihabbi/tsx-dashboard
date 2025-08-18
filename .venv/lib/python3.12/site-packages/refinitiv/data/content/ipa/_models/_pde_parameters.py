from .._param_item import param_item
from .._serializable import Serializable


class PdeParameters(Serializable):
    def __init__(
        self,
        pde_space_step_number=None,
        pde_standard_deviation=None,
        pde_time_step_number=None,
    ):
        super().__init__()
        self.pde_space_step_number = pde_space_step_number
        self.pde_standard_deviation = pde_standard_deviation
        self.pde_time_step_number = pde_time_step_number

    def _get_items(self):
        return [
            param_item.to_kv("pdeSpaceStepNumber", self.pde_space_step_number),
            param_item.to_kv("pdeStandardDeviation", self.pde_standard_deviation),
            param_item.to_kv("pdeTimeStepNumber", self.pde_time_step_number),
        ]
