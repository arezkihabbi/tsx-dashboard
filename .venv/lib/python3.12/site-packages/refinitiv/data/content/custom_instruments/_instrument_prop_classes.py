import abc
import copy
from dataclasses import dataclass, asdict
from typing import List, Union, Optional, Generic, TypeVar

import numpy as np

from refinitiv.data._tools import (
    EnumArgsParser,
    make_parse_enum,
    make_convert_to_enum,
    custom_inst_datetime_adapter,
)
from ..._types import OptDateTime
from refinitiv.data.content.custom_instruments._enums import (
    VolumeBasedRolloverMethod,
    DayBasedRolloverMethod,
    SpreadAdjustmentMethod,
)

volume_based_rollover_method_enum_arg_parser = EnumArgsParser(
    parse=make_parse_enum(VolumeBasedRolloverMethod),
    parse_to_enum=make_convert_to_enum(VolumeBasedRolloverMethod),
)

day_based_rollover_method_enum_arg_parser = EnumArgsParser(
    parse=make_parse_enum(DayBasedRolloverMethod),
    parse_to_enum=make_convert_to_enum(DayBasedRolloverMethod),
)

spread_adjustment_method_enum_arg_parser = EnumArgsParser(
    parse=make_parse_enum(SpreadAdjustmentMethod),
    parse_to_enum=make_convert_to_enum(SpreadAdjustmentMethod),
)

_camel_to_snake = {
    "numberOfYears": "number_of_years",
    "startMonth": "start_month",
    "includeAllMonths": "include_all_months",
    "includeMonths": "include_months",
    "numberOfDays": "number_of_days",
    "monthsPrior": "months_prior",
    "joinAtDay": "join_at_day",
    "rollOccursWithinMonths": "roll_occurs_within_months",
    "rollOnExpiry": "roll_on_expiry",
    "startDate": "start_date",
    "spreadAdjustment": "spread_adjustment",
    "normalizeByWeight": "normalize_by_weight",
}


def convert_camel_to_snake(data: dict) -> dict:
    return {_camel_to_snake.get(name, name): value for name, value in data.items()}


T = TypeVar("T")


class Serializable(abc.ABC, Generic[T]):
    @abc.abstractmethod
    def _to_dict(self) -> dict:
        # for override
        pass

    @classmethod
    def _from_dict(cls, data: dict) -> T:
        # for override
        pass


@dataclass
class Constituent(Serializable["Constituent"]):
    """
    ric : str
        The instrument being considered.
    weight : int
        A numerical value multiplying the value of the default pricing field of ric.
    """

    ric: str
    weight: int

    def _to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def _from_dict(cls, data: dict) -> "Constituent":
        return cls(**data)


@dataclass
class Basket(Serializable["Basket"]):
    """
    constituents : List
        A list of objects, one for each row.
    normalize_by_weight : bool, optional
        True: means the total value computed above is divided by the total
              weight - to normalize to a total weight of 1.0.
        False: means that the basket prices are multiplied by weights and summed as is.
    """

    constituents: List[Union[Constituent, dict]]
    normalize_by_weight: bool = False

    def _to_dict(self) -> dict:
        return {
            "constituents": [item._to_dict() if isinstance(item, Constituent) else item for item in self.constituents],
            "normalizeByWeight": self.normalize_by_weight,
        }

    @classmethod
    def _from_dict(cls, data: dict) -> "Basket":
        constituents = [Constituent._from_dict(constituent) for constituent in data["constituents"]]
        normalize_by_weight = data["normalizeByWeight"]
        return cls(constituents=constituents, normalize_by_weight=normalize_by_weight)


