from typing import TYPE_CHECKING, Optional

from ..._enums import DiscountingType
from ..._param_item import enum_param_item, param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr


class SwaptionSurfaceDefinition(Serializable):
    # new name VolatilityCubeDefinition in version 1.0.130
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
        Underlying index name (e.g. 'euribor').
    index_tenor : str, optional
        Index tenor of the projected zero curve used to calculate swap rates. the
        default value is the index tenor associated with the underlying swap structure
        (for eur_ab6e, 6m).
    underlying_swap_structure : str, optional
        Underlying swap structure, eg: eur_ab6e
    """

    def __init__(
        self,
        *,
        instrument_code: "OptStr" = None,
        discounting_type: Optional[DiscountingType] = None,
        index_name: "OptStr" = None,
        index_tenor: "OptStr" = None,
        underlying_swap_structure: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.instrument_code = instrument_code
        self.index_name = index_name
        self.index_tenor = index_tenor
        self.discounting_type = discounting_type
        self.underlying_swap_structure = underlying_swap_structure

    def _get_items(self):
        return [
            enum_param_item.to_kv("discountingType", self.discounting_type),
            param_item.to_kv("indexName", self.index_name),
            param_item.to_kv("indexTenor", self.index_tenor),
            param_item.to_kv("instrumentCode", self.instrument_code),
            param_item.to_kv("underlyingSwapStructure", self.underlying_swap_structure),
        ]
