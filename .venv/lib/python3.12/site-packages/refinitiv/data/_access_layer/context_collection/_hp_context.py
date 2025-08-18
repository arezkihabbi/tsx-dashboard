import abc
from collections import defaultdict
from typing import Optional, Dict, Tuple, List

from pandas import DataFrame

from ._context import Context, UDFMixin, RDPMixin
from ...content._historical_raw_transf import transform_to_dicts


class HPContext(Context, abc.ABC):
    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.hp and (not self.fields or self.fields.hp))

    @property
    def can_build_df(self) -> bool:
        return bool(self._hp_data and not (self._adc_data or self._cust_inst_data))

    @property
    def raw(self) -> Optional[Dict]:
        return self._hp_data and self._hp_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._hp_data and self._hp_data.df

    @property
    @abc.abstractmethod
    def date_name(self) -> str:
        #  for override
        pass

    def get_data_fields(self) -> Tuple[Dict[str, List[Dict]], List[str]]:
        """
        historical_raw is:
        {
            'universe': {'ric': 'GS.N'},
            'interval': 'P1D',
            'summaryTimestampLabel': 'endPeriod',
            'adjustments': ['exchangeCorrection', 'manualCorrection', 'CCH', 'CRE', 'RTS', 'RPO'],
            'defaultPricingField': 'TRDPRC_1',
            'qos': {'timeliness': 'delayed'},
            'headers': [{'name': 'DATE', 'type': 'string'}, {'name': 'BID', 'type': 'number', 'decimalChar': '.'}],
            'data': [['2023-04-17', 339.7], ['2023-04-14', 336.88]],
            'meta': {
                'blendingEntry': {
                    'headers': [{'name': 'DATE', 'type': 'string'}, {'name': 'BID', 'type': 'number', 'decimalChar': '.'}],
                    'data': [['2023-04-17', 339.7]]
                }
            }
        }
        """
        dicts_by_ric = defaultdict(list)
        fields = self.fields.hp
        return_new_fields = False
        date_name = self.date_name.casefold()
        for historical_raw in self.raw:
            try:
                if not fields:
                    fields = [header["name"] for header in historical_raw["headers"]]
                    return_new_fields = True

                dicts = transform_to_dicts(historical_raw, fields, date_name)
                ric = historical_raw["universe"]["ric"]
            except Exception:
                fields = None
                ric = None
                dicts = [{date_name: None}]

            dicts_by_ric[ric].extend(dicts)

        return (
            dicts_by_ric,
            list(fields) if return_new_fields else list(self.fields),
        )


class HPUDFContext(UDFMixin, HPContext):
    pass


class HPRDPContext(RDPMixin, HPContext):
    pass
