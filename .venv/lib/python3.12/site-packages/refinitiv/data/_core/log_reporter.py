import logging


class LogReporter:
    """
    The class for convenient use log's methods in child classes.

    Methods
    -------
    log(level, msg, *args, **kwargs)
        Log 'msg % args' with the integer severity 'level'.
    warning(msg, *args, **kwargs)
        Log 'msg % args' with severity 'WARNING'.
    error(msg, *args, **kwargs)
        Log 'msg % args' with severity 'ERROR'.
    debug(msg, *args, **kwargs)
        Log 'msg % args' with severity 'DEBUG'.
    info(msg, *args, **kwargs)
        Log 'msg % args' with severity 'INFO'.
    """

    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self.log = logger.log
        self.warning = logger.warning
        self.error = logger.error
        self.debug = logger.debug
        self.info = logger.info

    def is_debug(self):
        return self._logger.level == logging.DEBUG


class _LogReporter:
    """
    The class for convenient use log's methods in child classes.

    Methods
    -------
    _log(level, msg, *args, **kwargs)
        Log 'msg % args' with the integer severity 'level'.
    _warning(msg, *args, **kwargs)
        Log 'msg % args' with severity 'WARNING'.
    _error(msg, *args, **kwargs)
        Log 'msg % args' with severity 'ERROR'.
    _debug(msg, *args, **kwargs)
        Log 'msg % args' with severity 'DEBUG'.
    _info(msg, *args, **kwargs)
        Log 'msg % args' with severity 'INFO'.
    """

    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self.init_logger(logger)

    def _is_debug(self):
        return self._logger.level == logging.DEBUG

    def init_logger(self, logger):
        self._log = logger.log
        self._warning = logger.warning
        self._error = logger.error
        self._debug = logger.debug
        self._info = logger.info


class PrvLogReporterMixin:
    def _init_logger(self, logger):
        self._log = logger.log
        self._warning = logger.warning
        self._error = logger.error
        self._debug = logger.debug
        self._info = logger.info
