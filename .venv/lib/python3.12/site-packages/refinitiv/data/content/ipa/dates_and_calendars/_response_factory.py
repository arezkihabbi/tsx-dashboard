from typing import TYPE_CHECKING

from ....content._content_response_factory import ContentResponseFactory

if TYPE_CHECKING:
    from ....delivery._data._parsed_data import ParsedData


class DatesAndCalendarsResponseFactory(ContentResponseFactory):
    def create_fail(self, parsed_data: "ParsedData", **kwargs):
        errors = parsed_data.status.get("error", {}).get("errors")
        if errors:
            parsed_data.error_messages = f"{parsed_data.first_error_message}. {errors[0]['reason']}"
        return super().create_fail(parsed_data, **kwargs)
