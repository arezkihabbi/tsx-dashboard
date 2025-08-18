import abc


class UniverseExpander:
    @property
    @abc.abstractmethod
    def _universe(self):
        pass

    def __iter__(self):
        self._n = 0
        return self

    def __next__(self):
        if self._n < len(self._universe):
            result = self._universe[self._n]
            self._n += 1
            return result
        raise StopIteration
