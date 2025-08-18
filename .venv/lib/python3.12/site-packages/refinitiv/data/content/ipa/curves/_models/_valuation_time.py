from typing import TYPE_CHECKING

from ..._param_item import param_item
from ..._serializable import Serializable

if TYPE_CHECKING:
    from ....._types import OptStr


class ValuationTime(Serializable):
    """
    Parameters
    ----------
    city_name : str, optional
        The city name according to market identifier code (mic) (e.g., 'new york')  see
        iso 10383 for reference.
    local_time : str, optional
        Local time or other words time in offset timezone. the value is expressed in iso
        8601 format: [hh]:[mm]:[ss] (e.g., '14:00:00').
    market_identifier_code : str, optional
        Market identifier code (mic) is a unique identification code used to identify
        securities trading exchanges, regulated and non-regulated trading markets. e.g.
        xnas.  see iso 10383 for reference.
    time_zone_offset : str, optional
        Time offsets from utc. the value is expressed in iso 8601 format: [hh]:[mm]
        (e.g., '+05:00').
    """

    def __init__(
        self,
        city_name: "OptStr" = None,
        local_time: "OptStr" = None,
        market_identifier_code: "OptStr" = None,
        time_zone_offset: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.city_name = city_name
        self.local_time = local_time
        self.market_identifier_code = market_identifier_code
        self.time_zone_offset = time_zone_offset

    def _get_items(self):
        return [
            param_item.to_kv("cityName", self.city_name),
            param_item.to_kv("localTime", self.local_time),
            param_item.to_kv("marketIdentifierCode", self.market_identifier_code),
            param_item.to_kv("timeZoneOffset", self.time_zone_offset),
        ]
