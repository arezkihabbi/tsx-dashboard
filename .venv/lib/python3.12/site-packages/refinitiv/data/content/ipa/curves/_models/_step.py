from ..._param_item import datetime_param_item
from ..._serializable import Serializable
from ....._types import OptDateTime


class Step(Serializable):
    """
    Parameters
    ----------
    effective_date : str or date or datetime or timedelta, optional

    meeting_date : str or date or datetime or timedelta, optional

    """

    def __init__(
        self,
        effective_date: "OptDateTime" = None,
        meeting_date: "OptDateTime" = None,
    ) -> None:
        super().__init__()
        self.effective_date = effective_date
        self.meeting_date = meeting_date

    def _get_items(self):
        return [
            datetime_param_item.to_kv("effectiveDate", self.effective_date),
            datetime_param_item.to_kv("meetingDate", self.meeting_date),
        ]
