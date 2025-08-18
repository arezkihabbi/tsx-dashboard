from enum import unique, Enum


@unique
class EventCode(Enum):
    """
    Each session can report different status events during its lifecycle.
        StreamConnecting : the connection to the stream service within the session is pending.
        StreamConnected : the connection to the stream service has been successfully established.
        StreamDisconnected : the connection to the stream service is not established.
        SessionAuthenticationSuccess : the session has successfully authenticated this client.
        SessionAuthenticationFailed : the session has failed to authenticate this client.
        StreamAuthenticationSuccess: the stream has successfully authenticated this client.
        StreamAuthenticationFailed: the stream has failed to authenticate this client.
        DataRequestOk : the request for content from the session data services has completed successfully.
        DataRequestFailed : the request for content from the session data services has failed.
    """

    StreamConnecting = 1
    StreamConnected = 2
    StreamDisconnected = 3
    StreamAuthenticationSuccess = 4
    StreamAuthenticationFailed = 5
    StreamReconnecting = 6

    SessionConnecting = 21
    SessionConnected = 22
    SessionDisconnected = 23
    SessionAuthenticationSuccess = 24
    SessionAuthenticationFailed = 25
    SessionReconnecting = 26

    DataRequestOk = 61
    DataRequestFailed = 62
