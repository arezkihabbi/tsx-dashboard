from enum import unique

from ....._base_enum import StrEnum


@unique
class ConstituentOverrideMode(StrEnum):
    MERGE_WITH_DEFINITION = "MergeWithDefinition"
    REPLACE_DEFINITION = "ReplaceDefinition"
