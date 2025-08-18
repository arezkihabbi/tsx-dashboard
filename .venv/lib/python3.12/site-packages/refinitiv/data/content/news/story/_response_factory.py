from typing import TYPE_CHECKING

from ....delivery._data._response_factory import ResponseFactory

if TYPE_CHECKING:
    from ....delivery._data._parsed_data import ParsedData


class NewsStoryResponseFactory(ResponseFactory):
    @staticmethod
    def _try_write_error(parsed_data: "ParsedData"):
        new_error_msg = "Error while calling the NEP backend: Story not found"
        error_code = parsed_data.first_error_code
        error_msg = parsed_data.first_error_message

        if error_code == 400 or error_code == 404 and new_error_msg != error_msg:
            parsed_data.error_codes = 404
            parsed_data.error_messages = new_error_msg

    def create_fail(self, parsed_data: "ParsedData", **kwargs):
        self._try_write_error(parsed_data)
        return super().create_fail(parsed_data, **kwargs)
