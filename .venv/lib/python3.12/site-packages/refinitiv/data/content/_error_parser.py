from ..delivery._data._data_provider import Parser


class ErrorParser(Parser):
    def process_failed_response(self, raw_response):
        parsed_data = super().process_failed_response(raw_response)
        error_code = parsed_data.first_error_code
        error_message = parsed_data.first_error_message

        status = parsed_data.status
        error = status.get("error", {})
        errors = error.get("errors", [])

        err_msgs = []
        err_codes = []
        for err in errors:
            reason = err.get("reason")
            if reason:
                err_codes.append(error_code)
                err_msgs.append(f"{error_message}: {reason}")

        if err_msgs and err_codes:
            parsed_data.error_codes = err_codes
            parsed_data.error_messages = err_msgs

        return parsed_data
