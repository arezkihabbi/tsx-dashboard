from ..._base_enum import StrEnum


class Feed(StrEnum):
    EDGAR = "Edgar"
    CRIS = "CRIS"
    SEDAR = "SEDAR"
    TANSHIN = "Tanshin"
    YUHO = "Yuho"
    OBI = "OBI"
    CHINA = "China"
    DART = "DART"
    BRIDGE = "Bridge"
    SECNONEDGAR = "SEC NonEdgar"
    ITALY = "Italy"
    MUNI = "Muni"
