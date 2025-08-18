from datetime import datetime
from typing import List

import numpy as np
from pandas import DataFrame, NA, MultiIndex, concat

from .._tools import ohlc


def merge_dataframes(dfs: List[DataFrame]) -> DataFrame:
    df = dfs.pop()
    df = df.join(dfs, how="outer")  # noqa
    df = df.convert_dtypes()
    df.index.name = "Timestamp"

    df.ohlc = ohlc.__get__(df, None)
    return df


def create_df(data: list, timestamps: list, fields: list, stream_name: str) -> DataFrame:
    numpy_array = np.array(data)
    timestamp_array = np.array(timestamps)

    if np.size(numpy_array):
        dataframe = DataFrame(numpy_array, columns=fields, index=timestamp_array)
    else:
        dataframe = DataFrame()

    dataframe.sort_index(inplace=True)
    dataframe.columns = MultiIndex.from_product([[stream_name], dataframe.columns])
    return dataframe


def retrieve_data_for_df(stream_data: List[dict], repeat: bool = False) -> tuple:
    timestamps = []
    data = []
    fields = set()

    fields.update(*(item["Fields"] for item in stream_data))
    fields = list(fields)

    for idx, record in enumerate(stream_data):
        if repeat and idx == 0:
            timestamps.append(datetime.now())
        else:
            timestamps.append(record["Timestamp"])

        rics_data = [record["Fields"].get(field) for field in fields]
        data.append(rics_data)

    return timestamps, data, fields


def replace_values_by_nan(_data):
    for rics_data in _data:
        for idx, value in enumerate(rics_data):
            try:
                if value is not None:
                    float(value)
            except ValueError:
                rics_data[idx] = None


def create_df_based_on_ticks(df):
    first_update = df.index[0]
    last_update = df.index[-1]
    time_delta = last_update - first_update

    if hasattr(time_delta, "days") and time_delta.days != 0:
        days = time_delta.days + 1
        days = str(days) + "D"
        df = df.ohlc(days, origin="end", call_from_recorder=True)
    elif hasattr(time_delta, "hours"):
        hours = time_delta.hour + 1
        hours = str(hours) + "H"
        df = df.ohlc(hours, origin="end", call_from_recorder=True)
    elif hasattr(time_delta, "minutes"):
        minutes = time_delta.minutes + 1
        minutes = str(minutes) + "min"
        df = df.ohlc(minutes, origin="end", call_from_recorder=True)
    else:
        seconds = time_delta.seconds + 1
        seconds = str(seconds) + "s"
        df = df.ohlc(seconds, origin="end", call_from_recorder=True)

    return df


class OHLCBuilder:
    def __init__(self, frequency: str, universe: list, fields: list) -> None:
        self._frequency = frequency
        self.dataframes = []
        self.ohlc_df = None
        self._universe = universe
        self._fields = fields

        self._last_recorded_ohlc_updates = None

    def create_ohlc_df(self, df: DataFrame) -> DataFrame:
        return df.ohlc(self._frequency, origin="end", call_from_recorder=True)

    def save_ohlc_data(self, df: DataFrame):
        df.fillna(NA, inplace=True)

        if self.ohlc_df is None:
            self.ohlc_df = df

        else:
            self.ohlc_df = concat([self.ohlc_df, df])

    def build(self, updates_by_stream_name: dict):
        dfs = []
        df = DataFrame()
        self._count_of_updates = 0

        for universe, stream_data in updates_by_stream_name.items():
            _timestamps, _data, _fields = retrieve_data_for_df(stream_data, True)
            self._count_of_updates += len(_data)
            replace_values_by_nan(_data)
            updates_by_stream_name[universe] = []
            dataframe = create_df(_data, _timestamps, _fields, universe)
            dfs.append(dataframe)

        if dfs:
            df = merge_dataframes(dfs)
            self.dataframes.append(df)

        if not df.empty:
            df = self.create_ohlc_df(df)
            df["ticks count"] = self._count_of_updates

        if df.empty:
            empty_row = {}

            if isinstance(self.ohlc_df, DataFrame) and not self.ohlc_df.empty:
                columns = [col for col in self.ohlc_df]
            else:
                columns = self._create_ohlc_columns()

            for column in columns:
                empty_row[column] = np.nan

            _timestamps = np.array([datetime.now()])
            df = DataFrame(empty_row, index=_timestamps)

        self._last_recorded_ohlc_updates = df
        self.save_ohlc_data(df)

    def _create_ohlc_columns(self):
        columns = []
        ohlc_list = ["open", "high", "low", "close"]

        for universe in self._universe:
            for field in self._fields:
                for item in ohlc_list:
                    columns.append((universe, field, item))

        columns.append(("ticks count", "", ""))
        return columns

    def dispose(self):
        self.dataframes = []
        self.ohlc_df = None


class Ticks_OHLCBuilder(OHLCBuilder):
    def create_ohlc_df(self, df: DataFrame) -> DataFrame:
        return create_df_based_on_ticks(df)
