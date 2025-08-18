from typing import Optional, Union

from ._repo_underlying_contract import UnderlyingContract
from ..._enums import BuySell, DayCountBasis
from ..._param_item import enum_param_item, list_serializable_param_item, param_item, datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class RepoInstrumentDefinition(Serializable):
    def __init__(
        self,
        instrument_tag: Optional[str] = None,
        start_date: "OptDateTime" = None,
        end_date: "OptDateTime" = None,
        tenor: Optional[str] = None,
        buy_sell: Union[BuySell, str] = None,
        day_count_basis: Union[DayCountBasis, str] = None,
        underlying_instruments: Optional[UnderlyingContract] = None,
        is_coupon_exchanged: Optional[bool] = None,
        repo_rate_percent: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.instrument_tag = instrument_tag
        self.start_date = start_date
        self.end_date = end_date
        self.tenor = tenor
        self.buy_sell = buy_sell
        self.day_count_basis = day_count_basis
        self.underlying_instruments = underlying_instruments
        self.is_coupon_exchanged = is_coupon_exchanged
        self.repo_rate_percent = repo_rate_percent

    @staticmethod
    def get_instrument_type():
        return "Repo"

    def _get_items(self):
        return [
            enum_param_item.to_kv("buySell", self.buy_sell),
            enum_param_item.to_kv("dayCountBasis", self.day_count_basis),
            list_serializable_param_item.to_kv("underlyingInstruments", self.underlying_instruments),
            datetime_param_item.to_kv("endDate", self.end_date),
            param_item.to_kv("instrumentTag", self.instrument_tag),
            param_item.to_kv("isCouponExchanged", self.is_coupon_exchanged),
            param_item.to_kv("repoRatePercent", self.repo_rate_percent),
            datetime_param_item.to_kv("startDate", self.start_date),
            param_item.to_kv("tenor", self.tenor),
        ]
