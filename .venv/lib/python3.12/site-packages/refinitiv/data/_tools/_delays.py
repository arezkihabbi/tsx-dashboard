from typing import List


class Delays:
    def __init__(self, delays: List[int]) -> None:
        self._delays = delays
        self._index = 0

    def next(self) -> int:
        if self._index >= len(self._delays):
            self._index = len(self._delays) - 1
        delay = self._delays[self._index]
        self._index += 1
        return delay

    def reset(self):
        self._index = 0

    def __len__(self):
        return len(self._delays)


SECONDS_5 = 5
SECONDS_10 = 10
SECONDS_15 = 15
MINUTE_1 = 60
MINUTES_5 = 5 * MINUTE_1
MINUTES_10 = 10 * MINUTE_1
MINUTES_15 = 15 * MINUTE_1
HOUR_1 = 60 * MINUTE_1
HOURS_2 = 2 * HOUR_1


def get_delays() -> Delays:
    delays = Delays(
        [
            SECONDS_5,
            SECONDS_10,
            SECONDS_15,
            MINUTE_1,
        ]
    )
    return delays
