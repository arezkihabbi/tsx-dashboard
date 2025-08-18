from typing import TYPE_CHECKING

from ...delivery._stream.events import RDPCxnListeners, ResponseRDPListener, UpdateRDPListener

if TYPE_CHECKING:
    from ...delivery._stream import StreamConnection


class TDSResponseRDPListener(ResponseRDPListener["TradeDataStream"]):
    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        """
        Extract the response order summaries, order events and state

        Parameters
        ----------
        {
            'streamID': '5',
            'type': 'Response',
            'headers': [
                        {'id': 'OrderKey', 'type': 'String'},
                        {'id': 'OrderTime', 'type': 'String', 'format': 'datetime'},
                        {'id': 'OrderStatus', 'type': 'String'},
            ],
            'state': {
                'code': 200,
                'status': 'Ok',
                'stream': 'Open',
                'message': 'queueSize=133'
            }
        }
        """
        context = self.context
        context.headers_ids = [hdr["id"] for hdr in message.get("headers", [])]

        context.process_data(message)

        messages_data = message.get("messages", [])
        for datum in messages_data:
            context.events.dispatch_event(datum)

        context.process_state(message)
        super().callback(originator, message, *args, **kwargs)


class TDSUpdateRDPListener(UpdateRDPListener["TradeDataStream"]):
    def callback(self, originator: "StreamConnection", message: dict, *args, **kwargs):
        """
        Extract the update (add/update/remove) order summaries and new order status.
        """
        context = self.context
        context.process_data(message)

        update_data = message.get("update", [])
        for datum in update_data:
            context.events.dispatch_update(datum)

        removed_data = message.get("remove", [])
        for datum in removed_data:
            context.events.dispatch_remove(datum)

        messages_data = message.get("messages", [])
        for datum in messages_data:
            context.events.dispatch_event(datum)

        context.process_state(message)
        super().callback(originator, message, *args, **kwargs)


class TDSStreamListeners(RDPCxnListeners):
    response_listener_class = TDSResponseRDPListener
    update_listener_class = TDSUpdateRDPListener
