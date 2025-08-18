import abc
import threading
from typing import Union


class Updater(abc.ABC):
    def __init__(self, delay: Union[int, float], name: str = None):
        self.delay: Union[int, float] = delay or 1
        self.name = name or "updater"
        self._stopped: bool = True
        self._disposed: bool = False
        self._timeout_evt: threading.Event = threading.Event()

    @property
    def is_started(self) -> bool:
        return not self._stopped and not self._disposed

    @property
    def delay(self) -> Union[int, float]:
        return self._delay

    @delay.setter
    def delay(self, value: Union[int, float]):
        self._delay = value

    def start(self) -> None:
        if self._disposed:
            raise RuntimeError(f"{self.name} disposed")

        if self.is_started:
            return

        self._stopped = False
        self._timeout_evt.clear()

        while not self._stopped:
            self._timeout_evt.wait(timeout=self.delay)

            if not self._stopped:
                try:
                    self._do_update()
                except Exception as e:
                    self.stop()
                    raise e

    def stop(self) -> None:
        if self._disposed:
            raise RuntimeError(f"{self.name} disposed")

        if self._stopped:
            return

        self._stopped = True
        self._timeout_evt.set()

    def dispose(self) -> None:
        if self._disposed:
            return

        if not self._stopped:
            self.stop()

        self._disposed = True
        self._do_dispose()
        self._timeout_evt = None

    @abc.abstractmethod
    def _do_update(self) -> None:
        # for override
        pass

    @abc.abstractmethod
    def _do_dispose(self) -> None:
        # for override
        pass


class UpdaterThreaded(abc.ABC):
    def __init__(self, delay: Union[int, float], name: str = None):
        self.delay: Union[int, float] = delay or 1
        self.name = name or "updater"
        self._stopped: bool = True
        self._disposed: bool = False
        self._timeout_evt: threading.Event = threading.Event()
        self._start_evt: threading.Event = threading.Event()
        self._thread: threading.Thread = threading.Thread(
            target=self._run,
            name=f"{self.name}-Thread",
            daemon=True,
        )

    @property
    def delay(self) -> Union[int, float]:
        return self._delay

    @delay.setter
    def delay(self, value: Union[int, float]):
        self._delay = value

    def start(self) -> None:
        if self._disposed:
            raise RuntimeError(f"{self.name} disposed")

        if self._start_evt.is_set():
            return

        self._stopped = False
        self._timeout_evt.clear()
        self._start_evt.set()

        if not self._thread.ident:
            self._thread.start()

    def _run(self):
        while not self._disposed:
            self._start_evt.wait()

            while not self._stopped:
                self._timeout_evt.wait(timeout=self.delay)

                if not self._stopped:
                    try:
                        self._do_update()
                    except Exception as e:
                        self.stop()
                        raise e

    def stop(self) -> None:
        if self._disposed:
            raise RuntimeError(f"{self.name} disposed")

        if self._stopped:
            return

        self._stopped = True
        self._timeout_evt.set()
        self._start_evt.clear()

    def dispose(self) -> None:
        if self._disposed:
            return

        if not self._stopped:
            self.stop()

        self._disposed = True
        self._do_dispose()
        self._thread = None
        self._start_evt = None
        self._timeout_evt = None

    @abc.abstractmethod
    def _do_update(self) -> None:
        # for override
        pass

    @abc.abstractmethod
    def _do_dispose(self) -> None:
        # for override
        pass
