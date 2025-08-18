from typing import TYPE_CHECKING, List, Callable

from ...._tools import cached_property
from ....delivery._data._data_provider import ContentValidator

if TYPE_CHECKING:
    from ....delivery._data._data_provider import ParsedData


class ContentDataValidator(ContentValidator):
    @classmethod
    def any_valid_content_data(cls, data: "ParsedData") -> bool:
        counter = 0
        content_data = data.content_data

        if isinstance(content_data, list):
            for item in content_data:
                if item.get("error"):
                    data.error_codes.append(item["error"]["code"])
                    data.error_messages.append(item["error"]["message"])
                    counter += 1

            if counter == len(content_data):
                return False

        return True

    @cached_property
    def validators(self) -> List[Callable[["ParsedData"], bool]]:
        return [self.content_data_is_not_none, self.any_valid_content_data]
