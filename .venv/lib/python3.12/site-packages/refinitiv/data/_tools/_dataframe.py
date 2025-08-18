import re
from typing import List, Union, TYPE_CHECKING

from ._lazy_loader import load as lazy_load
from .._types import TimestampOrNaT

np = lazy_load("numpy")
pd = lazy_load("pandas")

if TYPE_CHECKING:
    from pandas.core.series import Series
    from pandas.core.dtypes.base import ExtensionDtype  # noqa

DtypeObj = Union["np.dtype", "ExtensionDtype"]


def set_df_column_value(df: "pd.DataFrame", loc: int, value) -> "pd.DataFrame":
    """
    Set the given value in the column with position 'loc'.

    Library pandas changed `iloc` property and recommends using `isetitem`
    from 1.5.0 version.

    More details:
    https://pandas.pydata.org/docs/whatsnew/v1.5.0.html

    Link for isetitem method:
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isetitem.html

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe to convert.
    loc : int
        Index for current column, when we need update value.
    value : scalar or arraylike
        New value for column.

    Returns
    -------
    pd.DataFrame
        Modified dataframe
    """
    if hasattr(df, "isetitem"):
        df.isetitem(loc, value)
    else:
        df.iloc[:, loc] = value

    return df


def convert_df_columns_to_datetime(
    df: "pd.DataFrame", entry: str, utc: bool = None, delete_tz: bool = False
) -> "pd.DataFrame":
    """Converts particular dataframe columns to datetime according the pattern.

    Converts particular dataframe column or columns if one of more columns
    matches the pattern, returns same dataframe otherwise.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe to convert.
    entry: str
        Pattern to find a column to convert.
    utc : bool
        Convert to UTC if True.
    delete_tz : bool
        Convert to timezone-unaware if True.

    Returns
    -------
    pd.DataFrame
        Converted dataframe
    """
    columns_indexes = [index for index, name in enumerate(df.columns.values) if entry.lower() in name.lower()]

    return convert_df_columns_to_datetime_by_idx(df, columns_indexes, utc, delete_tz)


def convert_df_columns_to_datetime_by_idx(
    df: "pd.DataFrame", columns_indexes: List[int], utc: bool = None, delete_tz: bool = False
):
    """Convert dataframe columns to datetime by index.

    Parameters
    ----------
    df : pd.Dataframe
        Pandas dataframe to convert.
    columns_indexes : List[int]
        List of indexes of columns to convert.
    utc : bool
        Convert to UTC if True.
    delete_tz : bool
        Convert to timezone-unaware if True.

    Returns
    -------
    df
        Converted dataframe.
    """
    for idx in columns_indexes:
        try:
            date_value = pd.to_datetime(df.iloc[:, idx], utc=utc, errors="coerce")
        except TypeError:  # TypeError: unhashable type: 'list'
            # This error occurs when we have a big list, and it contains an unhashable type.
            # pandas.core.tools.datetimes.should_cache will decide to cache or not.
            # We can use the cache=False parameter to avoid this error.
            # But it will be slow, how said in the docstring for pd.to_datetime.
            date_value = pd.to_datetime(df.iloc[:, idx], utc=utc, errors="coerce", cache=False)

        set_df_column_value(df, idx, date_value)

        if delete_tz:
            date_value = df.iloc[:, idx].dt.tz_localize(None)
            set_df_column_value(df, idx, date_value)

    return df


def convert_df_columns_to_datetime_re(df: "pd.DataFrame", pattern: re.compile) -> "pd.DataFrame":
    """Convert dataframe columns to datetime using regular expression pattern.

    Parameters
    ----------
    df : pd.Dataframe
        Pandas dataframe to convert.
    pattern : re.compile
        Regular expression pattern to check columns.

    Returns
    -------
    df
        Converted dataframe
    """
    column_indexes = [index for index, name in enumerate(df.columns.values) if pattern.search(name)]

    return convert_df_columns_to_datetime_by_idx(df, column_indexes, utc=True, delete_tz=True)


def convert_str_to_timestamp(s: str) -> TimestampOrNaT:
    timestamp = pd.to_datetime(s, utc=True, errors="coerce")
    localized = timestamp.tz_localize(None)
    return localized


def convert_dtypes(df: "pd.DataFrame") -> "pd.DataFrame":
    """
    This function is an extension to the standard pandas.DataFrame.convert_dtypes.

    Correct return dataframe if we have this columns in dataframe:

    GOOG.O                    Currency
    Date
    2020-12-31 00:00:00+00:00     <NA>
    2020-12-31 00:00:00+00:00     <NA>

    Correct convert None, np.nan, pd.NA, pd.NaN to pd.NA, see official docs:
    https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#missing-data-na

    Correct convert big int from Linux, Windows platform.


    Parameters
    ----------
    df: pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """
    if df.empty:
        return df

    from pandas.core.dtypes.common import is_object_dtype, is_datetime64_any_dtype

    df = df.fillna(np.nan)
    columns_indexes = [index for index, _ in enumerate(df.columns.values)]

    for index in columns_indexes:
        series = df.iloc[:, index]
        if is_datetime64_any_dtype(series.dtype):
            continue

        series = series.infer_objects()
        if is_object_dtype(series):
            series = series.copy()

        inferred_dtype = _get_inferred_dtype(series)
        if str(inferred_dtype).lower() == "object":
            new_series = series.copy()
            new_series.replace("", np.nan, inplace=True)

            inferred_dtype = _get_inferred_dtype(new_series)
            if str(inferred_dtype).lower() != "object":
                series = new_series

        result = series.astype(inferred_dtype)
        set_df_column_value(df, index, result)

    df.fillna(pd.NA, inplace=True)
    return df


def _get_inferred_dtype(series: "Series") -> DtypeObj:
    from pandas.core.dtypes.cast import convert_dtypes as pandas_covert_dtypes
    from pandas.core.dtypes.common import pandas_dtype

    inferred_dtype = pandas_covert_dtypes(series.values)
    if "float" in str(inferred_dtype).lower() and (series.fillna(-9999) % 1 == 0).all():
        return pandas_dtype("Int64")
    return inferred_dtype
