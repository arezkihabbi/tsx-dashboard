import abc
import math
import threading
from typing import TYPE_CHECKING, Callable, Optional, Union

from pandas import NA

from .._tools import RepeatedTimer

if TYPE_CHECKING:
    from ._stream_update_handler import (
        CollectUpdates_StreamUpdateHandler,
        BuildDF_StreamUpdateHandler,
        StreamUpdateHandler,
    )
    from ._ohlc_builder import OHLCBuilder


class RecordMixin:
    logger = None
    update_handler: "StreamUpdateHandler" = None
    ohlc_builder: "OHLCBuilder" = None
    on_record_callback: Callable = None

    def check_recorded_updates(self):
        for (
            steam_name,
            updates,
        ) in self.update_handler.updates_by_stream_name.items():
            if updates:
                self.record()
                break

    def record(self):
        updates_by_stream_name = self.update_handler.updates_by_stream_name
        self.ohlc_builder.build(updates_by_stream_name)
        ohlc_df = self.ohlc_builder._last_recorded_ohlc_updates

        if self.on_record_callback:
            try:
                if not ohlc_df.empty:
                    ohlc_df.fillna(NA, inplace=True)

                t = threading.Thread(target=self.on_record_callback, args=(ohlc_df, self._recorder))
                t.start()

            except Exception as error:
                self.logger.exception("Error occurred in user's callback function.")
                self.logger.exception(error)


class RecordingControl(abc.ABC):
    @abc.abstractmethod
    def start_recording(self):
        pass

    @abc.abstractmethod
    def stop_recording(self):
        pass

    @abc.abstractmethod
    def delete_recording(self):
        pass


class NoBlocking_RecordingControl(RecordingControl):
    def __init__(
        self,
        update_handler: Union["CollectUpdates_StreamUpdateHandler", "BuildDF_StreamUpdateHandler"],
    ) -> None:
        self.update_handler = update_handler

    def start_recording(self):
        self.update_handler.start_handling()

    def stop_recording(self):
        if self.update_handler._ticks_per_bar != 1:
            self.update_handler.check_recorded_updates()

        self.update_handler.stop_handling()

    def delete_recording(self):
        self.update_handler.dispose()


class Blocking_RecordingControl(RecordingControl):
    def __init__(
        self,
        update_handler: Union["CollectUpdates_StreamUpdateHandler", "BuildDF_StreamUpdateHandler"],
    ) -> None:
        self.update_handler = update_handler
        self.blocking = threading.Event()

    def start_recording(self, interval: int = 0):
        self.update_handler.start_handling()
        self.blocking.wait(interval)

    def stop_recording(self):
        if self.update_handler._ticks_per_bar != 1:
            self.update_handler.check_recorded_updates()
        self.update_handler.stop_handling()
        self.blocking.clear()

    def delete_recording(self):
        self.update_handler.dispose()


class RepeatNonBlocking_RecordingControl(RecordingControl, RecordMixin):
    timer: Optional[RepeatedTimer] = None

    def __init__(
        self,
        on_record_callback: Callable,
        update_handler: "CollectUpdates_StreamUpdateHandler",
        ohlc_builder: "OHLCBuilder",
        logger,
        recorder,
    ) -> None:
        self.logger = logger
        self.ohlc_builder = ohlc_builder
        self.update_handler = update_handler
        self.on_record_callback = on_record_callback
        self._recorder = recorder

    def start_recording(self, interval: int):
        self.update_handler.start_handling()
        self.timer = RepeatedTimer(function=self.record, interval=interval)
        self.timer.start()

    def stop_recording(self):
        self.check_recorded_updates()
        self.update_handler.stop_handling()
        self.ohlc_builder.dataframes = []
        self.timer.cancel()

    def delete_recording(self):
        self.ohlc_builder.dispose()
        self.update_handler.dispose()


class RepeatBlocking_RecordingControl(RecordingControl, RecordMixin):
    def __init__(
        self,
        duration: int,
        on_record_callback: Callable,
        update_handler: "CollectUpdates_StreamUpdateHandler",
        ohlc_builder: "OHLCBuilder",
        logger,
        recorder: "PricingRecorder",
    ) -> None:
        self.logger = logger
        self.ohlc_builder = ohlc_builder
        self.update_handler = update_handler
        self.on_record_callback = on_record_callback
        self.duration = duration
        self.blocking = threading.Event()
        self._recorder = recorder

    def start_recording(self, interval: int):
        self.update_handler.start_handling()

        remainder, count = math.modf(self.duration / interval)
        count = int(count)
        for _ in range(count):
            self.blocking.wait(interval)
            self.record()

        if remainder:
            remainder = self.duration - (count * interval)
            self.blocking.wait(remainder)
            self.record()

    def stop_recording(self):
        self.update_handler.stop_handling()
        self.ohlc_builder.dataframes = []
        self.blocking.clear()

    def delete_recording(self):
        self.ohlc_builder.dispose()
        self.update_handler.dispose()
