from typing import Optional, Dict, TYPE_CHECKING

from ._context import Context

if TYPE_CHECKING:
    from pandas import DataFrame


class HPAndCustInstContext(Context):
    @property
    def raw(self) -> Optional[Dict]:
        return self._hp_data and self._hp_data.raw

    @property
    def df(self) -> Optional["DataFrame"]:
        return self._hp_data and self._hp_data.df

    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.hp and (not self.fields or self.fields.hp)) or self.universe.cust_inst

    @property
    def can_build_df(self) -> bool:
        return bool(self._hp_data and not (self._adc_data or self._cust_inst_data))

    @property
    def columns(self) -> list:
        return self._hp_data.columns
