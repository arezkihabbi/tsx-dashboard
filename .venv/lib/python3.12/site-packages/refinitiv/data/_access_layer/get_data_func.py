import warnings
from typing import Iterable, Union

from pandas import DataFrame

from ._containers import ADCDataContainer, FieldsContainer, HPAndCustInstDataContainer, UniverseContainer
from ._data_df_builder import DataDFBuilder
from ._data_provider import get_data_from_stream, get_adc_data_safe
from .._tools._common import get_warning_message_if_parameter_no_used_in_request
from .context_collection import get_adc_context, get_hp_and_custinst_context
from .._core.session import get_default, raise_if_closed
from .._errors import RDError
from ..content.fundamental_and_reference._data_grid_type import get_data_grid_type_by_session
from ..usage_collection import FilterType, get_usage_logger
from ..usage_collection._utils import ModuleName


def get_data(
    universe: Union[str, Iterable[str]],
    fields: Union[str, Iterable[str], None] = None,
    parameters: Union[str, dict, None] = None,
    use_field_names_in_headers: bool = None,
) -> DataFrame:
    """
    Retrieves pricing snapshots, as well as Fundamental and Reference data.

    Parameters
    ----------
    universe: str | list
        Instruments to request
    fields: str | list, optional
        Fields to request
    parameters: str | dict, optional
        Single key=value global parameter or dictionary of global parameters to request
    use_field_names_in_headers: bool, default False
        If True - returns field name as column headers for data instead of title

    Returns
    -------
    pandas.DataFrame

    Examples
    --------
    >>> get_data(universe=['IBM.N', 'VOD.L'], fields=['BID', 'ASK'])
    >>> get_data(
    ...     universe=['GOOG.O', 'AAPL.O'],
    ...     fields=['TR.EV','TR.EVToSales'],
    ...     parameters = {'SDate': '0CY', 'Curn': 'CAD'}
    ...)
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

    # Library usage logging
    get_usage_logger().log_func(
        name=f"{ModuleName.ACCESS}.get_data",
        func_path=f"{__name__}.get_data",
        kwargs=dict(
            universe=universe,
            fields=fields,
            parameters=parameters,
            use_field_names_in_headers=use_field_names_in_headers,
        ),
        desc={FilterType.SYNC, FilterType.LAYER_ACCESS},
    )

    exceptions = list()
    universe = UniverseContainer(universe)
    fields = FieldsContainer(fields)
    data_grid_type = get_data_grid_type_by_session(session)
    adc = get_adc_context(data_grid_type, universe, fields, use_field_names_in_headers)
    hp_and_cust_inst = get_hp_and_custinst_context(data_grid_type, universe, fields, use_field_names_in_headers)

    universe.calc_hp(None)
    if parameters:
        not_applicable = []
        applicable = []
        if universe.cust_inst:
            not_applicable.append(f"custom instruments universe {universe.cust_inst}")

        if fields.hp:
            not_applicable.append(f"fields {fields.hp}")
        elif not fields:
            applicable.append("TR fields")
        if not_applicable or applicable:
            warnings.warn(get_warning_message_if_parameter_no_used_in_request("parameters", not_applicable, applicable))

    adc_raw, adc_df, adc_exception_msg = None, None, None
    if adc.can_get_data:
        adc_raw, adc_df, adc_exception_msg = get_adc_data_safe(
            {
                "universe": universe.adc,
                "fields": fields.adc,
                "parameters": parameters,
                "use_field_names_in_headers": use_field_names_in_headers,
            },
            logger,
            use_field_names_in_headers_passed,
        )
        exceptions.append(adc_exception_msg)

    universe.calc_hp(adc_raw)

    stream_columns, stream_data, stream_df, hp_exception_msg = None, None, None, None
    if hp_and_cust_inst.can_get_data:
        stream_columns, stream_data, stream_df, hp_exception_msg = get_data_from_stream(
            universe.hp_and_cust_inst, fields.hp, session
        )
        exceptions.append(hp_exception_msg)

    if exceptions and all(exceptions):
        except_msg = "\n\n".join(exceptions)
        raise RDError(-1, except_msg)

    hp_and_cust_inst_data = HPAndCustInstDataContainer(stream_columns, stream_data, stream_df)
    adc_data = ADCDataContainer(adc_raw, adc_df, fields)
    adc.set_data(adc_data=adc_data, hp_data=hp_and_cust_inst_data)
    hp_and_cust_inst.set_data(adc_data=adc_data, hp_data=hp_and_cust_inst_data)
    df = DataDFBuilder.build_df(adc, hp_and_cust_inst)
    df.rename(columns={"instrument": "Instrument"}, inplace=True)
    return df
