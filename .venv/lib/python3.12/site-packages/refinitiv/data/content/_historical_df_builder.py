from copy import deepcopy
from itertools import product
from typing import List, Dict

import pandas as pd

from ._historical_raw_transf import (
    transform_for_df_by_fields,
    transform_for_df_by_headers_names,
    _parse_raw,
    get_data_sorted_by_fields,
)
from .._tools import convert_dtypes, NotNoneList, convert_str_to_timestamp
from .._types import Strings


def process_data(data_append, index_append, date, items, num_allcolumns, num_raws, left_num_columns):
    prev_idx = None
    counter = 0

    template = [pd.NA] * num_allcolumns
    for instidx, raw_data, raw_columns in items:
        if (counter != 0 and counter % num_raws == 0) or prev_idx == instidx:
            index_append(date)
            data_append(template)
            template = [pd.NA] * num_allcolumns
            prev_idx = instidx

        if prev_idx is None:
            prev_idx = instidx

        counter += 1

        left_idx = left_num_columns[instidx]
        right_idx = left_idx + len(raw_columns)
        for item, i in zip(raw_data, range(left_idx, right_idx)):
            template[i] = item

    index_append(date)
    data_append(template)


def get_list_of_columns(inst_names, raws_columns, is_multiindex):
    if not is_multiindex:
        listofcolumns = inst_names
    else:
        listofcolumns = []
        for inst_name, raw_column in zip(inst_names, raws_columns):
            listofcolumns.append(list(product(inst_name, raw_column)))
    return listofcolumns


def process_bad_column(bad_raw, fields, last_raw_columns):
    inst_name = bad_raw["universe"]["ric"]

    raw_columns = fields or last_raw_columns or ["Field"]
    return inst_name, raw_columns


def process_valid_column(raw, fields, all_fields, items_by_date, instidx):
    parsed = _parse_raw(raw)
    timestamp_idx = parsed.timestamp_idx
    headers_names = parsed.headers_names
    headers_names.pop(timestamp_idx)

    parsed_data = list(filter(lambda a: bool(a), deepcopy(parsed.data)))
    raw_columns = fields or headers_names
    if not fields:
        all_fields.update(headers_names)

    for lst in parsed_data:
        date = convert_str_to_timestamp(lst.pop(timestamp_idx))

        if fields:
            raw_data = get_data_sorted_by_fields(lst, headers_names, fields)
        else:
            raw_data = NotNoneList(*lst)
        items = items_by_date.setdefault(date, [])
        items.append((instidx, raw_data, raw_columns))

    inst_name = raw["universe"]["ric"]
    return inst_name, raw_columns


class HistoricalBuilder:
    def build_one(self, raw: dict, fields: Strings, axis_name: str, **__) -> pd.DataFrame:
        if not raw["data"]:
            return pd.DataFrame()

        if fields:
            transformed = transform_for_df_by_fields(raw, fields)

        else:
            transformed = transform_for_df_by_headers_names(raw)

        data = transformed.data
        columns = transformed.fields
        index = transformed.dates

        inst_name = raw["universe"]["ric"]
        columns = pd.Index(data=columns, name=inst_name)
        index = pd.Index(data=index, name=axis_name)
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df = convert_dtypes(df)
        df.sort_index(inplace=True)
        return df

    def is_bad_raw(self, raw):
        return isinstance(raw, list)

    def get_bad_raw(self, universe, raw, instidx):
        return raw[0]

    def build(self, raws: List[dict], universe: Strings, fields: Strings, axis_name: str, **__) -> pd.DataFrame:
        items_by_date: Dict[str, list] = {}
        inst_names = []
        raws_columns = []
        num_raws = len(raws)
        all_fields = fields or set()

        last_raw_columns = None
        for instidx, raw in enumerate(raws):
            if self.is_bad_raw(raw):
                bad_raw = self.get_bad_raw(universe, raw, instidx)
                inst_name, raw_columns = process_bad_column(bad_raw, fields, last_raw_columns)

            else:
                inst_name, raw_columns = process_valid_column(raw, fields, all_fields, items_by_date, instidx)
                last_raw_columns = raw_columns

            inst_names.append([inst_name])
            raws_columns.append(raw_columns)

        if not items_by_date:
            return pd.DataFrame()

        is_multiindex = len(all_fields) > 1
        listofcolumns = get_list_of_columns(inst_names, raws_columns, is_multiindex)

        left_num_columns = {
            split_idx: sum([len(subcols) for subcols in listofcolumns[:split_idx]]) for split_idx in range(num_raws)
        }

        allcolumns = [col for subcolumns in listofcolumns for col in subcolumns]

        num_allcolumns = len(allcolumns)
        data = []
        index = []
        data_append = data.append
        index_append = index.append
        for date, items in items_by_date.items():
            num_items = len(items)

            if num_items > 1:
                process_data(
                    data_append,
                    index_append,
                    date,
                    items,
                    num_allcolumns,
                    num_raws,
                    left_num_columns,
                )

            else:
                index_append(date)
                instidx, raw_data, raw_columns = items[0]
                left = [pd.NA] * left_num_columns[instidx]
                right = [pd.NA] * (num_allcolumns - len(raw_columns) - len(left))
                data_append(left + raw_data + right)

        if not is_multiindex:
            columns = pd.Index(data=allcolumns, name=all_fields.pop())

        else:
            columns = pd.MultiIndex.from_tuples(allcolumns)

        index = pd.Index(data=index, name=axis_name)
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df = convert_dtypes(df)
        df.sort_index(inplace=True)
        return df


class HistoricalEventsBuilder(HistoricalBuilder):
    def is_bad_raw(self, raw):
        return super().is_bad_raw(raw) or (isinstance(raw, dict) and not raw.get("headers"))

    def get_bad_raw(self, universe, raw, instidx):
        return {"universe": {"ric": universe[instidx]}}


class CustomInstsBuilder(HistoricalBuilder):
    def is_bad_raw(self, raw):
        return not raw

    def get_bad_raw(self, universe, raw, instidx):
        return {"universe": {"ric": universe[instidx]}}

    def build_one(self, raw: dict, fields: Strings, axis_name: str, **__) -> pd.DataFrame:
        if fields:
            transformed = transform_for_df_by_fields(raw, fields)

        else:
            transformed = transform_for_df_by_headers_names(raw)

        data = transformed.data
        columns = transformed.fields
        index = transformed.dates

        if all(i is pd.NA for j in data for i in j):
            return pd.DataFrame()

        inst_name = raw["universe"]["ric"]
        columns = pd.Index(data=columns, name=inst_name)
        index = pd.Index(data=index, name=axis_name)
        df = pd.DataFrame(data=data, columns=columns, index=index)
        df = convert_dtypes(df)
        df.sort_index(inplace=True)
        return df


historical_builder = HistoricalBuilder()
historical_events_builder = HistoricalEventsBuilder()
custom_insts_builder = CustomInstsBuilder()
