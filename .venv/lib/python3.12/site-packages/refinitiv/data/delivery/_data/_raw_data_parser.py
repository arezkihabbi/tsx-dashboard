from json import JSONDecodeError
from typing import TYPE_CHECKING, Tuple

import requests

from ._parsed_data import ParsedData
from ..._tools import get_response_reason

if TYPE_CHECKING:
    import httpx

success_http_codes = [
    requests.codes.ok,
    requests.codes.accepted,
    requests.codes.created,
]


class Parser:
    def process_successful_response(self, raw_response: "httpx.Response") -> ParsedData:
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }

        media_type = raw_response.headers.get("content-type", "")

        if "/json" in media_type:
            try:
                content_data = raw_response.json()
                if content_data is None:
                    # Some HTTP responses, such as a DELETE,
                    # can be successful without any response body.
                    content_data = {}

                parsed_data = ParsedData(status, raw_response, content_data)
            except (TypeError, JSONDecodeError) as error:
                message = f"Failed to process HTTP response : {str(error)}"
                status["content"] = message
                content_data = raw_response.text
                parsed_data = ParsedData(status, raw_response, content_data)

        elif (
            "text/plain" in media_type
            or "text/html" in media_type
            or "text/xml" in media_type
            or "image/" in media_type
        ):
            content_data = raw_response.text
            parsed_data = ParsedData(status, raw_response, content_data)

        else:
            status["content"] = f"Unknown media type returned: {media_type}"
            parsed_data = ParsedData(status, raw_response)

        return parsed_data

    def process_failed_response(self, raw_response: "httpx.Response") -> ParsedData:
        status = {
            "http_status_code": raw_response.status_code,
            "http_reason": get_response_reason(raw_response),
        }
        error_codes = []
        error_messages = []

        try:
            content_data = raw_response.json()

            if not isinstance(content_data, list):
                content_data = [content_data]

            for content_item in content_data:
                content_error = content_item.get("error")

                if content_error:
                    if isinstance(content_error, str):
                        content_error = {"code": None, "message": content_error}

                    status["error"] = content_error
                    error_code = raw_response.status_code
                    error_message = content_error.get("message", "")

                else:
                    error_code = raw_response.status_code
                    error_message = raw_response.text

                if error_code == 403:
                    if not error_message.endswith("."):
                        error_message += ". "

                    error_message += "Contact Refinitiv to check your permissions."

                error_codes.append(error_code)
                error_messages.append(error_message)

        except (TypeError, JSONDecodeError):
            error_codes.append(raw_response.status_code)
            error_messages.append(raw_response.text)

        parsed_data = ParsedData(
            status,
            raw_response,
            error_codes=error_codes,
            error_messages=error_messages,
        )
        return parsed_data

    def parse_raw_response(self, raw_response: "httpx.Response") -> Tuple[bool, ParsedData]:
        is_success = False

        if raw_response is None:
            return is_success, ParsedData({}, {})

        is_success = raw_response.status_code in success_http_codes

        if is_success:
            parsed_data = self.process_successful_response(raw_response)

        else:
            parsed_data = self.process_failed_response(raw_response)

        return is_success, parsed_data
