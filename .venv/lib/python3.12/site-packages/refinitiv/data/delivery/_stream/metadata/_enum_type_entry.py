from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class EnumTypeEntry:
    value_type: str
    values: List[int]
    display_type: str
    displays: List[str]

    def __str__(self):
        return f"Enum Type Entry:  values ={self.values}, displays={self.displays}"


def create_enum_entry(values_data: dict, displays_data: dict) -> EnumTypeEntry:
    return EnumTypeEntry(
        value_type=values_data["Type"],
        values=values_data["Data"],
        display_type=displays_data["Type"],
        displays=displays_data["Data"],
    )
