from abc import abstractmethod
from typing import List, Optional

import pandas as pd

from ._fetch_data import fetch_data
from ._stakeholder_data import StakeholderData


class Stakeholders:
    _stakeholders: Optional[List[StakeholderData]] = None
    _df: pd.DataFrame = None
    rics: Optional[List[str]] = None
    org_ids: Optional[List[str]] = None

    def __init__(self, instrument: str):
        self._instrument = instrument

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def get_data(self):
        """
        Gets data from the server.
        """
        self._stakeholders, self._df = fetch_data(self._instrument, self._relationship_type)
        self.rics = [item.ric for item in self._stakeholders if item.ric is not None]
        self.org_ids = [
            item.related_organization_id for item in self._stakeholders if item.related_organization_id is not None
        ]

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n >= len(self._stakeholders):
            raise StopIteration
        else:
            retval = self._stakeholders[self._n]
            self._n += 1
            return retval

    def __getitem__(self, key):
        return self._stakeholders[key]

    @property
    @abstractmethod
    def _relationship_type(self):
        pass
