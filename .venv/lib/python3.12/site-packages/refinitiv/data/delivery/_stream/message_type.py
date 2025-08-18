from enum import unique

from ..._base_enum import StrEnum


@unique
class MessageTypeOMM(StrEnum):
    PING = "Ping"
    REFRESH = "Refresh"
    UPDATE = "Update"
    STATUS = "Status"
    ERROR = "Error"
    ACK = "Ack"


@unique
class MessageTypeRDP(StrEnum):
    ACK = "Ack"
    RESPONSE = "Response"
    UPDATE = "Update"
    ALARM = "Alarm"
    ERROR = "Error"
    HEARTBEAT = "Heartbeat"
