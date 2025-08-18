import abc
from collections import defaultdict
from typing import TYPE_CHECKING, Union, List, Dict

from pandas import DataFrame

from ._intervals_consts import NON_INTRA_DAY_INTERVALS
from .._core.session import get_default
from .._log import is_debug
from .._tools import ohlc, convert_dtypes, convert_str_to_timestamp

if TYPE_CHECKING:
    from .context_collection import ADCContext, CustInstContext, HPContext
    from ..content._df_builder import DFBuilder


class HistoryDFBuilder(abc.ABC):
    @property
    @abc.abstractmethod
    def dfbuilder(self) -> "DFBuilder":
        #  for override
        pass

    @property
    @abc.abstractmethod
    def date_name(self) -> str:
        #  for override
        pass

    def build_df_date_as_index(
        self,
        adc: "ADCContext",
        hp: "HPContext",
        cust_inst: "CustInstContext",
        universe: List[str],
        interval: Union[str, None],
    ) -> DataFrame:
        logger = get_default().logger()
        is_debug(logger) and logger.debug("[HistoryDFBuilder.build_df_date_as_index] Start")
        if adc.can_build_df:
            if not adc.raw["data"]:
                df = DataFrame()
            else:
                dicts_by_ric, headers = adc.get_data_headers()

                data = []
                fields = [f.casefold() for f in adc.fields.insert(0, self.date_name)]
                for inst in universe:
                    for d in dicts_by_ric.get(inst, []):
                        datum = [inst, *(d.get(f) for f in fields)]
                        data.append(datum)

                df = adc.dfbuilder.build_date_as_index(
                    {"data": data, "headers": headers},
                    adc.use_field_names_in_headers,
                    use_multiindex=False,
                    sort_ascending=True,
                )

        elif hp.can_build_df:
            df = hp.df

        elif cust_inst.can_join_hp_multiindex_df:
            df = cust_inst.join_hp_multiindex_df(hp.df)

        elif cust_inst.can_build_df:
            df = cust_inst.build_df()

        else:
            hp_data, fields = hp.get_data_fields()
            adc_data, headers = adc.get_data_headers()
            has_cust_inst_raw = bool(cust_inst.raw)
            df = self.build_common_df(
                adc_data,
                hp_data,
                headers,
                universe,
                fields,
                adc.use_field_names_in_headers,
                use_multiindex=has_cust_inst_raw,
            )

            if has_cust_inst_raw:
                df = cust_inst.join_common_df(df, headers)

            df = convert_dtypes(df)

            if interval is not None and interval not in NON_INTRA_DAY_INTERVALS:
                df.index.names = ["Timestamp"]

        df.ohlc = ohlc.__get__(df, None)
        is_debug(logger) and logger.debug("[HistoryDFBuilder.build_df_date_as_index] End")
        return df

    def build_common_df(
        self,
        adc_data: Dict[str, List[dict]],
        hp_data: Dict[str, List[dict]],
        headers: List[Dict[str, str]],
        universe: List[str],
        fields: List[str],
        use_field_names_in_headers: bool,
        use_multiindex: bool,
    ):
        date_name = self.date_name
        fields.insert(0, date_name)
        fields = [f.casefold() for f in fields]
        dicts_by_timestamp_by_inst = defaultdict(dict)
        date_name = date_name.casefold()
        for inst in universe:
            common_dicts = adc_data.get(inst, []) + hp_data.get(inst, [])
            for common_dict in common_dicts:
                date_str = common_dict[date_name]
                timestamp = None
                if date_str is not None:
                    timestamp = convert_str_to_timestamp(date_str)

                dicts_by_timestamp = dicts_by_timestamp_by_inst[inst]
                dicts = dicts_by_timestamp.setdefault(timestamp, [])
                for d in dicts:
                    common_dict_keys = set(common_dict.keys())
                    d_keys = set(d.keys())
                    keys_to_update = common_dict_keys - d_keys
                    for key in keys_to_update:
                        d[key] = common_dict.pop(key)

                    if keys_to_update:
                        break

                if list(common_dict.keys()) != [date_name]:
                    dicts.append(common_dict)

        data = []
        for inst in universe:
            for dicts in dicts_by_timestamp_by_inst[inst].values():
                for d in dicts:
                    datum = [inst, *(d.get(f) for f in fields)]
                    data.append(datum)

        df = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers}, use_field_names_in_headers, use_multiindex, sort_ascending=True
        )
        return df
