from typing import TYPE_CHECKING

from ._chain_record import create_chain_record, can_create_chain_record
from ...._listener import EventListener
from ....delivery._stream.events import OMMCxnListeners

if TYPE_CHECKING:
    from ....delivery._stream import _OMMStream


class OMMStreamAckListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", *args, **kwargs):
        self.context.events.dispatch_ack(*args)


class OMMStreamCompleteListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", *args, **kwargs):
        self.context.events.dispatch_complete(*args)


class OMMStreamErrorListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", *args, **kwargs):
        self.context.events.dispatch_error(*args)


class OMMStreamRefreshListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", message: dict, *args, **kwargs):
        context = self.context
        fields = message.get("Fields", [])
        if can_create_chain_record(fields):
            chain_record = create_chain_record(fields)
            context.records_by_name[originator.name] = chain_record

            if not context.display_template:
                context.display_template = chain_record.display_template

            context.refresh_evt_by_name[originator.name].set()

        else:
            context.error(f"StreamingChain :: Cannot parse chain {originator.name} because it is an invalid chain.")

        self.context.events.dispatch_refresh(message)


class OMMStreamStatusListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", message: dict, *args, **kwargs):
        context = self.context
        if message.get("State", {}).get("Stream") == "Closed":
            context.events.dispatch_error(message, originator.name)
            context.close()

        context.events.dispatch_status(message)


class OMMStreamUpdateListener(EventListener["StreamingChain"]):
    def callback(self, originator: "_OMMStream", message: dict, *args, **kwargs):
        context = self.context
        if not context.complete_evt.is_set():
            context.update_messages.append((originator.name, message))
            context.warning("StreamingChain :: waiting to update because chain decode does not completed.")
            return

        context.process_remaining_update_messages()
        context.update_chain_record(originator.name, message)


class StreamingChainListeners(OMMCxnListeners):
    ack_listener_class = OMMStreamAckListener
    complete_listener_class = OMMStreamCompleteListener
    error_listener_class = OMMStreamErrorListener
    refresh_listener_class = OMMStreamRefreshListener
    status_listener_class = OMMStreamStatusListener
    update_listener_class = OMMStreamUpdateListener
