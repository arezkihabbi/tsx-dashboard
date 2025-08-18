import abc


class Grant(abc.ABC):
    _argument_key_to_config_key = {}

    @abc.abstractmethod
    def is_valid(self) -> bool:
        pass

    def _update_session_arguments(self, arguments: dict, config: dict) -> None:
        for argument, value in self._argument_key_to_config_key.items():
            arguments[argument] = config.get(value)
