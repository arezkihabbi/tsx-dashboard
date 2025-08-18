from typing import TYPE_CHECKING

import pandas as pd

from .._core.session import get_default
from .._log import is_debug
from .._tools import convert_dtypes

if TYPE_CHECKING:
    from .context_collection import ADCContext, HPAndCustInstContext


class DataDFBuilder:
    @staticmethod
    def build_df(
        adc: "ADCContext",
        hp_and_cust_inst: "HPAndCustInstContext",
    ) -> pd.DataFrame():
        logger = get_default().logger()
        is_debug(logger) and logger.debug("[DataDFBuilder.build_df] Start")
        msg = "[DataDFBuilder.build_df] End"
        if not adc.raw and not hp_and_cust_inst.raw:
            is_debug(logger) and logger.debug(msg)
            return pd.DataFrame()

        elif hp_and_cust_inst.can_build_df:
            is_debug(logger) and logger.debug(msg)
            return hp_and_cust_inst.df

        elif adc.can_build_df:
            is_debug(logger) and logger.debug(msg)
            return adc.df

        adc_headers_names = adc.headers_names
        columns = adc_headers_names + hp_and_cust_inst.columns

        if not any(columns):
            is_debug(logger) and logger.debug(msg)
            return pd.DataFrame()

        else:
            if not adc_headers_names and hp_and_cust_inst.columns:
                columns.insert(0, "Instrument")
            elif "instrument" in columns:
                columns[columns.index("instrument")] = "Instrument"

            adc_data = adc.get_data_wid_universe_as_index()

            data = []
            for universe in hp_and_cust_inst.raw:
                if universe in adc_data:
                    for column in adc_data[universe]:
                        column.extend(hp_and_cust_inst.raw[universe])
                        data.append(column)

                else:
                    tmpl = [universe] + [pd.NA] * (len(adc_headers_names) - 1) + hp_and_cust_inst.raw[universe]
                    adc_data[universe] = tmpl
                    data.append(tmpl)
            is_debug(logger) and logger.debug(msg)
            return convert_dtypes(pd.DataFrame(data, columns=columns))
