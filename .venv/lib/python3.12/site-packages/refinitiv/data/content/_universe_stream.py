import re
from typing import TYPE_CHECKING

from ._listeners import OMMListenersUniverseStm
from .._tools import cached_property
from ..delivery._stream import _OMMStream, StreamCache, get_service_and_details_omm
from ..delivery._stream.events import _OMMStreamEvts

if TYPE_CHECKING:
    from ._universe_streams import _UniverseStreams
    from .._types import ExtendedParams
    from .._content_type import ContentType
    from .._core.session import Session

# regular expression pattern for intra-field position sequence
_partial_update_intra_field_positioning_sequence_regular_expression_pattern = re.compile(
    r"[\x1b\x5b|\x9b]([0-9]+)\x60([^\x1b^\x5b|\x9b]+)"
)


def _decode_intra_field_position_sequence(cached_value: str, new_value: str):
    # find all partial update in the value
    tokens = _partial_update_intra_field_positioning_sequence_regular_expression_pattern.findall(new_value)

    # check this value contains a partial update or not?
    if len(tokens) == 0:
        # no partial update required, so done
        return new_value

    # do a partial update
    updated_value = cached_value
    for offset, replace in tokens:
        # convert offset from str to int
        offset = int(offset)
        assert offset < len(updated_value)

        # replace the value in the string
        updated_value = updated_value[:offset] + replace + updated_value[offset + len(replace) :]

    # done, return
    return updated_value


class _UniverseStream(StreamCache, _OMMStream):
    def __init__(
        self,
        content_type: "ContentType",
        name: str,
        session: "Session",
        owner: "_UniverseStreams",
        fields: list = None,
        service: str = None,
        api: str = None,
        extended_params: "ExtendedParams" = None,
    ):
        if name is None:
            raise AttributeError("Instrument name must be defined.")

        stream_id = session._get_omm_stream_id()
        self.classname: str = f"{self.__class__.__name__} owner.id={owner.id} id={stream_id} name='{name}'"  # should be before _OMMStream.__init__
        service, details = get_service_and_details_omm(content_type, session, service, api)
        StreamCache.__init__(self, name=name, fields=fields, service=service, record={})
        _OMMStream.__init__(
            self,
            stream_id=stream_id,
            session=session,
            name=name,
            details=details,
            domain="MarketPrice",
            service=service,
            fields=fields,
            extended_params=extended_params,
        )
        self.owner = owner

    @property
    def prv_fields(self):
        return self._fields

    @cached_property
    def events(self) -> _OMMStreamEvts:
        return _OMMStreamEvts(self)

    @cached_property
    def cxn_listeners(self) -> OMMListenersUniverseStm:
        return OMMListenersUniverseStm(self)

    def _decode_partial_update_field(self, key, value):
        """
        This legacy is used to process the partial update
        RETURNS the processed partial update data
        """

        fields = self._record.get("Fields", {})
        if key not in fields:
            fields[key] = value
            self.debug(f"key {key} not in self._record['Fields']")
            return value

        # process infra-field positioning sequence
        cached_value = fields[key]

        # done
        return _decode_intra_field_position_sequence(cached_value, value)

    def filter_fields(self, fields):
        return fields

    def write_to_record(self, message: dict):
        for message_key, message_value in message.items():
            if message_key == "Fields":
                fields = message_value
                if self.prv_fields:
                    fields = self.filter_fields(fields)

                # fields data
                # loop over all update items
                for key, value in fields.items():
                    # only string value need to check for a partial update
                    if isinstance(value, str):
                        # value is a string, so check for partial update string
                        # process partial update and update the callback
                        # with processed partial update
                        fields[key] = self._decode_partial_update_field(key, value)

                # update the field data
                self._record.setdefault(message_key, {})
                self._record[message_key].update(fields)
            else:
                # not a "Fields" data
                self._record[message_key] = message_value

    def remove_fields_from_record(self, fields):
        for field in fields:
            if self._record.get("Fields"):
                self._record["Fields"].pop(field, None)
