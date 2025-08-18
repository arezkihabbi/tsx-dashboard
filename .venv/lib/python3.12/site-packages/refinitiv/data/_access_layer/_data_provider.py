from logging import Logger
from typing import Dict, List, Optional, Union, Tuple
from typing import TYPE_CHECKING

import pandas as pd
from pandas import DataFrame

from ._intervals_consts import INTERVALS, EVENTS_INTERVALS
from ._mixed_streams import MixedStreams
from .._log import is_debug
from .._tools import DEBUG, has_any_substrings, DATE_SUBSTRINGS, convert_dtypes
from ..content import custom_instruments, fundamental_and_reference, historical_pricing
from ..content._get_adc_data import get_adc_data as get_response_data
from ..errors import ScopeError, RDError

if TYPE_CHECKING:
    from .._core.session import Session
    from logging import Logger


def get_hp_data(
    universe: List[str],
    fields: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    adjustments: Optional[str],
    count: Optional[int],
    logger: Logger,
) -> Tuple[Union[Dict, None], Union[DataFrame, None], Union[str, None]]:
    """
    Gets historical pricing raw data.

    Parameters
    ----------
    universe : str / list
        Instruments to request.
    fields : str / list
        Fields for request.
    interval: str, optional
        Consolidation interval.
    start : str, optional
        Start date.
    end : str, optional
        End date.
    adjustments : str, optional
        Adjustments for request.
    count : int, optional
        Number of data rows.
    logger : Logger
        Session logger.

    Returns
    -------
    raw : dict or None:
        Historical pricing raw data.
    df : DataFrame or None
        Historical pricing dataframe.
    exception_msg : str or None
        API exception message.
    """
    raw = None
    df = None
    exception_msg = None
    if interval in EVENTS_INTERVALS:
        definition = historical_pricing.events.Definition(
            universe=universe,
            eventTypes=INTERVALS[interval]["event_types"],
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval

        definition = historical_pricing.summaries.Definition(
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields,
        )

    try:
        response = definition.get_data()
        DEBUG and logger.debug(f"HISTORICAL_PRICING --->\n{response.data.df.to_string()}\n")
        raw = response.data.raw
        if isinstance(raw, dict):
            raw = [raw]
        df = response.data.df
    except RDError as hp_error:
        DEBUG and logger.exception(f"Failure sending request with {definition}, error:{hp_error}")
        exception_msg = hp_error.message
    except Exception as exc:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {exc}")
        exception_msg = str(exc)

    return raw, df, exception_msg


def get_adc_data(
    universe: List[str],
    fields: List[str],
    parameters: dict,
    use_field_names_in_headers: bool,
    logger: Logger,
    use_field_names_in_headers_passed: bool,
) -> Tuple[Union[Dict, None], Union[DataFrame, None], Union[str, None]]:
    raw = None
    df = None
    exception_msg = None

    definition = fundamental_and_reference.Definition(
        universe=universe,
        fields=fields,
        parameters=parameters,
        row_headers="date",
        use_field_names_in_headers=use_field_names_in_headers if use_field_names_in_headers_passed else None,
    )
    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"ADC --->\n{response.data.df.to_string()}\n")
    except ScopeError as scope_error:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {scope_error}")
        exception_msg = (
            f"Insufficient scope for key={scope_error.key}, "
            f"method={scope_error.method} failed.\n "
            f"Required scope: {' OR '.join(map(str, scope_error.required_scope))}\n "
            f"Missing scopes: {' OR '.join(map(str, scope_error.missing_scopes))}"
        )
    except RDError as adc_error:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {adc_error}")
        exception_msg = adc_error.message
    except Exception as exc:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {exc}")
        exception_msg = str(exc)

    return raw, df, exception_msg


def get_adc_data_safe(
    params: dict, logger: "Logger", use_field_names_in_headers_passed: bool
) -> Tuple[dict, DataFrame, Union[str, None]]:
    """
    Gets data from ADC and handles exceptions, if necessary.

    Parameters
    ----------
    params : dict
        Input parameters with instruments and fields.
    logger : Logger
        Session logger.

    Returns
    -------
    raw : dict
        ADC raw data.
    df : DataFrame
        ADC dataframe.
    exception_msg : str or None
        API exception message, if returned.

    """
    raw = {}
    df = DataFrame()
    exception_msg = None

    if not use_field_names_in_headers_passed:
        del params["use_field_names_in_headers"]

    try:
        data = get_response_data(params, logger)
        raw = data.raw
        df = data.df
    except ScopeError as scope_error:
        DEBUG and logger.exception(
            f"Failure sending request with " f"{params.get('fields', '')} for {params['universe']}. " f"{scope_error}"
        )
        exception_msg = (
            f"Insufficient scope for key={scope_error.key}, "
            f"method={scope_error.method} failed.\n "
            f"Required scope: {' OR '.join(map(str, scope_error.required_scope))}\n "
            f"Missing scopes: {' OR '.join(map(str, scope_error.missing_scopes))}"
        )
    except RDError as adc_error:
        DEBUG and logger.exception(
            f"Failure sending request with {params.get('fields', '')} for {params['universe']}. {adc_error}"
        )
        exception_msg = adc_error.message
    except Exception as exc:
        DEBUG and logger.exception(
            f"Failure sending request with {params.get('fields', '')} for {params['universe']}. {str(exc)}"
        )
        exception_msg = str(exc)
    return raw, df, exception_msg


