from typing import TYPE_CHECKING

from ..delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ..delivery._data._data_provider import ParsedData


class UniverseContentValidator(ContentValidator):
    @classmethod
    def content_data_has_no_error(cls, data: "ParsedData") -> bool:
        error = data.content_data.get("error", {})
        if error:
            data.error_codes = error.get("code")
            error_message = error.get("description")

            if error_message == "Unable to resolve all requested identifiers.":
                universe = data.raw_response.url.params["universe"].split(",")
                error_message = f"{error_message} Requested items: {universe}"

            if not error_message:
                error_message = error.get("message")
                errors = error.get("errors")

                if isinstance(errors, list):
                    errors = "\n".join(map(str, errors))
                    error_message = f"{error_message}:\n{errors}"

            data.error_messages = error_message

            return False

        invalid_universes = [
            universe.get("Instrument")
            for universe in data.content_data.get("universe", [])
            if universe.get("Organization PermID") == "Failed to resolve identifier(s)."
        ]
        if invalid_universes:
            data.error_messages = f"Failed to resolve identifiers {invalid_universes}"

        return True

    def __init__(self) -> None:
        super().__init__()
        self.validators.append(self.content_data_has_no_error)
