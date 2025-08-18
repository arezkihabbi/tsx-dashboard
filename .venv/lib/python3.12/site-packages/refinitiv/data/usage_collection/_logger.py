import time
from queue import Empty, Queue
from threading import Thread, Lock
from typing import List, Set, Optional, Type, Tuple

from ._abstract_logger import AbstractUsageLogger
from ._utils import LogRecord, RecordData, LoggerConfig
from ._filter_types import FilterType
from .._configure import get_config


class UsageLoggerProxy(Thread):
    """
    This class is a wrapper around a threading.Thread that runs a
    logging thread. It is used to log usage data from the RD Library.

    Parameters
    ----------
    batch_size : int
        The maximum number of records to send to the loggers at once.
    flush_timeout : int
        The maximum time to wait before flushing the batch buffer.
    logging_enabled : bool
        Whether to enable logging.

    Examples
    --------
    >>> from refinitiv.data.usage_collection import get_usage_logger
    >>> class UserLogger(AbstractUsageLogger):
    >>>     def __init__(self, *args, **kwargs):
    >>>         ...
    >>>     def log(self, records: List[LogRecord]) -> None:
    >>>         ...
    >>>     def close(self) -> None:
    >>>         ...
    >>>
    >>> logger = get_usage_logger()
    >>> logger.add_logger(UserLogger)
    >>> logger.start()
    >>> ...
    >>> logger.join()
    """

    def __init__(
        self,
        batch_size: int = 100,
        flush_timeout: int = 10,
        logging_enabled: bool = True,
    ) -> None:
        super().__init__(name="UsageLoggerThread", daemon=True)
        self._queue: Queue = Queue()
        self._loggers: List[LoggerConfig] = []
        self._lock = Lock()
        self._logger_instances: List[Tuple[AbstractUsageLogger, Set[FilterType]]] = []
        self._batch_buffer: List[LogRecord] = []
        self._batch_size: int = batch_size
        self._flush_timeout: int = flush_timeout
        self._logging_enabled = logging_enabled
        self._last_flush: int = 0

    @property
    def logging_enabled(self):
        return self._logging_enabled

    @property
    def queue(self):
        return self._queue

    @staticmethod
    def _filter_batch(batch: List[LogRecord], logger_filter: Optional[Set[FilterType]]) -> List[LogRecord]:
        """
        Filter the batch by the given filter.
        Parameters
        ----------
        batch : List[LogRecord]
        logger_filter : Optional[Set[FilterType]]

        Returns
        -------

        """
        return [record for record in batch if not logger_filter or (logger_filter & record.filter)]

    def flush(self) -> None:
        """
        Flush the batch buffer to the loggers.
        Returns
        -------

        """
        if self._batch_buffer:
            # For each registered logger send the whole buffer
            for _logger, _filter in self._logger_instances:
                _logger.log(self._filter_batch(self._batch_buffer, _filter))
            self._batch_buffer.clear()
            self._last_flush = time.monotonic()

    def _update_loggers(self) -> None:
        """
        Update the list of logger instances.
        Returns
        -------

        """
        with self._lock:
            for logger_config in self._loggers:
                self._logger_instances.append(
                    (
                        logger_config.logger_type(*logger_config.args, **logger_config.kwargs),
                        logger_config.filters,
                    )
                )
            self._loggers = []

    def run(self) -> None:
        self._last_flush = time.monotonic()

        while True:
            if len(self._loggers) > 0:
                self._update_loggers()
            try:
                record = self._queue.get(timeout=max(0.1, self._flush_timeout - (time.monotonic() - self._last_flush)))
            except Empty:
                self.flush()
                continue
            if record is None:
                break
            self._batch_buffer.append(record)
            if len(self._batch_buffer) >= self._batch_size:
                self.flush()
        self.flush()
        for logger, _ in self._logger_instances:
            logger.close()

    def start(self) -> None:
        if self._logging_enabled:
            super().start()

    def add_logger(
        self,
        logger: Type[AbstractUsageLogger],
        _filter: Set[FilterType],
        *args,
        **kwargs,
    ) -> None:
        """
        Add a logger to the logging thread.
        """
        if self._logging_enabled:
            if not issubclass(logger, AbstractUsageLogger):
                raise ValueError("Logger must be a subclass of UsageLogger")
            with self._lock:
                self._loggers.append(LoggerConfig(logger, args, kwargs, _filter))
        else:
            raise RuntimeError("Tried to add a logger to a disabled logger thread. Check session config")

    def log(self, record: LogRecord) -> None:
        if self._logging_enabled:
            self.queue.put(record)

    def log_func(
        self,
        name: str,
        func_path: str,
        args: tuple = None,
        kwargs: dict = None,
        result: object = None,
        desc: Set[FilterType] = None,
    ) -> None:
        if self._logging_enabled:
            if args is None:
                args = ()
            if kwargs is None:
                kwargs = {}
            if desc is None:
                desc = set()
            self.log(
                LogRecord(name, func_path, RecordData(args, kwargs, result), desc),
            )

    def join(self, timeout: Optional[float] = None) -> None:
        """
        Stop the logger thread.
        Parameters
        ----------
        timeout : Optional[float]

        Returns
        -------

        """
        if self._logging_enabled:
            self.queue.put(None)
            try:
                super().join(timeout)
            except RuntimeError:
                pass
            self._logging_enabled = False


usage_logger: Optional[UsageLoggerProxy] = None


def get_usage_logger() -> UsageLoggerProxy:
    global usage_logger
    if usage_logger is None:
        logging_enabled = get_config().get_bool("usage_logger.enabled")
        usage_logger = UsageLoggerProxy(logging_enabled=logging_enabled)
        usage_logger.start()
    return usage_logger
