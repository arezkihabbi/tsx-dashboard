from itertools import zip_longest
from typing import TYPE_CHECKING, Union

from ._content_response_factory import ContentResponseFactory
from ..delivery._data._endpoint_data import Error
from ..delivery._data._response_factory import get_closure

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData

error_message_by_code = {
    "default": "{error_message}. Requested ric: {rics}. Requested fields: {fields}",
    "TS.Intraday.UserRequestError.90001": "{rics} - The universe is not found",
    "TS.Intraday.Warning.95004": "{rics} - Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
    "TS.Intraday.UserRequestError.90006": "{error_message} Requested ric: {rics}",
}


class HistoricalResponseFactory(ContentResponseFactory):
    @staticmethod
    def _write_error(error_code, error_message, rics, parsed_data: "ParsedData", **kwargs):
        error_messages = error_message_by_code.get(error_code, "default").format(
            error_message=error_message,
            rics=rics,
            fields=kwargs.get("fields"),
        )
        parsed_data.error_codes = error_code
        parsed_data.error_messages = error_messages

    @staticmethod
    def _try_write_error(parsed_data: "ParsedData", **kwargs):
        if isinstance(parsed_data.content_data, list) and len(parsed_data.content_data) == 1:
            raw = parsed_data.content_data[0]
        else:
            raw = {}

        error_code = parsed_data.first_error_code or raw.get("status", {}).get("code")

        if error_code:
            parsed_data.error_codes = error_code
            parsed_data.error_messages = error_message_by_code.get(error_code, error_message_by_code["default"]).format(
                error_message=parsed_data.first_error_message or raw.get("status", {}).get("message"),
                rics=raw.get("universe", {}).get("ric", kwargs.get("universe")),
                fields=kwargs.get("fields"),
            )

    def get_raw(self, parsed_data: "ParsedData") -> dict:
        return parsed_data.content_data[0]

    def create_success(self, parsed_data: "ParsedData", **kwargs):
        self._try_write_error(parsed_data, **kwargs)
        return super().create_success(parsed_data, **kwargs)

    def create_fail(self, parsed_data: "ParsedData", **kwargs):
        self._try_write_error(parsed_data, **kwargs)
        return super().create_fail(parsed_data, **kwargs)

    def _do_create_response(
        self,
        is_success: bool,
        raw: Union[dict, list, str],
        parsed_data: "ParsedData",
        **kwargs,
    ):
        http_response = parsed_data.raw_response
        return self.response_class(
            is_success,
            raw=http_response,
            errors=[Error(code, msg) for code, msg in zip_longest(parsed_data.error_codes, parsed_data.error_messages)],
            closure=get_closure(http_response),
            requests_count=1,
            _data_factory=self,
            _kwargs=kwargs,
            _raw=raw,
            _request_message=[http_response.request],
            _http_response=[http_response],
            _http_headers=[http_response.headers],
            _http_status=[parsed_data.status],
        )
