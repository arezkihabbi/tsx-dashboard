from typing import TYPE_CHECKING, Optional

from ..._enums import DiscountingType
from ..._param_item import enum_param_item, param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr


class IIrVolModelDefinition(Serializable):
    # new name CapletsStrippingDefinition version 1.0.130
    """
    The definition of the volatility surface.

    Parameters
    ----------
    instrument_code : str, optional
        The currency of the interest rate volatility model.
    discounting_type : DiscountingType, optional
        The discounting type of the interest rate volatility model. the default value is
        selected based on 'instrumentcode'.
    index_name : str, optional
        Underlying index name.
    reference_caplet_tenor : str, optional
        Reference caplet payment or index tenor. ex: 1m, 3m, 6m, 1y.
    """

    def __init__(
        self,
        instrument_code: "OptStr" = None,
        discounting_type: Optional[DiscountingType] = None,
        index_name: "OptStr" = None,
        reference_caplet_tenor: "OptStr" = None,
    ):
        super().__init__()
        self.instrument_code = instrument_code
        self.discounting_type = discounting_type
        self.index_name = index_name
        self.reference_caplet_tenor = reference_caplet_tenor

    def _get_items(self):
        return [
            enum_param_item.to_kv("discountingType", self.discounting_type),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("referenceCapletTenor", self.reference_caplet_tenor),
            param_item.to_kv("indexName", self.index_name),
        ]
