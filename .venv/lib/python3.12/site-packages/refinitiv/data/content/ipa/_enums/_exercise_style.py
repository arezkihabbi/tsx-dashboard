from enum import unique

from ...._base_enum import StrEnum


@unique
class ExerciseStyle(StrEnum):
    """
    - AMER: the owner has the right to exercise on any date before the option
      expires,
    - BERM: the owner has the right to exercise on any of several specified dates
      before the option expires. all exercise styles may not apply to certain option
      types. optional. if instrumentcode of listed eti option is defined, the value
      comes from the instrument reference data,
    - EURO: the owner has the right to exercise only on enddate.

    """

    AMER = "AMER"
    BERM = "BERM"
    EURO = "EURO"
