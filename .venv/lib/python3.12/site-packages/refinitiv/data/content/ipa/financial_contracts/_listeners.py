from typing import TYPE_CHECKING

from ....delivery._stream.events import RDPCxnListeners, ResponseRDPListener, UpdateRDPListener

if TYPE_CHECKING:
    from ....delivery._stream import StreamConnection, _RDPStream  # noqa: F401


class QuantitativeResponseRDPListener(ResponseRDPListener["_RDPStream"]):
    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        context = self.context
        if "data" in message:
            context.data = message["data"]

        if "headers" in message:
            context.headers = message["headers"]
            context.column_names = [col["name"] for col in context.headers]

        super().callback(originator, message, *args, **kwargs)


class QuantitativeUpdateRDPListener(UpdateRDPListener["_RDPStream"]):
    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        context = self.context
        if "data" in message:
            context.data = message["data"]

        super().callback(originator, message, *args, **kwargs)


class QuantitativeStreamListeners(RDPCxnListeners):
    response_listener_class = QuantitativeResponseRDPListener
    update_listener_class = QuantitativeUpdateRDPListener