@dataclass
class Months(Serializable["Months"]):
    """
    number_of_years: int
        Maximum of 30 - more results in an error
    include_all_month: bool
        Include all available months as a contract method
    include_months: List, Optional
        Include only selected months as contract method
    start_month: int, Optional

    """

    number_of_years: int
    include_all_months: Optional[bool] = None
    start_month: Optional[int] = None
    include_months: Optional[list] = None

    def _to_dict(self) -> dict:
        retval = {
            "numberOfYears": self.number_of_years,
        }
        if self.include_all_months:
            retval["includeAllMonths"] = self.include_all_months
        if self.start_month:
            retval["startMonth"] = self.start_month
        if self.include_months:
            retval["includeMonths"] = self.include_months
        return retval

    @classmethod
    def _from_dict(cls, data: dict) -> Optional["Months"]:
        obj = None
        months = data.get("months")
        if months:
            obj = cls(**convert_camel_to_snake(months))
        return obj


@dataclass
class VolumeBasedRollover(Serializable["VolumeBasedRollover"]):
    """
    “Method” for chaining individual contracts to produce UDCs.
        method:
        number_of_days: int
            The default for this is set at “1” which means the roll will occur between each pair of eligible contracts
            on the first day where the traded volume of the second contract exceeds that of the first.
        join_at_day: int
            Default is set at “1”. This can’t be altered when the “Number of Days” parameter is also set as “1” –
            not logical. However, you can alter this to any setting within a range limited by the minimum of “1” to
            a maximum of whatever value the “Number of Days” parameter is entered as.
        roll_occurs_within_months: int
        roll_on_expiry: bool
            This setting should the roll conditions not be met you will still get the roll to the next contract occurring
            but this will now be implemented on the expiry day of the first contract. This obviously requires that
            there is an overlap of data between the contracts. If param is False - History will terminate at the
            first point of failure to roll.

    """

    method: Union[VolumeBasedRolloverMethod, str]
    roll_occurs_within_months: int
    roll_on_expiry: bool = True
    number_of_days: int = 1
    join_at_day: int = 1

    def _to_dict(self) -> dict:
        return {
            "volumeBased": {
                "method": volume_based_rollover_method_enum_arg_parser.get_str(self.method),
                "numberOfDays": self.number_of_days,
                "joinAtDay": self.join_at_day,
                "rollOccursWithinMonths": self.roll_occurs_within_months,
                "rollOnExpiry": self.roll_on_expiry,
            }
        }

    @classmethod
    def _from_dict(cls, data: dict) -> "VolumeBasedRollover":
        data = convert_camel_to_snake(data)
        data["method"] = volume_based_rollover_method_enum_arg_parser.get_enum(data.get("method"))
        return cls(**data)


@dataclass
class DayBasedRollover(Serializable["DayBasedRollover"]):
    """
    This method supplies an entirely different approach to creating a futures continuation contract.
    The roll determination points are based purely on time and have nothing to do with comparing Volume and/or Open Interest.
        method: DayBasedRolloverMethod, str
                "daysBeforeExpiry" - the roll to the second contract occurs “X” business days before the expiry of the first contract.
                "daysBeforeEndOfMonth" - counts back business days from the final business day of a specified month –
                the default is the expiry month of the first contract.
                "daysAfterBeginningOfMonth" - the second bullet point re contracts such as CL/HO/RB.
        number_of_days: int
        month_prior: int

    """

    method: Union[DayBasedRolloverMethod, str]
    number_of_days: int
    months_prior: Optional[int] = None

    def _to_dict(self) -> dict:
        retval = {
            "dayBased": {
                "method": day_based_rollover_method_enum_arg_parser.get_str(self.method),
                "numberOfDays": self.number_of_days,
            }
        }
        if self.months_prior:
            retval["dayBased"]["monthsPrior"] = self.months_prior

        return retval

    @classmethod
    def _from_dict(cls, data: dict) -> "DayBasedRollover":
        data = convert_camel_to_snake(data)
        data["method"] = day_based_rollover_method_enum_arg_parser.get_enum(data.get("method"))
        return cls(**data)


@dataclass
class ManualItem:
    """
    month: int
    year: int
    star_date: str or datetime or timedelta
    """

    month: int
    year: int
    start_date: "OptDateTime"

    def _to_dict(self) -> dict:
        retval = {"month": self.month, "year": self.year}
        if self.start_date is not None:
            retval["startDate"] = custom_inst_datetime_adapter.get_str(self.start_date)

        return retval

    @classmethod
    def _from_dict(cls, data: dict) -> "ManualItem":
        month = data.get("month")
        year = data.get("year")
        start_date = np.datetime64(data.get("startDate"))
        return cls(month=month, year=year, start_date=start_date)


