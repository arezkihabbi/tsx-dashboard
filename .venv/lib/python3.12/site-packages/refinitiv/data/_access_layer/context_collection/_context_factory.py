from enum import Enum, auto
from typing import TYPE_CHECKING, Union

from ._adc_context import ADCContext
from ._adc_rdp_context import ADCRDPContext
from ._adc_udf_context import ADCUDFContext
from ._cust_inst_context import CustInstContext
from ._cust_inst_rdp_context import CustInstRDPContext
from ._cust_inst_udf_context import CustInstUDFContext
from ._hp_and_cust_inst_context import HPAndCustInstContext
from ._hp_context import HPContext, HPUDFContext, HPRDPContext
from ...content.fundamental_and_reference._data_grid_type import DataGridType

if TYPE_CHECKING:
    from .._containers import FieldsContainer, UniverseContainer


class ContextType(Enum):
    ADC = auto()
    HP = auto()
    HPAndCustInst = auto()
    CustInst = auto()


data_grid_type_by_context_class_by_context_type = {
    ContextType.ADC: {
        DataGridType.UDF: ADCUDFContext,
        DataGridType.RDP: ADCRDPContext,
    },
    ContextType.HP: {
        DataGridType.UDF: HPUDFContext,
        DataGridType.RDP: HPRDPContext,
    },
    ContextType.CustInst: {
        DataGridType.UDF: CustInstUDFContext,
        DataGridType.RDP: CustInstRDPContext,
    },
    ContextType.HPAndCustInst: {
        DataGridType.UDF: HPAndCustInstContext,
        DataGridType.RDP: HPAndCustInstContext,
    },
}


def get_context(
    context_type: ContextType,
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
    use_field_names_in_headers: bool,
) -> Union[CustInstContext, ADCContext, HPContext, HPAndCustInstContext]:
    data_grid_type_by_context_class = data_grid_type_by_context_class_by_context_type.get(context_type)

    if not data_grid_type_by_context_class:
        raise TypeError(f"Unexpected context_type. Type: {context_type}")

    context_class = data_grid_type_by_context_class.get(data_grid_type)

    if not context_class:
        raise TypeError(f"Unexpected type. Type: {data_grid_type}")

    return context_class(universe, fields, use_field_names_in_headers)


def get_cust_inst_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
    use_field_names_in_headers: bool,
) -> CustInstContext:
    return get_context(ContextType.CustInst, data_grid_type, universe, fields, use_field_names_in_headers)


def get_adc_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
    use_field_names_in_headers: bool,
) -> ADCContext:
    return get_context(ContextType.ADC, data_grid_type, universe, fields, use_field_names_in_headers)


def get_hp_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
    use_field_names_in_headers: bool,
) -> HPContext:
    return get_context(ContextType.HP, data_grid_type, universe, fields, use_field_names_in_headers)


def get_hp_and_custinst_context(
    data_grid_type: "DataGridType",
    universe: "UniverseContainer",
    fields: "FieldsContainer",
    use_field_names_in_headers: bool,
) -> HPAndCustInstContext:
    return get_context(ContextType.HPAndCustInst, data_grid_type, universe, fields, use_field_names_in_headers)
