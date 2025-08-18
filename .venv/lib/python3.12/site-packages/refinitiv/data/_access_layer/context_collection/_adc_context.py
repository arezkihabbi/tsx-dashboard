import abc
from collections import defaultdict
from typing import Optional, Dict, List, TYPE_CHECKING, Tuple

import pandas as pd

from ._context import Context
from ..._tools import convert_dtypes

if TYPE_CHECKING:
    from ...content._df_builder import DFBuilder


class ADCContext(Context, abc.ABC):
    @property
    def can_build_df(self) -> bool:
        return bool(self._adc_data and not (self._hp_data or self._cust_inst_data))

    @property
    def can_get_data(self) -> bool:
        if not self.fields.adc:
            return False

        return bool(self.universe.adc) and not (
            self.universe.is_universe_expander and self.fields.hp and self.fields.is_disjoint_adc
        )

    @property
    def raw(self) -> Optional[Dict]:
        return self._adc_data and self._adc_data.raw

    @property
    def df(self) -> Optional[pd.DataFrame]:
        if isinstance(self._adc_data.df, pd.DataFrame) and not self._adc_data.df.empty:
            return convert_dtypes(self._adc_data.df)
        return self._adc_data.df

    @property
    @abc.abstractmethod
    def dfbuilder(self) -> "DFBuilder":
        # for override
        pass

    @property
    @abc.abstractmethod
    def date_name(self) -> str:
        #  for override
        pass

    @property
    @abc.abstractmethod
    def headers_names(self) -> List[str]:
        #  for override
        pass

    @abc.abstractmethod
    def get_fields(self, headers, user_fields) -> List[str]:
        # for override
        pass

    def get_data_headers(self) -> Tuple[Dict[str, List], List[Dict]]:
        dicts_by_ric = defaultdict(list)
        fields = self.get_fields(self.dfbuilder.get_headers(self.raw), self.fields.adc)
        fields = [f.casefold() for f in fields]
        for ric, *items in self.raw["data"]:
            dicts = dicts_by_ric[ric]
            d = dict(zip(fields, items))
            if len(dicts) == 0 or not any(filter(lambda i: i == d, dicts)):
                dicts.append(d)

        return dicts_by_ric, self.prepare_headers(self.raw, list(self.fields))

    @staticmethod
    @abc.abstractmethod
    def prepare_headers(raw: dict, fields: list) -> List[Dict]:
        # for override
        pass

    def get_data_wid_universe_as_index(self) -> Dict[str, list]:
        idx_to_adc_header_name_wid_date = self.dfbuilder.get_idx_to_header_name_wid_date_dict(
            self.dfbuilder.get_headers(self.raw), self.use_field_names_in_headers
        )
        data = defaultdict(list)

        for datas in self.raw.get("data", []):
            first_datum = datas[0]

            result = []
            for idx, datum in enumerate(datas):
                if datum is None:
                    datum = pd.NA

                elif idx_to_adc_header_name_wid_date.get(idx):
                    datum = pd.to_datetime(datum, utc=True, errors="coerce").tz_localize(None)

                result.append(datum)

            data[first_datum].append(result)

        return data
