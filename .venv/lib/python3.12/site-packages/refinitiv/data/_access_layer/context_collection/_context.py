import abc
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from ...content._df_builder import dfbuilder_rdp, dfbuilder_udf

if TYPE_CHECKING:
    from .._containers import (
        ADCDataContainer,
        CustInstDataContainer,
        FieldsContainer,
        HPAndCustInstDataContainer,
        HPDataContainer,
        UniverseContainer,
    )


@dataclass
class Context(abc.ABC):
    universe: "UniverseContainer"
    fields: "FieldsContainer"
    use_field_names_in_headers: bool
    _adc_data: Optional["ADCDataContainer"] = None
    _hp_data: Union["HPDataContainer", "HPAndCustInstDataContainer", None] = None
    _cust_inst_data: Optional["CustInstDataContainer"] = None

    def set_data(
        self,
        adc_data: "ADCDataContainer",
        hp_data: Union["HPDataContainer", "HPAndCustInstDataContainer"],
        cust_inst_data: Optional["CustInstDataContainer"] = None,
    ):
        self._adc_data = adc_data
        self._hp_data = hp_data
        self._cust_inst_data = cust_inst_data


class RDPMixin:
    @property
    def dfbuilder(self):
        return dfbuilder_rdp

    @property
    def date_name(self) -> str:
        return "date"


class UDFMixin:
    @property
    def dfbuilder(self):
        return dfbuilder_udf

    @property
    def date_name(self) -> str:
        return "Date"
