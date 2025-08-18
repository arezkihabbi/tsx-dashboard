"""
RDP stream is used to subscribe to streaming items of generic RDP WebSocket Protocol to support more simplified and
generic data model without limited by existing Refinitiv property technology.

RDP stream emits a number of different events that application can listen to in order to be notified of the latest
fields values in real-times.
"""

__all__ = ("Definition",)

from ._stream.rdp_stream_definition import Definition
