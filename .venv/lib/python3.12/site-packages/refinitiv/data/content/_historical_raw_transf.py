from copy import deepcopy
from dataclasses import dataclass
from typing import List, Dict

import pandas as pd

from .._tools import convert_str_to_timestamp, NotNoneList
from .._types import Strings, TimestampOrNaT


@dataclass
class _TransformedData:
    data: List[List]
    fields: Strings
    dates: List[TimestampOrNaT]


@dataclass
class _ParsedData:
    data: List[List]
    headers_names: Strings
    timestamp_idx: int
    timestamp_name: str


def _parse_raw(raw: dict) -> _ParsedData:
    headers_names = [header["name"] for header in raw["headers"]]

    timestamp_name = None
    if "DATE_TIME" in headers_names:
        timestamp_name = "DATE_TIME"
    elif "DATE" in headers_names:
        timestamp_name = "DATE"

    timestamp_idx = headers_names.index(timestamp_name)
    return _ParsedData(raw["data"], headers_names, timestamp_idx, timestamp_name)


def get_data_sorted_by_fields(lst, headers_names, fields):
    return NotNoneList(*(lst[headers_names.index(field)] if field in headers_names else None for field in fields))


def transform_for_df(raw: dict, fields: Strings = None):
    parsed = _parse_raw(raw)
    timestamp_idx = parsed.timestamp_idx
    headers_names = parsed.headers_names
    headers_names.pop(timestamp_idx)

    parsed_data = list(filter(lambda a: bool(a), deepcopy(parsed.data)))

    dates = [convert_str_to_timestamp(lst.pop(timestamp_idx)) for lst in parsed_data]

    if fields:
        data = [get_data_sorted_by_fields(lst, headers_names, fields) for lst in parsed_data]
    else:
        data = [NotNoneList(*lst) for lst in parsed_data]
        fields = headers_names

    return _TransformedData(data, fields, dates)


def transform_for_df_by_fields(raw: dict, fields: Strings) -> _TransformedData:
    parsed = _parse_raw(raw)
    headers_names = parsed.headers_names
    timestamp_idx = parsed.timestamp_idx
    headers_names.pop(timestamp_idx)

    data = []
    dates = []

    for lst in deepcopy(parsed.data):
        if not lst:
            continue
        dates.append(convert_str_to_timestamp(lst.pop(timestamp_idx)))
        newlst = (lst[headers_names.index(field)] if field in headers_names else None for field in fields)
        newlst = NotNoneList(*newlst)

        data.append(newlst)

    return _TransformedData(data, fields, dates)


def transform_for_df_by_headers_names(raw: dict) -> _TransformedData:
    parsed = _parse_raw(raw)
    headers_names = parsed.headers_names
    timestamp_idx = parsed.timestamp_idx
    headers_names.pop(timestamp_idx)

    data = []
    dates = []

    for lst in deepcopy(parsed.data):
        if not lst:
            continue
        dates.append(convert_str_to_timestamp(lst.pop(timestamp_idx)))

        newlst = NotNoneList(*lst)

        data.append(newlst)

    return _TransformedData(data, headers_names, dates)


def transform_to_dicts(raw: dict, fields: Strings, date_name: str) -> List[Dict]:
    parsed = _parse_raw(raw)
    headers_names = [header_name.casefold() for header_name in parsed.headers_names]
    timestamp_idx = parsed.timestamp_idx
    dicts = []
    fields = [f.casefold() for f in fields]
    for lst in parsed.data:
        newlst = []
        for field in fields:
            if field in headers_names:
                item = lst[headers_names.index(field)]
                newlst.append(pd.NA if item is None else item)

            else:
                newlst.append(pd.NA)

        dicts.append({date_name: lst[timestamp_idx], **dict(item for item in zip(fields, newlst))})

    return dicts
