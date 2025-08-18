from typing import Optional, Union

from ..._enums import ExerciseScheduleType
from ..._param_item import enum_param_item, param_item
from ..._serializable import Serializable
from ....._tools import try_copy_to_list
from ....._types import Strings


class BermudanSwaptionDefinition(Serializable):
    def __init__(
        self,
        exercise_schedule: Optional[Strings] = None,
        exercise_schedule_type: Union[ExerciseScheduleType, str] = None,
        notification_days: Optional[int] = None,
    ):
        super().__init__()
        self.exercise_schedule = try_copy_to_list(exercise_schedule)
        self.exercise_schedule_type = exercise_schedule_type
        self.notification_days = notification_days

    def _get_items(self):
        return [
            param_item.to_kv("exerciseSchedule", self.exercise_schedule),
            enum_param_item.to_kv("exerciseScheduleType", self.exercise_schedule_type),
            param_item.to_kv("notificationDays", self.notification_days),
        ]
