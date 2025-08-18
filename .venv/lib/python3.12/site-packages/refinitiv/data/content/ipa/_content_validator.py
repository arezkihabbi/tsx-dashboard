from typing import TYPE_CHECKING

from ...delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ...delivery._data._data_provider import ParsedData


class CurvesAndSurfacesContentValidator(ContentValidator):
    _NAME_DATA = "data"

    @classmethod
    def content_data_is_not_none(cls, data: "ParsedData") -> bool:
        if data.content_data.get(cls._NAME_DATA) is None:
            data.error_codes = 1
            data.error_messages = "Content data is None"
            return False

        return True

    @classmethod
    def any_element_have_no_error(cls, data: "ParsedData") -> bool:
        elements = data.content_data.get(cls._NAME_DATA)
        if isinstance(elements, list):
            counter = len(elements) or 1
            for element in elements:
                if not hasattr(element, "get"):
                    counter -= 1
                    data.error_messages = f"Invalid data type={type(element)}, data={element}"
                    continue

                error = element.get("error")

                if error:
                    counter -= 1
                    error_code = error.get("code")
                    data.error_codes.append(error_code)
                    error_message = error.get("message")
                    data.error_messages.append(error_message)

            if counter == 0:
                return False

        return True
