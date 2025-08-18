import requests

from .event import StreamEvtID
from .message_type import MessageTypeRDP
from .stream_connection import StreamConnection, LOGIN_STREAM_ID
from .stream_cxn_state import StreamCxnState
from ..._core.session import SessionCxnType
from ..._tools import lazy_dump

_message_type_to_event_id = {
    MessageTypeRDP.ACK: StreamEvtID.ACK,
    MessageTypeRDP.RESPONSE: StreamEvtID.RESPONSE,
    MessageTypeRDP.UPDATE: StreamEvtID.UPDATE,
    MessageTypeRDP.ALARM: StreamEvtID.ALARM,
    MessageTypeRDP.ERROR: StreamEvtID.ERROR,
    MessageTypeRDP.HEARTBEAT: StreamEvtID.HEARTBEAT,
}


class RDPStreamConnection(StreamConnection):
    @property
    def subprotocol(self) -> str:
        return "rdp_streaming"

    def get_login_message(self) -> dict:
        message = {
            "method": "Auth",
            "streamID": f"{LOGIN_STREAM_ID:d}",
        }
        if self._session._get_session_cxn_type() == SessionCxnType.DESKTOP:
            message["appKey"] = self._session.app_key
            message["authorization"] = f"Bearer {self._session._access_token}"
        else:
            message["token"] = self._session._access_token
        return message

    def _handle_login_message(self, message: dict) -> None:
        """
        Parameters
        ----------
        message: dict
            The login message from the server.

        Example
        ----------
        >>> message
        ... {
        ...     'state': {
        ...         'code': 200,
        ...         'status': 'OK',
        ...         'message': 'Access token is valid'
        ...     },
        ...     'type': 'Ack',
        ...     'streamID': '2'
        ... }
        """
        state = message.get("state", {})
        status = state.get("status")
        code = state.get("code")

        # "OK" for qps and "Ok" for tds
        if status == "OK" or status == "Ok":
            self._state = StreamCxnState.MessageProcessing
            self._connection_result_ready.set()
            self.events.dispatch_login_success(message)

        elif status == "Closed" or status == "Error" or code == requests.codes.bad:
            self.is_debug() and self.debug(
                f"{self._classname} received a bad message: state={self.state}, message={message}"
            )
            self._state = StreamCxnState.Disconnected
            not self.can_reconnect and self._connection_result_ready.set()
            self._config.info_not_available()
            self._listener.close()
            self.events.dispatch_login_fail(message)

        else:
            raise ValueError(
                f"{self._classname}._handle_login_message() | Don't know what to do: state={self.state}, message={message}"
            )

    def _process_message(self, message: dict) -> None:
        self.is_debug() and self.debug(f"{self._classname} process message %s", lazy_dump(message))
        event_id = _message_type_to_event_id.get(message.get("type"))

        if event_id is None:
            raise ValueError(f"Unknown message type {message}")

        if event_id == StreamEvtID.HEARTBEAT:
            return

        self._emit_event_with_stream_id(event_id, message)

    def _emit_event_with_stream_id(self, event_id: StreamEvtID, message: dict) -> None:
        try:
            stream_id = int(message.get("streamID"))
        except TypeError as e:
            raise ValueError(f"streamID is not found in message {message}") from e

        self.events.dispatch(stream_id + event_id, message)
