from enum import unique

from refinitiv.data._base_enum import StrEnum


@unique
class ConstituentOverrideMode(StrEnum):
    MERGE_WITH_DEFINITION = "MergeWithDefinition"
    REPLACE_DEFINITION = "ReplaceDefinition"