class ManualRollover(Serializable["ManualRollover"]):
    """
    “Manual” allows you to construct a futures continuation piece by piece – a process I refer to as “Daisy Chaining”.
    All that’s required is that you define consecutive contracts with the days that they should be spliced together.
        manual_items: args: ManualItem
    """

    def __init__(self, *args: ManualItem):
        self.manual_items = args

    def _to_dict(self) -> dict:
        return {"manual": [item._to_dict() if isinstance(item, ManualItem) else item for item in self.manual_items]}

    @classmethod
    def _from_dict(cls, data: List) -> "ManualRollover":
        data = [ManualItem._from_dict(item) for item in data]
        return cls(*data)


@dataclass
class SpreadAdjustment(Serializable["SpreadAdjustment"]):
    """
    adjustment: str, optional
        None: prices are not changed at all.
        arithmetic: the arithmetic difference in price is used to adjust via addition/subtraction.
        percentage: instead of adding/subtracting from the price, a percentage adjustment is made instead.
    method: str, SpreadAdjustmentMethod
        "close-to-close",
        "open-to-open",
        "close-to-open",
        "close-to-open-old-gap",
        "close-to-open-new-gap"
    backwards: bool
        True: After retrieving all of the required futures contracts data, working out the roll dates and the basis gap
        adjustments that apply, the software then applies these basis adjustments working from the most recent contract backwards.

    """

    adjustment: Optional[Union[str, None]]
    method: Union[SpreadAdjustmentMethod, str]
    backwards: bool = True

    def _to_dict(self) -> dict:
        retval = {
            "method": spread_adjustment_method_enum_arg_parser.get_str(self.method),
            "backwards": self.backwards,
        }
        if self.adjustment:
            retval["adjustment"] = self.adjustment
        return retval

    @classmethod
    def _from_dict(cls, data: dict) -> "SpreadAdjustment":
        data = data.get("spreadAdjustment")
        data["method"] = spread_adjustment_method_enum_arg_parser.get_enum(data.get("method"))
        return cls(**data)


_rollover_key_name_by_class = {
    "dayBased": DayBasedRollover,
    "volumeBased": VolumeBasedRollover,
    "manual": ManualRollover,
}


@dataclass
class UDC(Serializable["UDC"]):
    """
    root: str
        This is the uppercase letter (or letters) before the month and year of the futures contract RIC code.
    rollover: VolumeBasedRollover, DayBasedRollover, ManualRollover
    spread_adjustment: SpreadAdjustment
        When joining the prices of two contracts as rollover from one to the other,
        the price series have to be adjusted so that the prices are continuous.
    months: Months
    """

    root: str
    rollover: Union[VolumeBasedRollover, DayBasedRollover, ManualRollover]
    spread_adjustment: SpreadAdjustment
    months: Optional[Months] = None

    def _to_dict(self) -> dict:
        retval = {
            "root": self.root,
            "rollover": self.rollover._to_dict(),
            "spreadAdjustment": self.spread_adjustment._to_dict(),
        }

        if self.months:
            retval["months"] = self.months._to_dict()
        return retval

    @classmethod
    def _from_dict(cls, data: dict) -> "UDC":
        rollover_obj = None
        data = copy.deepcopy(data)
        _data_rollover = data["rollover"]

        for rollover_key, rollover_class in _rollover_key_name_by_class.items():
            if rollover_key in _data_rollover:
                rollover_obj = rollover_class._from_dict(_data_rollover[rollover_key])
                break

        if not rollover_obj:
            raise ValueError("Rollover is missing, please define rollover parameter")

        return cls(
            root=data.get("root"),
            rollover=rollover_obj,
            spread_adjustment=SpreadAdjustment._from_dict(data),
            months=Months._from_dict(data),
        )