def get_custominsts_data(
    universe: List[str],
    interval: Optional[str],
    start: Optional[str],
    end: Optional[str],
    count: Optional[int],
    logger: Logger,
) -> Tuple[Union[Dict, None], Union[DataFrame, None], Union[str, None]]:
    """
    Get custom instruments data.

    Parameters
    ----------
    universe : list of str
        Instruments for request.
    interval : str, optional
        Interval for request.
    start : str, optional
        Start date.
    end : str, optional
        End date.
    count : int, optional
        Maximum number of retrieved data.
    logger : Logger
        Session logger.

    Returns
    -------
    raw : dict or None:
        Custom instruments raw data.
    df : DataFrame or None
        Custom instruments dataframe.
    exception_msg : str or None
        API exception message.
    """
    raw = None
    df = None
    exception_msg = None
    if interval in EVENTS_INTERVALS:
        definition = custom_instruments.events.Definition(
            universe=universe,
            start=start,
            end=end,
            count=count,
        )

    else:
        interval = INTERVALS[interval]["pricing"] if interval is not None else interval
        definition = custom_instruments.summaries.Definition(
            universe=universe,
            interval=interval,
            start=start,
            end=end,
            count=count,
        )

    try:
        response = definition.get_data()
        raw = response.data.raw
        df = response.data.df
        DEBUG and logger.debug(f"CUSTOMINSTS --->\n{response.data.df.to_string()}\n")
    except RDError as cust_error:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {cust_error}")
        exception_msg = cust_error.message
    except Exception as exc:
        DEBUG and logger.exception(f"Failure sending request with {definition}. {exc}")
        exception_msg = str(exc)

    return raw, df, exception_msg


def get_columns_from_stream(stream: "Stream") -> List[str]:
    """
    Gets columns names from stream.

    Parameters
    ----------
    stream : Stream
        Pricing stream.

    Returns
    -------
    list of str
        Columns names.

    """
    columns = set()
    for _stream in stream:
        fields = _stream.fields or []
        columns.update(fields)
    return list(columns)


def convert_types(values: list, columns: list, logger: "Logger") -> None:
    """
    Converts types for values. If value is None or empty string, it will be converted to pd.NA.
    If column name contains any of DATE_SUBSTRINGS, it will be converted to datetime.
    If length of values and columns are different, it will be logged as warning.
    """

    if len(values) != len(columns):
        logger.warning(
            f"[convert_types] Columns and values have different length: {len(columns)} != {len(values)}, cannot convert types."
        )
        return

    for idx, zipped in enumerate(zip(values, columns)):
        value, column = zipped
        if value is None or value == "":
            values[idx] = pd.NA

        elif has_any_substrings(column, DATE_SUBSTRINGS):
            values[idx] = pd.to_datetime(values[idx], errors="ignore")


def get_columns_and_data_from_stream(stream: "Stream", fields: List[str], logger: "Logger") -> Tuple[List[str], dict]:
    """
    Gets columns names and raw data items from stream.

    Parameters
    ----------
    logger: Logger
        Session logger
    stream : Stream
        Pricing stream.
    fields : list of str
        Input columns names.

    Returns
    -------
    columns : list of strings
        Columns names.
    data
        Pricing raw data.

    """
    stream_columns = get_columns_from_stream(stream)

    if fields:
        columns = [i for i in fields if i in stream_columns]

    else:
        columns = stream_columns

    data = {}
    for _stream in stream:
        values = [_stream[column] for column in columns]
        convert_types(values, columns, logger)
        data[_stream.name] = values

    return columns, data


def get_data_from_stream(
    universe: Union[str, List[str]], fields: Union[str, List[str]], session: "Session"
) -> Tuple[Union[List[str], None], Union[dict, None], DataFrame, Union[str, None]]:
    """
    Gets pricing and custom instruments data from stream.

    Parameters
    ----------
    universe : str or list of str
        Instruments using to get data.
    fields : str or list of str
        Instruments fields for request.
    session: Session
        Session instance.

    Returns
    -------
    columns : list of str or None
        Names of data columns, if returned.
    data : dict or None
        Pricing raw data, if returned.
    df : DataFrame
        Pricing dataframe, if returned, else empty DataFrame.
    exception_msg : str or None
        API exception message, if returned.

    """
    logger = session.logger()
    logger.info(f"Requesting pricing info for fields={fields} via websocket")
    stream = MixedStreams(universe=universe, fields=fields, session=session)
    columns, data, exception_msg, df = None, None, None, DataFrame()

    try:
        stream.open(with_updates=False)
        columns, data = get_columns_and_data_from_stream(stream, fields, logger)
        df = stream.get_snapshot(fields=fields)
        if len(df.columns) == 1 or not any(_stream.fields for _stream in stream):
            df = DataFrame()
        else:
            df = convert_dtypes(df)
        stream.close()

    except Exception as exc:
        is_debug(logger) and logger.debug(f"Failure retrieving data for {stream.universe}")
        exception_msg = str(exc)

    return columns, data, df, exception_msg
