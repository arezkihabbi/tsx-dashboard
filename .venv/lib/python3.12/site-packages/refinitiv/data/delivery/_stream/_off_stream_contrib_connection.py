from .omm_stream_connection import OMMStreamConnection


class OffStreamContribConnection(OMMStreamConnection):
    @property
    def can_reconnect(self) -> bool:
        return False
