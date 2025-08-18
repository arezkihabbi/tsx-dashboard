import math
import threading
from typing import Callable, Optional, Union
from typing import TYPE_CHECKING

import pandas as pd

from ._ohlc_builder import (
    merge_dataframes,
    create_df,
    retrieve_data_for_df,
    Ticks_OHLCBuilder,
    OHLCBuilder,
)
from ._recording_control import (
    RecordingControl,
    NoBlocking_RecordingControl,
    Blocking_RecordingControl,
    RepeatNonBlocking_RecordingControl,
    RepeatBlocking_RecordingControl,
)
from ._stream_update_handler import (
    BuildDF_StreamUpdateHandler,
    CollectUpdates_StreamUpdateHandler,
    StreamUpdateHandler,
)
from ..session import get_default

if TYPE_CHECKING:
    from ..content._universe_streams import _UniverseStreams


class PricingRecorder:
    """
    Pricing recorder class allows to record updates from server.
    Create dataframes based on received updates.

    Parameters
    ----------

    stream : _UniverseStreams
        UniverseStreams object

    """

    def __init__(self, stream: "_UniverseStreams"):
        self._stream = stream
        self._logger = get_default().logger()
        self._event = threading.Event()

        self._frequency = None
        self._duration = None
        self._ticks_per_bar = None
        self._on_data = None
        self._record_called = 0

        self.is_running = False

        self._ohlc_builder: Union[OHLCBuilder, None] = None
        self._update_handler: Optional[StreamUpdateHandler] = None
        self._recording_control: Optional[RecordingControl] = None

    @staticmethod
    def _parse_input_frequency_and_duration(value: str) -> int:
        last_char = value[-1]
        if last_char not in ["s", "h", "d", "m"] and not value.endswith("min"):
            raise ValueError(
                "Please provide 'duration' or 'frequency' value in valid format. For example: '10s', '2min', '1h'"
            )

        result = None
        try:
            if "s" == last_char:
                result = int(value[:-1])
            elif value.endswith("min"):
                seconds = int(value[:-3])
                result = seconds * 60
            elif "h" == last_char:
                seconds = int(value[:-1])
                result = seconds * 3600
            elif "d" == last_char:
                seconds = int(value[:-1])
                result = seconds * 3600 * 24
            elif "m" == last_char:
                seconds = int(value[:-1])
                result = seconds * 3600 * 24 * 30
        except ValueError:
            raise ValueError("Please provide 'duration' value in valid format. For example: '10s', '2min', '1h'")

        return result

    @staticmethod
    def _validate_count_argument(ticks_per_bar):
        try:
            ticks_per_bar = int(ticks_per_bar)
        except ValueError:
            raise ValueError(
                "Invalid argument. Please provide 'ticks_per_bar' in the following format: '10', '100', '500'"
            )

        if ticks_per_bar <= 0:
            raise ValueError("Invalid argument. 'ticks_per_bar' should be more then 0")

    def _validate_arguments(self, frequency: str, duration: str, ticks_per_bar: str):
        if ticks_per_bar != "1" and frequency != "tick":
            raise ValueError("Please provide 'tick' value as frequency when you are using 'ticks_per_bar' argument.")

        self._validate_count_argument(ticks_per_bar)

        if duration and frequency != "tick":
            frequency = self._parse_input_frequency_and_duration(frequency)
            duration = self._parse_input_frequency_and_duration(duration)

            self._expected_count_of_callbacks = duration / frequency

            float_part, self._expected_count_of_callbacks = math.modf(self._expected_count_of_callbacks)

            self._callback_called_count = 0
            if duration % frequency:
                self._expected_count_of_callbacks += 1

            if frequency > duration:
                raise ValueError("Please check your arguments, 'duration' should be higher that 'frequency'.")

    @staticmethod
    def _check_df(df: pd.DataFrame) -> pd.DataFrame:
        if isinstance(df, pd.DataFrame):
            df.fillna(pd.NA, inplace=True)

        else:
            df = pd.DataFrame()

        return df

    def record(
        self,
        frequency: str = "tick",
        duration: "str" = None,
        ticks_per_bar: str = "1",
        on_data: Callable = None,
    ):
        """
        Starts recording updates from server and save it in memory

        Parameters
        ----------
        frequency : str, optional
            Using to calculate ohlc based on received updates during period that was provided
        duration : str, optional
            Duration of recording data. Could be provided in seconds, minutes, hours
        ticks_per_bar : str, optional
            Count of ticks to record
        on_data : function, optional
             Callback which is calling with 'frequency' and receive dataframe
             with calculated ohlc from last updates and recorder object.
             Frequency has to be provided

        Returns
        -------
        Examples
        -------
        Start recording all updates during 15 seconds and calculate ohlc

        >>> import refinitiv.data as rd
        >>> stream = rd.open_pricing_stream(universe=['EUR='], fields=['BID', 'ASK', 'OPEN_PRC'])
        >>> stream.recorder.record(duration="15s")
        >>> stream.recorder.stop()

        >>> stream.close()
        >>> history = stream.recorder.get_history()
        >>> history.ohlc("5s")

        Start recording updates and calculate ohlc
        by using 'frequency' and call 'callback'
        function with updated ohlc dataframe every 5 seconds
        >>> import refinitiv.data as rd
        >>> stream = rd.open_pricing_stream(universe=['EUR='], fields=['BID', 'ASK', 'OPEN_PRC'])
        >>>
        >>>
        >>> def callback(dataframe, recorder):
        ...     print(dataframe)
        >>>
        >>> stream.recorder.record(frequency="5s", duration="15s", on_data=callback)
        >>> stream.recorder.stop()
        >>> stream.close()
        >>> history = stream.recorder.get_history()

        """
        if self._stream.is_close_st:
            raise ConnectionError("Stream is closed. Cannot record.")

        self._validate_arguments(frequency, duration, ticks_per_bar)

        self._frequency = frequency
        self._duration = duration
        self._ticks_per_bar = int(ticks_per_bar)
        self._on_data = on_data

        self.is_running = True

        frequency_tick = self._frequency == "tick"
        no_duration = not self._duration
        ticks_1 = self._ticks_per_bar == 1
        ticks_not_1 = self._ticks_per_bar != 1

        # stream.recorder.record(frequency='tick')
        if all([frequency_tick, no_duration, ticks_1]):
            if not isinstance(self._update_handler, CollectUpdates_StreamUpdateHandler):
                self._update_handler = CollectUpdates_StreamUpdateHandler(self._stream, recorder=self)
            self._recording_control = NoBlocking_RecordingControl(self._update_handler)
            self._recording_control.start_recording()

        # stream.recorder.record(frequency='tick', ticks_per_bar=10)
        elif all([frequency_tick, no_duration, ticks_not_1]):
            self._create_ohlc_builder(Ticks_OHLCBuilder)
            self._update_handler = BuildDF_StreamUpdateHandler(
                self._stream,
                self._ohlc_builder,
                self._ticks_per_bar,
                recorder=self,
                on_record_callback=on_data,
            )
            self._recording_control = NoBlocking_RecordingControl(self._update_handler)
            self._recording_control.start_recording()

        # stream.recorder.record(frequency='tick', duration="60s")
        elif all([frequency_tick, duration, ticks_1]):
            if not isinstance(self._update_handler, CollectUpdates_StreamUpdateHandler):
                self._update_handler = CollectUpdates_StreamUpdateHandler(self._stream, recorder=self)

            self._recording_control = Blocking_RecordingControl(self._update_handler)
            interval = self._parse_input_frequency_and_duration(self._duration)
            self._recording_control.start_recording(interval)
            self.stop()

        # stream.recorder.record(frequency='tick', duration="60s", ticks_per_bar=10)
        elif all([frequency_tick, duration, ticks_not_1]):
            self._create_ohlc_builder(Ticks_OHLCBuilder)
            self._update_handler = BuildDF_StreamUpdateHandler(
                self._stream,
                self._ohlc_builder,
                self._ticks_per_bar,
                self,
                self._on_data,
            )
            self._recording_control = Blocking_RecordingControl(self._update_handler)
            interval = self._parse_input_frequency_and_duration(self._duration)
            self._recording_control.start_recording(interval)
            self.stop()

        # stream.recorder.record(frequency='5s')
        elif all([frequency, no_duration, ticks_1]):
            self._create_ohlc_builder(OHLCBuilder)
            self._update_handler = CollectUpdates_StreamUpdateHandler(self._stream, recorder=self)
            self._recording_control = RepeatNonBlocking_RecordingControl(
                self._on_data,
                self._update_handler,
                self._ohlc_builder,
                self._logger,
                self,
            )
            interval = self._parse_input_frequency_and_duration(self._frequency)
            self._recording_control.start_recording(interval)

        # stream.recorder.record(frequency='5s', duration="17s")
        elif all([frequency, duration, ticks_1]):
            self._create_ohlc_builder(OHLCBuilder)
            self._update_handler = CollectUpdates_StreamUpdateHandler(self._stream, recorder=self)
            duration = self._parse_input_frequency_and_duration(self._duration)
            self._recording_control = RepeatBlocking_RecordingControl(
                duration,
                self._on_data,
                self._update_handler,
                self._ohlc_builder,
                self._logger,
                self,
            )
            interval = self._parse_input_frequency_and_duration(self._frequency)
            self._recording_control.start_recording(interval)
            self.stop()

        else:
            raise ValueError(
                f"Cannot cover case when "
                f"frequency={self._frequency}, "
                f"duration={self._duration}, "
                f"ticks_per_bar={self._ticks_per_bar}"
            )

    def _create_ohlc_builder(self, klass):
        if not isinstance(self._ohlc_builder, klass):
            self._ohlc_builder = klass(self._frequency, self._stream.universe, self._stream.fields)

    def get_history(self) -> "pd.DataFrame":
        dfs = []

        if self._frequency == "tick" and self._ticks_per_bar == 1:
            updates_by_stream_name = self._update_handler.updates_by_stream_name
            for universe, stream_data in updates_by_stream_name.items():
                timestamps, data, fields = retrieve_data_for_df(stream_data)
                dataframe = create_df(data, timestamps, fields, universe)
                dfs.append(dataframe)

            if not dfs:
                msg = "We didn't receive any updates. Dataframe couldn't be created."
                self._logger.warning(msg)
                df = pd.DataFrame()

            else:
                df = merge_dataframes(dfs)

        else:
            df = self._check_df(self._ohlc_builder.ohlc_df)

        return df

    def stop(self):
        """
        Stop recording updates and cancel repeat timer for creating ohlc dataframes.
        """
        if not self.is_running:
            return

        self.is_running = False
        self._recording_control.stop_recording()

    def delete(self):
        """Delete whole recorded updates"""
        self._recording_control.delete_recording()
