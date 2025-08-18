import abc
from typing import Dict, Optional, List, TYPE_CHECKING, Union

import pandas as pd
from pandas import DataFrame

from ._context import Context
from ..._tools import convert_dtypes

if TYPE_CHECKING:
    from ...content._df_builder import DFBuilder


class CustInstContext(Context, abc.ABC):
    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.cust_inst)

    @property
    def can_build_df(self) -> bool:
        return bool(self._cust_inst_data and not (self._adc_data or self._hp_data))

    @property
    def can_join_hp_multiindex_df(self) -> bool:
        return bool(not self._adc_data and (self._hp_data and self._cust_inst_data and len(self.universe.hp) > 1))

    @property
    def raw(self) -> Optional[Dict]:
        return self._cust_inst_data and self._cust_inst_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._cust_inst_data and self._cust_inst_data.df

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

    def build_df(self) -> DataFrame:
        """
        Builds custom instrument dataframe.

        Returns
        -------
        pd.DataFrame
            Custom instrument dataframe.
        """
        fields = self.fields
        df = self.df
        if fields:
            data = self.prepare_data(self.raw, fields)
            headers = self.prepare_headers(fields.raw)
            use_multiindex = len(fields.raw) > 1 and len(self.universe.cust_inst) > 1
            df = self.dfbuilder.build_date_as_index(
                {"data": data, "headers": headers},
                self.use_field_names_in_headers,
                use_multiindex=use_multiindex,
            )
        return df

    @abc.abstractmethod
    def prepare_data(self, raw, fields) -> list:
        # for override
        pass

    @staticmethod
    @abc.abstractmethod
    def prepare_headers(raw: Union[list, dict]) -> List:
        # for override
        pass

    def join_hp_multiindex_df(self, hp_df: DataFrame):
        """
        Joins historical pricing multiindex dataframe with custom instruments dataframe.

        Parameters
        ----------
        hp_df : pd.DataFrame
            Historical pricing multiindex dataframe.

        Returns
        -------
        pd.DataFrame
            Historical pricing multiindex dataframe, joined with custom instruments
            dataframe.
        """
        fields = self._get_fields_from_raw()
        data = self.prepare_data(self.raw, fields)
        headers = self.prepare_headers(fields)
        cust_df = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers},
            self.use_field_names_in_headers,
            use_multiindex=isinstance(hp_df.columns, pd.MultiIndex),
        )
        joined_df = hp_df.join(cust_df, how="outer")
        df = convert_dtypes(joined_df)
        return df

    def _get_fields_from_raw(self):
        fields = []
        if isinstance(self.raw, list):
            headers = self.raw[0]["headers"]

        else:
            headers = self.raw["headers"]

        for header in headers:
            name = header.get("name")
            if name and name.lower() not in {"date", "instrument"}:
                fields.append(name)

        return fields

    def _get_fields_from_headers(self, headers):
        name = "name" if self.use_field_names_in_headers else "title"
        return [
            header[name]
            for header in self.dfbuilder.get_headers({"headers": headers})
            if header[name].lower() not in {"date", "instrument"}
        ]

    def join_common_df(self, df: DataFrame, headers):
        """
        Creates dataframe with ADC, historical pricing and custom instruments data.

        Join or merge previously created ADC and historical pricing dataframe with
        custom instruments dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            Previously created ADC and historical pricing dataframe.
        headers : List
            Common headers for building dataframe

        Returns
        -------
        pd.Dataframe that includes ADC, hp and custom instruments data.
        """
        if not self.fields:
            fields = self._get_fields_from_raw()

        else:
            fields = self._get_fields_from_headers(headers)

        data = self.prepare_data(self.raw, fields)
        headers = self.prepare_headers(fields)
        cust_df = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers},
            self.use_field_names_in_headers,
            use_multiindex=True,
        )

        if not self._adc_data and self._hp_data:
            df = df.join(cust_df, how="outer")

        else:
            df = pd.merge(df, cust_df, on=["Date"])

        return df
