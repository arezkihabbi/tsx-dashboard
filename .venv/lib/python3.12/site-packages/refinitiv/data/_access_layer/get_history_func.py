import warnings
from datetime import date, datetime, timedelta
from typing import Optional, Union, Iterable

from pandas import DataFrame

from refinitiv.data.errors import RDError
from ._containers import UniverseContainer, FieldsContainer, ADCDataContainer, HPDataContainer, CustInstDataContainer
from ._data_provider import get_hp_data, get_custominsts_data, get_adc_data
from ._history_df_builder_factory import get_history_df_builder
from ._intervals_consts import INTERVALS
from .._tools._common import get_warning_message_if_parameter_no_used_in_request
from .context_collection import get_hp_context, get_adc_context, get_cust_inst_context
from .._core.session import get_default, raise_if_closed
from .._tools import fr_datetime_adapter
from .._types import OptDateTime
from ..content.fundamental_and_reference._data_grid_type import get_data_grid_type_by_session
from ..usage_collection._filter_types import FilterType
from ..usage_collection._logger import get_usage_logger
from ..usage_collection._utils import ModuleName


def get_history(
    universe: Union[str, Iterable[str]],
    fields: Union[str, Iterable[str], None] = None,
    interval: Optional[str] = None,
    start: "OptDateTime" = None,
    end: "OptDateTime" = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
    use_field_names_in_headers: bool = None,
    parameters: Union[str, dict, None] = None,
) -> DataFrame:
    """
    Retrieves the pricing history, as well as Fundamental and Reference data history.

    Parameters
    ----------
    universe: str | list
        Instruments to request
    fields: str | list, optional
        Fields to request
    interval: str, optional
        Date interval. Supported intervals are:
        tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
        1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
    start: str or date or datetime or timedelta, optional
        The start date and timestamp of the requested history
    end: str or date or datetime or timedelta, optional
        The end date and timestamp of the requested history
    adjustments : str, optional
        Tells the system whether to apply or not apply CORAX (Corporate Actions)
        events or exchange/manual corrections or price and volume adjustment
        according to trade/quote qualifier summarization actions to historical time
        series data. Possible values are:
        exchangeCorrection, manualCorrection, CCH, CRE, RTS, RPO, unadjusted,
        qualifiers
    count : int, optional
        The maximum number of data points returned. Values range: 1 - 10000.
        Applies only to pricing fields.
    use_field_names_in_headers : bool, default False
        If True - returns field name as column headers for data instead of title
    parameters: str | dict, optional
        Single global parameter key=value or dictionary
        of global parameters to request.
        Applies only to TR fields.

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """
    if use_field_names_in_headers is None:
        use_field_names_in_headers = False
        use_field_names_in_headers_passed = False

    else:
        use_field_names_in_headers_passed = True
        warnings.warn(
            "Parameter 'use_field_names_in_headers' is deprecated and will be removed in future library version v2.0.",
            FutureWarning,
        )

    session = get_default()
    raise_if_closed(session)

    logger = session.logger()

    if interval is not None and interval not in INTERVALS:
        raise ValueError(f"Not supported interval value.\nSupported intervals are: {list(INTERVALS.keys())}")

    # Library usage logging
    get_usage_logger().log_func(
        name=f"{ModuleName.ACCESS}.get_history",
        func_path=f"{__name__}.get_history",
        kwargs=dict(
            universe=universe,
            fields=fields,
            interval=interval,
            start=start,
            end=end,
            count=count,
            adjustments=adjustments,
            parameters=parameters,
            use_field_names_in_headers=use_field_names_in_headers,
        ),
        desc={FilterType.SYNC, FilterType.LAYER_ACCESS},
    )

    universe = UniverseContainer(universe)
    fields = FieldsContainer(fields)
    data_grid_type = get_data_grid_type_by_session(session)
    hp = get_hp_context(data_grid_type, universe, fields, use_field_names_in_headers)
    adc = get_adc_context(data_grid_type, universe, fields, use_field_names_in_headers)
    cust_inst = get_cust_inst_context(data_grid_type, universe, fields, use_field_names_in_headers)
    exceptions = list()

    if adjustments is not None:
        not_applicable = []
        if cust_inst.can_get_data:
            not_applicable.append(f"custom instruments universe {cust_inst.universe.cust_inst}")
        if adc.can_get_data:
            not_applicable.append(f"fields {adc.fields.adc}")

        if not_applicable:
            warnings.warn(
                get_warning_message_if_parameter_no_used_in_request("adjustments", not_applicable=not_applicable)
            )

    universe.calc_hp(None)
    if parameters is not None:
        not_applicable = []
        applicable = []
        if cust_inst.can_get_data:
            not_applicable.append(f"custom instruments universe {universe.cust_inst}")
        if hp.can_get_data:
            if fields.hp:
                not_applicable.append(f"fields {fields.hp}")
            elif not fields:
                applicable.append("TR fields")
        if applicable or not_applicable:
            warnings.warn(get_warning_message_if_parameter_no_used_in_request("parameters", not_applicable, applicable))

    adc_raw = None
    adc_df = None
    if adc.can_get_data:
        adc_params = get_adc_params(start, end, interval)
        adc_params.update(parameters or {})
        adc_raw, adc_df, adc_exception_msg = get_adc_data(
            universe=universe.adc,
            fields=fields.adc,
            parameters=adc_params,
            use_field_names_in_headers=use_field_names_in_headers,
            logger=logger,
            use_field_names_in_headers_passed=use_field_names_in_headers_passed,
        )
        exceptions.append(adc_exception_msg)

    adc_data = ADCDataContainer(adc_raw, adc_df, fields)
    universe.calc_hp(adc_data.raw)

    hp_raw = None
    hp_df = None
    if hp.can_get_data:
        hp_raw, hp_df, hp_exception_msg = get_hp_data(
            universe=universe.hp,
            interval=interval,
            start=start,
            end=end,
            adjustments=adjustments,
            count=count,
            fields=fields.hp,
            logger=logger,
        )
        exceptions.append(hp_exception_msg)

    hp_data = HPDataContainer(hp_raw, hp_df)
    cust_inst_raw = None
    cust_inst_df = None
    if cust_inst.can_get_data:
        cust_inst_raw, cust_inst_df, cust_inst_exception_msg = get_custominsts_data(
            universe=universe.cust_inst,
            interval=interval,
            start=start,
            end=end,
            count=count,
            logger=logger,
        )
        exceptions.append(cust_inst_exception_msg)

    cust_inst_data = CustInstDataContainer(cust_inst_raw, cust_inst_df)

    if exceptions and all(exceptions):
        except_msg = "\n\n".join(exceptions)
        raise RDError(-1, except_msg)

    if not any({adc_data, hp_data, cust_inst_data}):
        return DataFrame()

    adc.set_data(adc_data, hp_data, cust_inst_data)
    hp.set_data(adc_data, hp_data, cust_inst_data)
    cust_inst.set_data(adc_data, hp_data, cust_inst_data)

    history_provider = get_history_df_builder(data_grid_type)
    return history_provider.build_df_date_as_index(adc, hp, cust_inst, universe.hp, interval)


def get_adc_params(
    start: Union[str, date, datetime, timedelta],
    end: Union[str, date, datetime, timedelta],
    interval: Optional[str],
) -> dict:
    """
    Gets parameters for ADC request.

    Parameters
    ----------
    start : str or date or datetime or timedelta
        Parameters start date.
    end : str or date or datetime or timedelta
        Parameters end date.
    interval : str, optional
        Interval using to calculate parameters.

    Returns
    -------
    parameters : dict
        Parameters for ADC requests.
    """
    parameters = {}
    if start is not None:
        parameters["SDate"] = fr_datetime_adapter.get_str(start)

    if end is not None:
        parameters["EDate"] = fr_datetime_adapter.get_str(end)

    if interval is not None:
        parameters["FRQ"] = INTERVALS[interval]["adc"]

    return parameters
